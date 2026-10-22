# Histórico e decisões preservadas

21/10: `exigir-texto-denuncias-avaliacoes` arquivada em 5/5; dois requisitos
e cinco cen?rios sincronizados em submission-content-validation, 19 specs
validadas e evid?ncia real preservada. Restam tr?s changes ativas.

21/10, conclus?o de conte?do obrigat?rio: change em 5/5 ap?s oito rejei??es
autenticadas reais (HTTP 400) e compara??o integral das tabelas report e
user_media_interaction antes/depois, sem altera??es. Login manual privado;
sem republica??o. Mantida ativa, aguardando sincroniza??o/arquivamento.
[Evid?ncia final](changes/archive/2026-10-21-exigir-texto-denuncias-avaliacoes/validation/conclusao-api-real-2026-10-21.md).

21/10, revisao documental concluida: cinco links historicos corrigidos; estado
atual separado dos relatos antigos em README/PENDENCIAS. Conflitos (2/2) e revisao
documental (3/3) arquivados. Quatro changes funcionais permanecem ativas.
[Auditoria](changes/archive/2026-10-21-revisar-consistencia-documental-openspec/validation.md).


21/10, conclusao posterior: traducao DeepL concluida em 6/6 e arquivada.
Quatro cenarios reais de navegador (anime/livro, desktop/celular) e oito testes
aprovados; chave privada restaurada. Registros anteriores de ausencia da chave
e validacao pendente sao historicos.
[Evidencias finais](changes/archive/2026-10-21-traduzir-descricoes-deepl/validation/conclusao-navegador-2026-10-21.md).


21/10, validação posterior: 18 testes pertinentes e 12 casos de navegador com
fixtures aprovados para conteúdo obrigatório, em produção isolada via npm.
Servidor do usuário em 3000 preservado; contrato remoto não reenviado. Conteúdo
em 4/5 por falta de sessão autenticada real. DeepL em 5/6: ausência atual da
chave configurada impede validar tradução; fallback original confirmado no
navegador. Evidências e tentativas preservadas nas duas changes ativas.

21/10/2026, rodada posterior: concluídas e arquivadas as duas changes de processo
(4/4 cada). AGENTS.md exige change ativa e criação quando ausente, distingue
investigação de leitura e registra evidências por critério. Bloco Reflex idêntico
por bytes; 140 arquivos de implementação, HEAD e índice preservados. Merge
bc26305 confirmado ancestral de develop; sem conflitos no índice ou marcadores
nos 384 arquivos examinados. Nenhum commit/push/reset criado nesta rodada.
[Registro](validation/encerramento-processo-git-2026-10-21.md).

21/10/2026: arquivadas `avaliar-meias-estrelas` (5/5),
`corrigir-erros-operacionais` (7/7) e `padronizar-listas-iniciais` (7/7).
Contratos consolidados em media-interactions, operational-reliability e
data-user-lists, com cenários anteriores preservados. Sete changes continuam
abertas, incluindo scaffold incompleto de regularização Git. Sem nova execução
de produto ou dados remotos. [Registro](validation/arquivamento-changes-2026-10-21.md).

21/10/2026: usuário confirmou reset sem preservar listas e com personalização
posterior. Backup privado antes de remover 15 listas/três itens (quatro listas
órfãs); sete contas receberam 14 listas base vazias. Um 429 interrompeu criações;
recuperação explícita criou somente faltantes, sem novas exclusões. Signup com
acentuação corrigido e publicado, somente um contrato alterado. Catálogo e
avaliações iguais por hash; personalizada/navegação cobertas por testes locais.
[Evidência](changes/archive/2026-10-21-padronizar-listas-iniciais/validation/execucao-2026-10-21.md).

