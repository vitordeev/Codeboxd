## 1. Navegação do dashboard e usuários

- [x] 1.1 Fazer os indicadores de usuários, catálogo e reports abrirem as áreas existentes; manter publicações sem link. Verificar destinos, filtro inicial de reports pendentes e ausência de nova rota de publicações.
- [x] 1.2 Permitir que `/admin/users` carregue a primeira página com busca vazia e pagine sem termo. Verificar lista, vazio, filtros, busca existente, paginação e resposta de acesso negado com fixtures.

## 2. Identidade da pessoa administradora

- [x] 2.1 Criar contrato local mínimo e protegido para dados de cabeçalho (nome, username, avatar e cargo), usando perfil do usuário autenticado e validando sessão ativa/role admin; verificar projeção sem dados privados e rejeição de visitante/membro.
- [x] 2.2 Integrar o avatar circular e menu de identidade nos cabeçalhos administrativos, com acessibilidade por teclado, fallback sem foto/perfil, invalidação ao sair/trocar sessão e cargo vindo da sessão verificada; cobrir com testes de estado/componentes.

## 3. Paginação do catálogo

- [x] 3.1 Solicitar 35 itens por página para filmes, séries e animes e manter livros em 25; verificar parâmetro, busca, ordenação e navegação de páginas com mais de 35 resultados.
- [x] 3.2 Confirmar estados com menos de 35, zero e falha/429 sem semear ou importar obras; validar contagens exibidas com fixtures locais.

## 4. Segurança e comportamento de reports

- [x] 4.1 Adicionar testes de regressão para `POST /reports` e `PUT /admin/reports/{id}` mostrando que criar/enviar/revisar report não apaga, oculta ou edita o alvo e que a decisão/auditoria é preservada.
- [x] 4.2 Conferir cada tipo de alvo suportado (comentário, publicação e obra, além dos demais tipos já existentes) em testes locais/contratos; manter aberta qualquer verificação remota não executada.

## 5. Integração e evidências

- [x] 5.1 Validar fluxos locais em navegador desktop e celular: destinos dos cards, listagem sem busca, menu do administrador com/sem avatar, catálogo de 35 por tipo e fila de reports; registrar fixtures, chamadas e limitações.
- [x] 5.2 Executar testes pertinentes, `reflex compile --dry`, `git diff --check` e `openspec validate melhorar-painel-administrativo --type change`; revisar o diff para confirmar que ficou restrito ao painel e não incorporou trabalho de colegas.
- [x] 5.3 Preparar prévia Xano restrita para o endpoint de identidade e documentar hashes/escopo sem publicar. Manter qualquer mutação/publicação/aceite integrado pendente até autorização específica e registrar separadamente a validação remota se autorizada.



## Local implementation evidence (2026-11-18)

- Tasks 1.1-4.2: dashboard destinations, initial users page and blank-search pagination, protected identity contract, 35-item movie/series/anime pages and 25-item book pages implemented. Local report contract regressions cover all five target types, report snapshots, status/audit updates and no target deletion or editing. Tests: `.venv\Scripts\python.exe -m unittest tests.test_admin tests.test_admin_report_contracts` (29 passed).
- Task 5.2: `.venv\Scripts\python.exe -m reflex compile --dry`, `git diff --check` and `openspec validate melhorar-painel-administrativo --type change` passed. Diff review stayed within the admin panel, its styles/tests and local Xano endpoint.
- Task 5.3: local Xano endpoint preflight and SHA-256 scope record are in `xano-identity-preflight.json`. No remote publish or acceptance was performed.
- Task 5.1 remains open: desktop/mobile browser validation has not been run.
- Live catalog counts and integrated identity behavior remain unverified because the Xano workspace is not available.

- User acceptance for task 5.1: user reports their browser validation is complete and everything is correct (2026-11-18). This is recorded as user-reported validation; no independent browser capture was produced.
