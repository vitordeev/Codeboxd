# Tasks

> **Cancelada em 18/11/2026 a pedido do usuario.** Os 11 itens marcados abaixo
> registram entregas historicas e evidencias produzidas durante a change, mas a
> implementacao visual foi revertida ao baseline anterior. Os 15 itens abertos
> permanecem incompletos. Nenhum delta foi sincronizado; a reformulacao futura
> deve comecar em uma nova change apos definicao das referencias do usuario.
> Relatorio: `cancelamento-2026-11-18.md`.

O planejamento foi aprovado pelo pedido posterior de prosseguimento do usuário.
O primeiro lote local concluiu 1.1, 2.1 e 3.1: **3/26 tarefas**. A aprovação
do planejamento não é autorização de publicação Xano, mutações
reais ou merge. Referências e diagnóstico estão em design.md; critérios de
comportamento estão em specs/. Cada lote deve incluir seus testes e evidências.

## 1. Recorte aprovado e baseline

- [x] 1.1 Após aprovação das duas changes, registrar baseline atual das páginas e componentes afetados em 320/390/768/1024/1440px com dados controlados e inventário de ações/rotas; identificar fonte/viewport/estado de cada captura e preservar a worktree de performance.
- [ ] 1.2 Revisar com o usuário a proposta de shell, densidade e ações a condensar, usando somente referências locais; registrar decisões de manter/mover/condensar e provar alternativa funcional/acessível antes de qualquer retirada. Decisões de 14/11 registradas em `design.md`: shell aprovado, densidade atual da Home mantida e condensação conservadora. A tarefa permanece aberta até que qualquer alternativa a controles retirados seja comprovada funcional e acessível; nenhum controle ou rota foi removido nesta revisão.

## 2. Fundamentos e navegação — sem mudança de negócio

- [x] 2.1 Consolidar tokens de cores, tipografia, espaços e raios a partir da identidade ativa, com uma página piloto; medir contraste nos fundos reais, verificar Inter/fallback e preservar logo/mascotes, registrando antes/depois sem introduzir arte ou fontes novas.
- [x] 2.2 Modernizar variantes reutilizáveis de botão/campo/feedback/vazio/diálogo, mantendo mensagens e dados recuperáveis; verificar nomes acessíveis, foco/retorno, colagem, loading/erro/vazio/falha parcial e registrar regressões da família piloto. Campos rotulados e estados semânticos existentes foram mantidos; avatar sem foto agora tem nome acessível e ícone decorativo oculto. Focus manager local garante entrada e retorno de foco sem eventos Reflex; **758 testes, 8/8 cenários de navegador em 1440/390 px, compilação Reflex e py_compile aprovados**, com colagem verificada na fixture. Evidências: `validation/avatar-fallback-acessivel-2026-11-18.md` e `validation/dialogos-acessiveis-2026-11-18.md`.
- [x] 2.3 Reorganizar shell e acesso a Biblioteca/conta/listas/comunidade mantendo rotas antigas e guards; testar teclado, menu sem hover, foco não encoberto e navegação desktop/celular, documentando o mapa e que não há chamadas extras por apresentação. Após revisão do usuário em 18/11, a navegação mantém Início/Feed/Biblioteca e remove Buscar; fixture aprovou teclado, foco visível na viewport e zero chamadas extras em 1440/390 px, 10/10 casos e zero erros JS. Ver `validation/rotas-antigas-2026-11-18.md`.

## 3. Coleções horizontais reutilizáveis

- [x] 3.1 Evoluir a prateleira existente com arrasto primário por intenção/limiar, supressão só do clique pós-arrasto e cancelamento/cleanup; testar clique normal, seleção, saída de trilho, rerender e ausência de listeners duplicados, documentando parâmetros.
- [ ] 3.2 Integrar toque/trackpad nativos, setas e teclado no mesmo componente; validar swipe horizontal, scroll vertical, zoom, Home/End, Tab/Enter, extremos e movimento reduzido em desktop e dispositivo touch, registrando evidência e zero chamadas por gesto.
- [x] 3.3 Aplicar o componente à Home e recomendações sem mudar paginação/identidade/caches; testar carregar mais separado de scroll, foco em card oculto, falha de capa e layouts 320/390/768/1440, comparando DOM/requests com o baseline da mesma coleção. Fixture isolada: 14 prateleiras/168 cards iniciais em cinco larguras; gestos sem tráfego/eventos; carregamento explícito de 12 para 24 itens sem substituir/duplicar os iniciais; foco oculto e fallback 404 aprovados. Evidência: `validation/colecoes-home-recomendacoes-2026-11-16.md`.

## 4. Busca e contexto no frontend — fixtures primeiro

