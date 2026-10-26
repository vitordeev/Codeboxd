# Relatório do estado do Codeboxd

Meias estrelas em 19/10: 0,5–5 com preenchimento parcial, notas em vírgula e
restauração decimal de visitante/conta. 148 testes e compilação aprovados; nove
checks de browser/Xano real confirmaram persistência 1,5 e preservação da crítica.
Avaliação de teste removida. [Evidência](changes/archive/2026-10-21-avaliar-meias-estrelas/validation/implementacao-2026-10-19.md).

Denúncia de obras em 19/10: retorno no modal e tratamento de 429 corrigidos;
obra externa recebe ID ao enviar. 143 testes/compilação aprovados; denúncia de
teste persistida no Xano e sucesso confirmado no browser, com limpeza. Limitação
429 testada por simulação. [Evidência](changes/gerenciamento-website/validation/denunciar-obras-2026-10-19.md).

Tradução opcional DeepL em 19/10: fichas anime/livro integradas localmente com
cache persistente, fallback e chave privada; 136 testes locais e smoke DeepL real
passaram. Revisão de navegador ainda aberta. [Evidência](changes/archive/2026-10-21-traduzir-descricoes-deepl/validation/implementacao-2026-10-19.md).

Atualização de 19/10/2026: correções dos três GETs administrativos publicadas;
backup estrutural de 77 documentos e dry-run posterior sem delta. 18 testes
locais passaram; visitante/membro rejeitados nos endpoints reais. Faltam testes
funcionais com admin aprovado e navegador; contagem administrativa mantida em
17/34. [Evidência](changes/gerenciamento-website/validation/publicacao-buscas-admin-2026-10-19.md).

Base inicial: 13/10/2026, código/documentação e evidências históricas. Atualização de encerramento: 14/10/2026, com nova publicação Xano, testes remotos de visitante/membro e recuperação inválida, e validação de imagem no navegador. Evidências e limites estão nas rodadas abaixo.

## Avaliação geral

Recuperação de senha por seis dígitos (pedido posterior em 14/10): contratos
publicados; 127 testes locais, compilação, 22 cenários Xano e sete de browser
passaram. Prazo, tentativas, reenvio, consumo concorrente e troca/restauração de
senha comprovados na conta de teste. Chegada do e-mail em caixa real controlada
continua pendente. [Evidência](changes/recuperar-senha-codigo-6-digitos/validation/implementacao-2026-10-14.md).

Encerramento em 14/10: P.5 validada no navegador em 15 cenários com criação,
recarga, edição e cancelamento de imagem; posts, arquivos temporários e blobs
remotos de teste limpos. 120 testes locais e compilação aprovados. Contratos
publicados de admin/posts ficaram sincronizados no dry-run final. O commit
`f93287e` de 13/10 registra apenas backup/testes/evidência; demais alterações
continuam locais. [Resultado completo P.5](validation/uploads-and-session-2026-10-13.md).

Rodada mais recente: [administração publicada](changes/gerenciamento-website/validation/publicacao-admin-2026-10-13.md), com tabela report/nove endpoints sincronizados e rejeição de visitante/membro nos GETs. Admin/desativado e mutações permanecem pendentes. Backup local verificado foi registrado no commit `f93287e`; upload e rascunho receberam correções acompanhadas em [P.5](validation/uploads-and-session-2026-10-13.md). Suíte atual: 120 testes locais aprovados, compilação e pip check aprovados; fluxo de recuperação inválido verificado remotamente. Entrega de e-mail e rotação TMDB não concluídas.

Retomada posterior nesta data: autorização local administrativa e busca de usuários corrigidas; dry-run limitado passou, mas quatro GETs administrativos reais retornaram 404. Nenhum endpoint foi publicado nesta rodada. [Evidência atual](changes/gerenciamento-website/validation/retomada-admin-2026-10-13.md); 113 testes locais passaram novamente, sem nova validação autenticada ou navegador.

A fundação funcional e o modelo de dados estão concluídos no escopo original. A administração tem telas, estados e contratos locais, mas ainda precisa de validação real. As correções locais de Git, ambiente, mensagens e URL de banner foram aplicadas; Docker foi retirado do escopo pelo usuário; a execução permanece local. A prontidão para publicação ainda não foi comprovada.

| Entrega | Situação | Tarefas |
| --- | --- | --- |
| Fundação do produto | Concluída e arquivada | 87/87 |
| Modelo de dados Xano | Concluído e arquivado | 37/37 |
| Administração | Em andamento | 17/34 concluídas; 17 abertas |
| Correções operacionais | Concluídas no escopo local, sem Docker | 7/7 |

Contagens medem os checklists de seus respectivos escopos, não uma porcentagem geral de prontidão do produto. Correções transversais e complementos posteriores são acompanhados separadamente.

## O que está pronto no escopo original

