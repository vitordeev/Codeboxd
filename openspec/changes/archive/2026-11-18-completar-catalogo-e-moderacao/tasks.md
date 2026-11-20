## 1. Diagnostico e preenchimento do catalogo

- [x] 1.1 Confirmar no estado/UI/API o `per_page`, total e quantidade efetivamente renderizada em series/animes; reproduzir com fixtures de 5, 35 e total 0.
- [x] 1.2 Complementar series, animes e livros com resultados externos de leitura ate 35, sem rotulos de cadastro, edicao ou gravacao.
- [x] 1.3 Cobrir identidade repetida, poucas respostas e falha parcial de provedor; confirmar ausencia de chamadas de escrita para resultados externos.
- [x] 1.4 Preparar preflight local do bundle Xano de moderacao; nao publicar nem afirmar aceite remoto.

## 2. Remocao moderada de alvos

- [x] 2.1 Adicionar confirmacao e justificativa nos reports de post/obra/comentario/avaliacao; verificar que mensagem/perfil nao mostram remocao.
- [x] 2.2 Expandir contrato Xano admin para validar sessao, report pendente/em analise, tipo/alvo, justificativa e auditoria transacional para post/obra/comentario/avaliacao; testar rejeicoes sem mutacao.
- [x] 2.3 Remover post e comentarios/likes associados preservando report/snapshot e encaminhar asset para a rotina de limpeza; testar cascade e auditoria.
- [x] 2.4 Adicionar flag de ocultacao de media, filtrar catalogo/selecoes publicas e bloquear novas referencias sem remover historico; testar leitura, interacao, lista e associacao de post.
- [x] 2.5 Testar concorrencia/repeticao e falha parcial da remocao; confirmar que report e evento de auditoria ficam consistentes.

## 2.6 Tipos adicionais de moderacao

- [x] 2.6 Adicionar report de avaliacao no perfil publico e validar snapshot seguro da interacao.
- [x] 2.7 Remover apenas comentario reportado ou limpar nota/critica/spoiler mantendo status da biblioteca; cobrir cada tipo com testes.
- [x] 2.8 Expor acao e dialogo com rotulo especifico para obra, comentario e avaliacao; ocultar acao para mensagem/perfil.

## 3. Validacao e integracao

- [x] 3.1 Executar testes direcionados, `reflex compile --dry`, `git diff --check` e `openspec validate completar-catalogo-e-moderacao --type change`; registrar resultados.
- [ ] 3.2 Validar no navegador os fluxos de confirmacao/cancelamento e feedback para post/obra/comentario/avaliacao; registrar tamanhos e estados.
- [x] 3.3 Documentar hashes/escopo Xano local e manter publicacao, importacao/remocao remota e aceite integrado pendentes enquanto nao houver workspace acessivel.


## Local evidence (2026-11-18)

- Tasks 1.1-1.4: catalog displays up to 35, combining persisted rows with read-only TMDB/Kitsu/Open Library results; no registration badge or import action. Results are deduplicated and never written.
- Tasks 2.1-2.8: report actions require a reason and match post/media/comment/review targets; message/profile reports have no remove action. Review reports capture a safe snapshot; comment deletion leaves the parent post intact; review moderation preserves library status. Local contract checks cover admin/session validation, post cascade and image cleanup queue, soft-hidden media filters, report snapshot/audit, and repeated/finalized report rejection.
- Task 3.1: 13 targeted tests passed; Reflex `--dry` compile succeeded; both OpenSpec changes validated; `git diff --check` passed with only line-ending normalization warnings.
- Task 3.3: Xano file hashes and scope are in `xano-preflight.json`. No remote contract was published, no records were imported/removed remotely, and no Xano integrated acceptance is claimed.
- Task 3.2 remains open: browser desktop/mobile flows were not run in this session.