Continuação da otimização em 20/10: removida carga da home ao abrir comunidade,
preservando perfis/conexões e descartando aviso tardio de outra rota. 274 testes
e compile aprovados. Utilitários de frontend isolados; tentativas de produção
continuaram falhando no prerender, com um build direto por Node aprovado.
Não houve navegador ou validação autenticada nova; 11/37 mantidas.
[Evidência](changes/otimizar-performance-app/validation/comunidade-sem-home-2026-10-20.md).

Rodada de texto obrigatório em 20/10/2026: denúncias e formulário de avaliações
passam a exigir texto escrito; contratos publicados após backup/dry-run, somente
dois endpoints alterados. 269 testes/compile passaram. Browser não executou casos
por falha de build/prerender; usuário pediu retorno à análise de performance.
[Registro](changes/archive/2026-10-21-exigir-texto-denuncias-avaliacoes/validation/implementacao-2026-10-20.md).

Correção operacional em 20/10/2026 após relato TMDB: app havia herdado bloqueio
de rede do executor. Reinício aprovado com rede restaurou consultas reais
(quatro endpoints 200/20 itens) e três fileiras de 20 cards no browser. Utilitários
ganharam preflight e 11 testes pertinentes passaram; nenhuma chave foi alterada.
[Registro](changes/otimizar-performance-app/validation/tmdb-rede-restaurada-2026-10-20.md).

Rodada posterior em 20/10/2026: pedido de concluir o restante levou a 11/37
tarefas da change de performance, com 259 testes e compilação aprovados.
Concluídas 2.2/3.4/4.3/5.1/5.2 localmente; browser com fixtures validou fichas
dos quatro tipos e falhas 429 em 1440/390px. Não há encerramento global: contas
reais, metas e etapas de diagnóstico/implementação/integração continuam abertas.
[Registro](changes/otimizar-performance-app/validation/continuacao-fichas-busca-2026-10-20.md).

Continuação em 20/10/2026: usuário orientou concluir várias tarefas; encerradas
2.1/3.1/3.2/3.3 de performance com diagnóstico e implementação local de leituras
concorrentes/retry/cooldown. 244 testes e compilação aprovados; sem reinício,
navegador ou remoto. A change passa de 2 para 6 tarefas concluídas, de 37.
[Evidência](changes/otimizar-performance-app/validation/cache-concorrencia-cooldown-2026-10-20.md).

Em 20/10/2026, após solicitação de executar uma tarefa pendente, concluída 1.1
de `otimizar-performance-app`: inventário estático de 21 rotas e eventos/funções,
com ferramenta reproduzível e dois testes offline aprovados. Sem mudança de
produto, servidor ou acesso remoto. [Evidência](changes/otimizar-performance-app/validation/inventario-rotas-eventos-2026-10-20.md).

Consolidação documental em 13/10/2026. Datas abaixo indicam a rodada original, não execução nova.

## Evolução

Rodada posterior 13–14/10/2026: publicação autorizada de report/nove endpoints
administrativos; GETs de visitante/membro rejeitados; duas APIs de posts corrigidas
e publicadas para converter arquivo bruto em metadados. Corrigidos rascunho em
falha transitória e cancelamento com limpeza. 120 testes locais, compilação e 15
cenários de browser passaram; posts e blobs de teste removidos. Backup verificado
registrado no commit `f93287e` de 13/10 às 23h42, somente três arquivos. Admin/
desativado, e-mail completo e rotação TMDB permanecem pendentes. Essa entrega
complementa o histórico arquivado sem substituir suas evidências.