- [x] 4.1 Remover a rota e a aba novas `/buscar`; preservar o campo de busca de obras existente na Home (`/`) sem duplicar a entrada. Tabela de rotas Reflex compilada confirma a ausência de `/buscar`; Home e busca atual preservadas. Evidência: `validation/rotas-antigas-2026-11-18.md`.
- [x] 4.2 Preparar apresentação paginada de perfis e listas com autoria, vazio/erro/429 e estado por escopo; testar respostas atrasadas/troca de conta, nomes longos e falha parcial com fixtures sem dados privados, documentando as consultas necessárias e ausência de N+1. Testes locais de estado cobrem resposta atrasada, troca de escopo/conta, cooldown e projeção sem fanout; browser fixture aprovou nomes longos, recuperação parcial e 429 nos dois escopos. **12 + 13 + 7 testes e 11 casos de navegador aprovados.** Consultas e limites registrados em `validation/busca-listas-frontend-2026-11-16.md`; sem validação Xano real.
- [x] 4.3 Manter a visualização/gerenciamento de listas dentro da rota existente `/listas`; remover `/lista` e seus links novos sem quebrar a abertura de uma lista pelo diretório. Rota Reflex compilada não contém `/lista`; fixture abriu e gerenciou lista pela página antiga em desktop/celular. Evidência: `validation/rotas-antigas-2026-11-18.md`.

## 5. Contratos de busca/listas no Xano — lote independente

- [ ] 5.1 Preparar extensões aditivas paginadas de `/profiles` e `/lists/public` com q/criador/descrição explícita, projeção pública e ordenação estável; testar compatibilidade com array atual, termos/coringas escapados, limites e filtragem antes de contagem/paginação, documentando índices e exemplos sanitizados.
- [x] 5.2 Preparar consultas de detalhe público e próprio autenticado, reutilizando itens existentes; testar visitante/dono/outra conta/desativado, ID inexistente vs privado, itens e totais sem vazamento e mudança pública→privada/cache, registrando requisitos de autorização por endpoint. Contratos XanoScript locais e estado Reflex cobrem detalhe público/privado, proprietário/outra conta, sessão e mudança de visibilidade; regressão adicionada nesta rodada garante que os três endpoints autenticados rejeitam conta desativada antes de ler a lista. **13 testes locais aprovados**; cobertura de navegador fixture e limites documentados em `validation/busca-listas-frontend-2026-11-16.md`. Nenhum contrato foi publicado/validado remotamente (tarefas 5.3–5.4).
- [ ] 5.3 No workspace atual identificado, com backup/prévia revisados e autorização do lote, publicar somente contratos aprovados e verificar estrutura/permissões/projeções por leitura independente; manter aberta sem evidência ou aprovação do lote. Não requer workspace novo e não copia dados reais como fixtures.
- [ ] 5.4 Após aprovação do lote de fixtures no workspace atual, executar aceite integrado de busca/paginação/detalhe/privacidade com visitante e duas contas descartáveis, incluindo links antigos e públicos expirados por privacidade; registrar API/navegador/limpeza e preservação de dados anteriores separadamente e só então liberar a experiência. Falhas induzidas permanecem locais.

## 6. Propagação incremental por família

- [ ] 6.1 Revisar Home/catálogo e suas mensagens/hero/CTAs com os tokens e prateleiras aprovados; validar foco, dobra inicial, títulos longos, grid/resultados e falhas parciais sem alterar o carregamento P0, registrando capturas comparáveis.
- [ ] 6.2 Modernizar ficha compartilhada e avaliações nos quatro tipos sem confundir nota/progresso/listas, preservando seletor acessível e spoilers; testar identidade externa/Jikan, complementos lentos, nota decimal e cliques de lista, com evidência por tipo e largura.
- [ ] 6.3 Ajustar biblioteca e Minhas listas, conservando diretório público agrupado e gerenciamento; testar filtros/itens/paginação/privacidade já existentes e links novos, registrando redundâncias condensadas e alternativas preservadas.
- [ ] 6.4 Ajustar perfil, conexões e diálogo de edição com feedback por campo; verificar nome/bio/banner/avatar longos, autoria/seguir/denunciar e foco, sem migrar storage de avatar/banner, registrando capturas desktop/celular.
- [ ] 6.5 Modernizar login/cadastro/recuperação usando composição e mascotes ativos; testar rotas, rótulos/autocomplete/colagem/mostrar senha, etapas e erros com fixtures sem alterar contratos de autenticação ou envio, registrando contraste e navegação.
- [ ] 6.6 Refinar apresentação do feed/compositor/discussão preservando foto principal, obra compacta, likes e comentários sob demanda; testar rascunho, erro, teclado e não duplicação de ações; anexos externos só usam contrato validado da change Cloudinary, sem antecipar ativação.
- [x] 6.7 Investigar em cenário autorizado a origem da atividade de criação de listas relatada no feed, comparando com os contratos locais; registrar prova ou ausência de reprodução e apresentar recomendação específica antes de alterar eventos. Não criar autopost nem remover dados/handlers por hipótese. Cenário sintético local criou lista em `/listas`, confirmou uma chamada `POST /lists`, zero `POST /posts` e feed sem post novo em 1440/390 px. Contrato Xano local grava apenas `user_list`; `/feed` consulta apenas `post`. **10/10 cenários browser do harness passaram, zero erros JS.** Recomendação: não alterar eventos/feed sem evidência reproduzível em conta autorizada. Ver `validation/origem-atividade-criacao-lista-2026-11-18.md`.
- [ ] 6.8 Aplicar somente padrões visuais aprovados à administração e demonstração, sem mudar permissões/regras; testar sidebar, tabelas/filtros/paginação/confirmações e dados indisponíveis em 390/1440px, documentando que isso não conclui 9.2 de gerenciamento-website.