| Área | Entregue | Evidência/limite |
| --- | --- | --- |
| Estrutura | Aplicação Reflex, rotas, estados, serviços e estilos | Compilação atual aprovada |
| Conta | Cadastro, login, logout, identidade verificada e bloqueio de ações sem autenticação | Testes locais e integrações históricas Xano; redefinição de senha é complemento ainda pendente de teste completo |
| Catálogo | Filmes/séries TMDB, animes Kitsu e livros Open Library; identidade e normalização | APIs e navegador verificados historicamente; disponibilidade atual não retestada |
| Descoberta | Busca global, categorias independentes, relevância por título, paginação e falhas parciais | Testes locais e smoke histórico |
| Home e ficha | Coleções por tipo, capas/fallback, metadados, trailers e relacionados quando disponíveis | Implementação atual e evidências históricas; campos dependem da fonte |
| Visitantes | Navegação pública e nota pessoal somente no navegador | Sem publicação de nota de visitante no Xano |
| Biblioteca | Status de consumo, notas, reviews e isolamento por conta | Testes locais e persistência histórica após novo login |
| Perfis | Perfil público, edição própria, atividades e estatísticas | Ownership e privacidade verificados historicamente; persistência operacional de banner precisa de ajuste |
| Social | Seguir/deixar de seguir, feed dos seguidos, posts, curtidas e comentários | Evidência histórica de autoria, unicidade e exclusões; `/likes` depende do fallback documentado |
| Listas | Criar/editar/excluir, visibilidade pública/privada e itens dos quatro tipos sem duplicação | Mesma mídia em listas diferentes e ownership verificados historicamente |
| Dados | Usuários, perfis, mídias, interações, seguidores, posts, curtidas, comentários e listas | Migração inicial Xano concluída; reports administrativos pertencem à change ativa |
| OpenSpec | Índice, contexto, histórico, pendências, contratos e arquivos de entregas concluídas | 16 specs consolidadas; validações estritas aprovadas |

## Implementado, mas ainda não concluído operacionalmente

| Área | O que já existe | O que falta |
| --- | --- | --- |
| Login administrativo | Formulário dedicado e verificação do papel admin | Smoke atual no navegador e autorização direta nos endpoints |
| Dashboard | Indicadores, atividade, pendências e tratamento de falhas | Conferir contagens e respostas com dados reais |
| Usuários | Busca, filtros, paginação, confirmação de suspensão/reativação | Testar conta suspensa usando operações protegidas e conferir auditoria persistida |
| Catálogo administrativo | Seções por tipo, cadastro sem duplicata e correção de campos | Validar paginação, filtros e preservação de identidade no Xano real |
| Denúncias | Modelo report, snapshots, fila, decisão e auditoria locais | Comprovar publicação/persistência, autorização, transições e conteúdo alvo intacto |
| Interface administrativa | Navegação, componentes e CSS responsivo | Validar estados vazios/erros e telas desktop/celular com dados reais |
| Imagem em post | Multipart convertido em metadados, prévia, rascunho preservado e cancelamento com limpeza | Fluxo validado no navegador nesta rodada; evidência em P.5 |
| Redefinição de senha | Solicitar código, validar e alterar senha | Confirmar entrega de e-mail e fluxo completo com conta controlada |
| Publicação | Preparação histórica preservada, fora do escopo atual | Escolher e validar solução somente quando solicitada; sem Docker nesta etapa |

Os contratos administrativos locais e o dry-run histórico não comprovam publicação remota. A rota `/admin/demo` usa dados fictícios e não substitui os testes reais.

## Correções e organização ainda necessárias

1. **Credenciais antigas:** ignore e índice corrigidos; 441 entradas retiradas sem apagar arquivos locais. O histórico contém `.env` e arquivos de contas em commit incluído na referência `origin/main`; revisar/rotacionar credenciais e tratar contas de teste.
2. **Banners em produção:** URL concreta corrigida/testada; arquivos permanecem no diretório local. Backup e eventual migração serão tratados quando houver hospedagem; Docker excluído desta etapa.
3. **Ambiente corrigido:** `.venv` canônica instalada, dependências diretas fixadas e pip check aprovado; `venv` anterior preservada.
4. **Mensagens de upload corrigidas:** rede, HTTP e resposta inválida verificadas por testes controlados.
5. **Curtidas:** revalidar a ausência remota de `/likes` e decidir manter compatibilidade ou publicar a rota após revisão.
6. **Documentos externos:** checkpoints atuais reconciliados e direcionados ao OpenSpec; evidências históricas preservadas.
7. **Scripts históricos:** adaptar cópias antes de reutilizar caminhos/portas antigos, preservando as evidências arquivadas.

Separação dos estados/páginas sociais é uma melhoria conforme crescimento, sem impedir o encerramento do escopo já entregue. Chat, notificações e recomendações por aprendizado de máquina estão fora do escopo atual, não são funcionalidades prometidas como prontas.

## Qualidade verificada

- 127 testes locais passaram e o Reflex compilou no `.venv` após a atualização da recuperação por seis dígitos.
- A configuração Compose chegou a ser verificada, mas os ajustes foram revertidos após o usuário decidir continuar sem Docker; nenhum teste de contêiner foi executado.
- OpenSpec mantém 16 specs consolidadas, três changes não arquivadas (duas em andamento e uma concluída) e duas arquivadas; recuperação tem 6/7 tarefas verificadas, aguardando chegada real do e-mail.
- IDs de tarefas preservados; resultados/scripts históricos mantidos byte a byte.
- Essas verificações não garantem disponibilidade contínua de APIs nem integração administrativa completa.

## Próxima sequência recomendada

Tratar credenciais presentes no histórico e validar autorização administrativa diretamente no Xano, dashboard, usuários, catálogo e reports. Concluir revisão de interface, imagem de post e redefinição de senha. A execução permanece local com `.venv`. Hospedagem e eventual migração de arquivos exigem uma etapa futura solicitada pelo usuário.

Correções executadas: [relatório operacional](changes/archive/2026-10-21-corrigir-erros-operacionais/validation/correcoes-2026-10-13.md). Comandos de setup: [AMBIENTE.md](AMBIENTE.md).

Detalhamento por tarefa: [administração](changes/gerenciamento-website/tasks.md) e [matriz de evidências](changes/gerenciamento-website/validation/revisao-2026-10-13.md). Pendências transversais: [PENDENCIAS.md](PENDENCIAS.md). Datas e limites das verificações: [VALIDACAO.md](VALIDACAO.md) e [HISTORICO.md](HISTORICO.md).
