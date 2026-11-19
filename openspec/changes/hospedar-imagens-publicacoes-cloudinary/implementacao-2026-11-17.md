# Implementação local Cloudinary — 17/11/2026

Continuação autorizada pelo pedido de implementar os itens do plano. Trabalho vinculado à change ativa; execução `.venv`, sem Docker. Preservadas as alterações anteriores de busca/listas e a auditoria inicial desta data.

## Implementado

- Campos externos anuláveis e revisão no post, preservando `post.image` legado. Journal `post_image_asset` com estado, identidade, dono/operação, revisão, metadados, retenção e índices únicos. `post_id` não é referência com cascata: o registro operacional sobrevive à remoção da publicação.
- Reserva idempotente por dono e chave de operação; consulta protegida; sessão normal atual e conta ativa verificadas. Substituição exige post próprio e revisão compatível. Consulta/repetição da reserva preservam a operação mesmo após commit.
- Início de upload concedido uma única vez sob lock. Antes do envio, a reserva passa a `reconciliation_required` e registra tentativa; timeout não autoriza reenviar. Identidade `public_id` é gerada no backend e fornecida ao transporte.
- Verificação privada no Python confere recibo assinado e consulta Admin API; o Xano faz sua própria consulta autenticada ao recurso reservado antes de commit. O Xano não confia em URL ou assinatura fornecida pelo cliente como autoridade: confirma identidade, versão, formato, tamanho, dimensões e monta a URL canônica a partir da resposta autenticada do provedor.
- Recuperação de upload incerto por GET da identidade reservada, sem novo upload; assinatura interna reconstruída apenas no servidor depois da consulta autenticada. Erros/429 são sanitizados, sem retry de escrita. Leitura/verificação continuam possíveis com novos uploads desativados.
- Criação com imagem usa transação e locks de conta/reserva; repetição de uma reserva já anexada retorna a publicação existente. Criação sem anexo preserva o caminho atual sem depender do Cloudinary.
- Edição preservadora e substituição/remoção explícitas com revisão sob lock; imagem legada não é enviada a destroy. A imagem anterior só entra em fila após desvinculação confirmada. Substituição retém por 24 h; remoção explícita permite candidatura imediata, sempre sujeita ao futuro executor supervisionado.
- Exclusão do post mantém journal e coloca o asset em fila dentro da transação. Comentários e likes seguem a remoção atual. A fila recusa assets ainda referenciados. **Não há destroy nem exclusão física automática.**
- Integração local no `SocialState`: reserva → início único → upload → verificação → commit JSON; rascunho/arquivo preservados em erro e nenhum fallback silencioso ao multipart quando o fluxo externo está habilitado. Respostas de outra sessão/editor são ignoradas; cache é invalidado antes/depois da tentativa. Imagens externas têm prioridade de leitura sobre metadados legados e permanecem visíveis quando a flag é desligada.
- Editor permite solicitar remoção da imagem externa e desfazer a solicitação antes de salvar. Contrato incompatível impede falso sucesso. Caminho legado permanece disponível com a integração desligada.

## Validação executada

| Verificação | Resultado e alcance |
| --- | --- |
| `python -m unittest discover -s tests -p 'test_post_image*.py' -q` | **43 testes direcionados aprovados**: 16 de reserva/transporte, oito de contratos backend e 19 de fluxo/estado. Lambdas reais XanoScript executadas em JavaScript com dados fictícios; banco Xano não executado |
| `python -m unittest discover -s tests -p test_cloudinary_uploads.py -q` | 12 regressões do adaptador aprovadas |
| `python -m unittest discover -s tests -q` | **718 testes aprovados**, 36,316 s na rodada final |
| `python -m reflex compile --dry` | Aprovado, **6,503 s** |
| `python -m pip check` | Nenhuma dependência quebrada |
| `openspec validate hospedar-imagens-publicacoes-cloudinary --type change` | Aprovado |
| `openspec validate --all --no-interactive` | **38/38**, incluindo as nove changes ativas e 29 specs |
| `git diff --check` | Aprovado; avisos de normalização LF/CRLF não alteram conteúdo |
| Prévia Xano final, somente contratos | Aprovada, **13 documentos**: journal novo, post atualizado com seis campos, quatro funções novas, quatro endpoints novos e três endpoints existentes atualizados. Sem publicação, registros, ambiente ou GUIDs |

Comando da prévia: `xano workspace push -d xano -w 147717 -b v1 --dry-run --no-guids`, com includes `table/post.xs`, `table/post_image_asset.xs`, `function/PostImages/*.xs`, `api/codeboxd/post_image*.xs`, `api/codeboxd/posts_POST.xs`, `api/codeboxd/posts_id_PUT.xs` e `api/codeboxd/posts_id_DELETE.xs`. O workspace é somente destino da prévia, não foi usado para homologação mutável.

A primeira suíte encontrou falta da guarda de sessão como primeira instrução da rota `/begin`; corrigida mantendo rechecagem dentro da transação. O inventário do teste de revogação foi atualizado de 43 para 46 rotas protegidas por causa das três rotas autenticadas novas. Todas as 46 precisam continuar verificando sessão antes de qualquer ação. O teste de política executa a função real e rejeita sessão antiga/legada e propósito de recuperação.

## Checklist e limites

Concluídos **2.1.1, 2.1.3 e 2.1.8**, no escopo local explicitado nessas tarefas. Change passa a **6/17**, sem concluir os marcos 2.1/2.2. Código candidato das tarefas 2.1.2 e 2.1.4–2.1.6 foi preparado, mas seus critérios completos de autorização, retomada, concorrência/atomicidade e execução do banco ainda precisam de evidência; esses itens continuam abertos. Os testes estruturais e de lambdas não comprovam a concorrência do banco.

Pendências locais: executor supervisionado de prévia/reconciliação/limpeza (2.1.7) e retomada de operação pelo usuário após recarga/reabertura do editor. A API recupera reserva por ID ou repetição da chave, mas ainda não há interface para listar operações pendentes de outro editor. Uma nova sessão de cliente com ID conhecido foi testada; não alegar retomada integral de navegador após reinício.

Pendências de integração: backup/prévia revisados para o lote final, configuração privada do verificador no Xano, publicação autorizada, testes de transação/concorrência com dados descartáveis, duas contas, onze fluxos API e navegador 390/1440. Nenhum asset real foi enviado, consultado ou destruído nesta rodada. A prévia não comprova execução nem autorização no backend publicado.

`CLOUDINARY_UPLOADS_ENABLED` continua desativada; o novo gate **Xano-only** `CLOUDINARY_POST_IMAGES_CONTRACT_READY` tem default false no exemplo e não foi configurado no ambiente remoto. Não ativar por apenas instalar esses arquivos. O rollback de novas escritas conserva journal, leitura de imagens existentes e pendências de limpeza; não remove schema nem assets.

## Referências técnicas

[Admin API Cloudinary](https://cloudinary.com/documentation/admin_api), [schema XanoScript](https://raw.githubusercontent.com/xano-inc/xano-developer-mcp/main/src/xanoscript_docs/tables.md), [banco/transações](https://raw.githubusercontent.com/xano-inc/xano-developer-mcp/main/src/xanoscript_docs/database.md) e [sessões XanoScript](https://raw.githubusercontent.com/xano-inc/xano-developer-mcp/main/src/xanoscript_docs/security.md). Reflex conferido pelas skills disponíveis e pelos componentes instalados; nenhuma arte ou provedor foi substituído.