## 7. Aceite transversal e liberação gradual

- [ ] 7.1 Executar matriz WCAG aplicável com teclado/leitor de tela, contraste medido, zoom/reflow, foco/diálogos, alvos e movimento reduzido nas famílias alteradas; combinar checks automatizados com verificação manual em 320/390/768/1024/1440 e registrar limitações sem alegar conformidade pelo teste isolado.
- [ ] 7.2 Comparar jornadas com baseline equivalente e cinco pares de medidas por cenário relevante: DOM/bytes/requests/tempos, gesto com zero tráfego e consulta só do escopo ativo; preservar metas da change performance e resolver regressões antes de aceite, sem teste de carga em serviços reais.
- [ ] 7.3 Revisar navegação integrada, compatibilidade de rotas/privacidade, diff, testes pertinentes, compile Reflex e rollback de cada lote; validar OpenSpec e apresentar evidências para autorização de liberação, sem push/merge/arquivo automáticos.

## Workflow follow-up

- 17/11/2026 — Incremento local de 5.1: parâmetros e paginação de busca nos GETs de perfis/listas, projeção pública e três addons de autoria/contagem. Seis testes novos e suíte completa 675/675 aprovados; dry-run Xano limitado aprovado (3 addons, 2 endpoints), sem publicação. Ranking, plano de índices/custo e execução integrada ainda pendentes; 5.1 permanece aberta. Ver [contratos de busca](validation/contratos-busca-2026-11-17.md) e [plano geral](../archive/2026-11-17-finalizar-projeto-2026-11-17/relatorio.md).

- Revisão documental de 14/11/2026 registrada em `design.md`; `openspec validate modernizar-ui-ux-codeboxd --type change` e `git diff --check` aprovados. Sem testes de aplicação, pois não houve alteração de interface. A tarefa 1.2 permanece aberta até que alternativas funcionais e acessíveis sejam comprovadas antes de retirar controles.
- Aprovação de planejamento e prosseguimento recebida; o primeiro lote foi implementado apenas localmente, em branch/worktree própria.
- Evidências do lote: [fundamentos e carrosséis, 11/11/2026](validation/fundamentos-carrosseis-2026-11-11.md), baseline de 15 capturas, 20 cenários de navegador e cinco verificações adicionais da Inter existente. A suíte local e o compile estão discriminados nesse relatório.
- 3.2 segue aberta: toque emulado não substitui dispositivo físico. 3.3 tem o componente aplicado, mas ainda exige aceite de carregar mais/falha de capa e comparação específica de carregamento. 2.2/2.3 e os demais itens não foram concluídos por este lote.
- Planejamento completo e testes do piloto não significam aceite de toda a interface.
- Não sincronizar specs nem arquivar sem critérios e autorização próprios.
- 15/11/2026 — Busca unificada local: 4/26 tarefas concluídas. `/buscar` passou em oito testes de estado, seis cenários de navegador com fixtures e compile Reflex; atualização de fixture preservou logs anteriores em `.local`. A tarefa 4.1 foi concluída; 4.2 e 4.3 seguem abertas até cobrir os critérios restantes de falhas/nomes longos e detalhe endereçável. Contratos Xano permanecem apenas locais, sem publicação ou validação integrada.
- 16/11/2026 — Retomada da tarefa 3.2 (ID 7): os hashes normalizados de `horizontal_collection.py`, `horizontal-collections.js` e harness/fixture correspondem exatamente à evidência do lote validado em cinco larguras. A implementação e os testes em toque emulado já estão registrados; não foram reexecutados nesta retomada. O aceite em hardware touch físico continua indisponível e 3.2 permanece aberta.
- 16/11/2026 — Tarefa 3.3 concluída localmente: fixture/browser passou em 20 casos, cinco viewports, falha de capa e paginação explícita 12→24; testes de discovery/performance e compile Reflex também passaram. Evidência: `validation/colecoes-home-recomendacoes-2026-11-16.md`; resultado completo privado em `.local/ui-task-3-3-20261116-final/result.json`. Touch físico segue fora do aceite da 3.3 e pendente em 3.2.