| Data | Entrega/verificação | Evidência e limites |
| --- | --- | --- |
| 17–18/09/2026 | Migração social inicial Xano, contas, perfis, mídias, interações, seguidores, posts, curtidas, comentários e listas | Modelo de dados 37/37; `.local/remote-results.json` lista 10 grupos de verificações reais; checklist e docs de retomada descrevem ownership e isolamento |
| 18–19/09/2026 | Posts com/sem mídia, mídia em listas distintas, persistência após login e lista com os quatro tipos | `docs/RETOMADA.md` e tasks originais; objetos temporários removidos/restaurados conforme os registros históricos |
| 19/09/2026 | Navegação pública, notas locais de visitante, trailers e otimizações de carga/curtidas | Fundação grupo 12; smoke histórico do Edge e 48 testes; 429 Xano tratado como recuperável |
| 22/09/2026 | Cadastro/login revalidados | 14 testes locais, 6 verificações Xano e compilação; relatório de autenticação não incluiu navegador nessa rodada |
| 22/09/2026 | Busca global, categorias independentes, capas/fallback e paginação | 54 testes e 7 verificações de navegador; relatório discovery |
| 22/09/2026 | Relevância por título e populares em grades verticais | 61 testes e smoke desktop/celular; comportamento de home substituído posteriormente |
| 23/09/2026 | Kitsu substitui consultas Jikan; mapeamento legado e deduplicação Xano | `docs/KITSU.md`; ranking 20, busca 4, Cowboy Bebop, 3 relacionados, 1 trailer; Naruto preserva identidade Jikan; 86 testes e navegador histórico |
| 23/09/2026 e checkpoint posterior | Home com fileiras horizontais, cinco coleções de livros/três de animes; pôster inteiro; streaming TMDB BR | `docs/CHECKPOINT_ATUAL.md`, catálogo, página e CSS atuais; não repetir a exigência antiga de home exclusivamente vertical |
| Até 26/09/2026 | Planejamento e implementação administrativa local | `docs/ADMIN_OPERATIONS.md`: dry-run reconheceu contratos; não comprova publicação administrativa |
| 27/09/2026 | `/admin/demo` com dados fictícios e sem escrita | `changes/gerenciamento-website/validation/local-demo-2026-09-27.md`; HTTP 200 e compilação históricos; não substitui integração real |
| 13/10/2026 | Reanálise local | 106 testes e compilação passaram; revisão documental, correção de contagem e arquivamento das duas entregas concluídas |
| 13/10/2026, após reanálise | Correções operacionais | Ignore/índice corrigidos preservando 434 arquivos existentes; `.venv` instalada; Unicode/URL de banner corrigidos; volume configurado; 113 testes e compilação passaram; teste Docker e tratamento de credenciais antigos pendentes |

## Mudanças arquivadas

- [Regra obrigatória OpenSpec](changes/archive/2026-10-21-exigir-openspec-para-implementacoes/tasks.md): 4/4; documentação de processo concluída em 21/10, sem delta funcional.
- [Revisão de merge e commits](changes/archive/2026-10-21-regularizar-merge-e-commits/tasks.md): 4/4; acompanhamento Git concluído em 21/10, sem alterar histórico.

- [Meias estrelas](changes/archive/2026-10-21-avaliar-meias-estrelas/tasks.md): 5/5; arquivada em 21/10, contrato media-interactions consolidado.
- [Correções operacionais](changes/archive/2026-10-21-corrigir-erros-operacionais/tasks.md): 7/7; arquivada em 21/10, contrato operational-reliability consolidado; Docker fora do escopo.
- [Listas iniciais](changes/archive/2026-10-21-padronizar-listas-iniciais/tasks.md): 7/7; arquivada em 21/10, contrato data-user-lists consolidado, preservando limites de validação da entrega.

- [Modelo Xano](changes/archive/2026-10-13-criar-modelo-dados-xano/tasks.md): 37 tarefas; sete capacidades de dados consolidadas em `specs/`.
- [Fundação](changes/archive/2026-10-13-definir-fundacao-codeboxd/tasks.md): 87 tarefas; nove capacidades funcionais consolidadas em `specs/`.
- [Administração ativa](changes/gerenciamento-website/tasks.md): 34 tarefas próprias, 17 concluídas e 17 abertas.

A busca de anime pendente na fundação referia-se à Jikan. A evidência Kitsu de 23/09 resolveu o objetivo de busca externa, sem exigir recuperar um provedor substituído. O item 11.7 estava escrito como `- []`, invisível à contagem do CLI; foi corrigido e encerrado após a validação documental. Antes da revisão o CLI mostrava 85/86, mas havia 87 IDs reais.

## Complementos anteriores à administração — H.1–H.7

Esses IDs foram retirados apenas do checklist administrativo; o conteúdo e os limites permanecem aqui.

| ID histórico | Trabalho registrado | Evidência disponível / limite |
| --- | --- | --- |
| H.1 | Solicitação de código de senha por e-mail, validação do código e atualização da senha | Estado de sessão e endpoints reset existentes; entrega real de e-mail não comprovada |
| H.2 | Pesquisa de obra dos quatro tipos no compositor do feed e seleção de resultado | Página/estado social existentes; não equivale a smoke completo atual |
| H.3 | Upload multipart de imagem do post, validação, prévia e leitura no feed | `services/uploads.py`, estado e contratos Xano; publicação real com imagem no navegador pendente |
| H.4 | Bloqueio de envio duplicado enquanto post é salvo | Trava `post_saving` no handler; suíte/compilação locais |
| H.5 | Ajustes visuais de pesquisa, upload, card e exclusão | CSS e diálogos; validação visual atual completa pendente |
| H.6 | Atualização de campo de imagem e POST/PUT de posts no workspace | Registro histórico relata publicação, dry-run sem delta e 68 arquivos analisados; não revalidado nesta revisão |
| H.7 | Compilação depois das mudanças do feed | Evidência histórica; compilação geral também passou em 13/10 |

## Decisões substituídas e mantidas

- **Substituída:** Jikan como fonte de consulta de anime → Kitsu; identidade Jikan permanece por compatibilidade.
- **Substituída:** home só com grades verticais → coleções horizontais empilhadas; busca/categorias continuam paginadas.
- **Mantida:** login é página; pop-up das referências foi descartado.
- **Mantida:** adaptadores rodam no Python; Xano guarda dados e aplica autorização.
- **Mantida:** catálogo legado `titulos` não é convertido automaticamente em `media`.
- **Mantida:** `/likes` ausente não cria consultas de discussão para todo o feed; compatibilidade sob demanda.
- **Mantida:** publicar hospedagem/domínio não é parte desta etapa.
- **Corrigida:** afirmação documental de Git protegido → `.gitignore` vazio verificado; proteção precisa ser implementada.

## Preservação das evidências

Saídas `.txt`, `.json` e scripts de validação foram preservados com a fundação arquivada. Não foram executados novamente nem tiveram resultados alterados. Relatórios de setembro são históricos: URLs locais, comportamento visual e comandos podem ter envelhecido.

Os scripts históricos possuem caminhos fixos: `auth_live.py` usa uma profundidade de diretório anterior ao arquivo; scripts de browser escrevem na antiga change ativa. Antes de reutilizá-los, adaptar uma cópia fora do arquivo para o diretório atual e uma nova pasta de resultados. Não sobrescrever evidências arquivadas. O teste de autenticação real cria conta; não executá-lo apenas para validar documentação.

Resultados `.local/` são auxiliares e podem conter dados privados. Somente resumos sem segredos foram incorporados. Ausência desses arquivos em outra máquina não invalida o registro histórico, mas limita sua reprodução; consultar o relatório arquivado e revalidar quando necessário.

## Decisão posterior — sem Docker

Em 13/10/2026, o usuário solicitou manter o projeto sem Docker. Os ajustes Docker desta rodada foram revertidos e o Desktop iniciado para diagnóstico foi encerrado. Nenhum contêiner/volume foi criado. A execução permanece local com `.venv`; 3.1/3.2 saíram do escopo operacional, preservados no histórico, deixando 7/7 tarefas próprias concluídas. Permanecem as correções Git, dependências e uploads, verificadas em 113 testes e compilação.
