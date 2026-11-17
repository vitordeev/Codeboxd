# Tasks

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
- [ ] 2.2 Modernizar variantes reutilizáveis de botão/campo/feedback/vazio/diálogo, mantendo mensagens e dados recuperáveis; verificar nomes acessíveis, foco/retorno, colagem, loading/erro/vazio/falha parcial e registrar regressões da família piloto. Implementação local de campos rotulados, feedback/empty states e fechamento de diálogo; cinco testes novos, 38 regressões sociais e compile Reflex aprovados. Verificação de foco/retorno e colagem no navegador ainda pendente.
- [ ] 2.3 Reorganizar shell e acesso a Buscar/Biblioteca/conta/listas/comunidade mantendo rotas antigas e guards; testar teclado, menu sem hover, foco não encoberto e navegação desktop/celular, documentando o mapa atual→novo e que não há chamadas extras por apresentação. Shell agora expõe Início/Buscar/Feed/Biblioteca e menu nativo expansível para conta/listas/comunidade/admin guardado; rotas/links antigos preservados. Testes estruturais e compile Reflex aprovados; navegação por teclado, foco e viewports reais pendentes.

## 3. Coleções horizontais reutilizáveis

- [x] 3.1 Evoluir a prateleira existente com arrasto primário por intenção/limiar, supressão só do clique pós-arrasto e cancelamento/cleanup; testar clique normal, seleção, saída de trilho, rerender e ausência de listeners duplicados, documentando parâmetros.
- [ ] 3.2 Integrar toque/trackpad nativos, setas e teclado no mesmo componente; validar swipe horizontal, scroll vertical, zoom, Home/End, Tab/Enter, extremos e movimento reduzido em desktop e dispositivo touch, registrando evidência e zero chamadas por gesto.
- [x] 3.3 Aplicar o componente à Home e recomendações sem mudar paginação/identidade/caches; testar carregar mais separado de scroll, foco em card oculto, falha de capa e layouts 320/390/768/1440, comparando DOM/requests com o baseline da mesma coleção. Fixture isolada: 14 prateleiras/168 cards iniciais em cinco larguras; gestos sem tráfego/eventos; carregamento explícito de 12 para 24 itens sem substituir/duplicar os iniciais; foco oculto e fallback 404 aprovados. Evidência: `validation/colecoes-home-recomendacoes-2026-11-16.md`.

## 4. Busca e contexto no frontend — fixtures primeiro

- [x] 4.1 Criar a entrada `/buscar` com escopos Obras/Pessoas/Listas públicas e query/filtros/página na URL, reutilizando a busca multiformato atual; testar recarga/voltar, categorias separadas, texto não submetido e nenhuma consulta de todos os domínios por tecla, registrando contratos. Implementação local: busca multiformato no escopo Obras, perfis/listas com chamadas separadas e filtros/consulta/página na URL. Oito testes de estado e seis cenários de navegador com fixture fictícia passaram; recarga, histórico, paginação e ausência de consulta ao digitar confirmados. Sem chamadas reais ou publicação Xano.
- [x] 4.2 Preparar apresentação paginada de perfis e listas com autoria, vazio/erro/429 e estado por escopo; testar respostas atrasadas/troca de conta, nomes longos e falha parcial com fixtures sem dados privados, documentando as consultas necessárias e ausência de N+1. Testes locais de estado cobrem resposta atrasada, troca de escopo/conta, cooldown e projeção sem fanout; browser fixture aprovou nomes longos, recuperação parcial e 429 nos dois escopos. **12 + 13 + 7 testes e 11 casos de navegador aprovados.** Consultas e limites registrados em `validation/busca-listas-frontend-2026-11-16.md`; sem validação Xano real.
- [x] 4.3 Preparar detalhe endereçável de lista, links ao criador/obras, fallback de copiar link e gerenciamento do dono; testar abertura fora da página do diretório, paginação/zero itens, contexto pessoal privado e perda de acesso após mudar visibilidade, registrando os casos que dependem de Xano real. Browser fixture aprovou detalhe direto, paginação, lista vazia, links de obras e fallback de clipboard; testes locais cobrem contexto do proprietário, outra conta, sessão/visibilidade alterada e resposta obsoleta. **32 testes direcionados e 11 casos de navegador aprovados.** Contratos XanoScript foram inspecionados/testados localmente, não publicados nem verificados remotamente; dependências reais registradas em `validation/busca-listas-frontend-2026-11-16.md` e permanecem nas tarefas 5.2–5.4.

## 5. Contratos de busca/listas no Xano — lote independente

- [ ] 5.1 Preparar extensões aditivas paginadas de `/profiles` e `/lists/public` com q/criador/descrição explícita, projeção pública e ordenação estável; testar compatibilidade com array atual, termos/coringas escapados, limites e filtragem antes de contagem/paginação, documentando índices e exemplos sanitizados.
- [ ] 5.2 Preparar consultas de detalhe público e próprio autenticado, reutilizando itens existentes; testar visitante/dono/outra conta/desativado, ID inexistente vs privado, itens e totais sem vazamento e mudança pública→privada/cache, registrando requisitos de autorização por endpoint.
- [ ] 5.3 No workspace atual identificado, com backup/prévia revisados e autorização do lote, publicar somente contratos aprovados e verificar estrutura/permissões/projeções por leitura independente; manter aberta sem evidência ou aprovação do lote. Não requer workspace novo e não copia dados reais como fixtures.
- [ ] 5.4 Após aprovação do lote de fixtures no workspace atual, executar aceite integrado de busca/paginação/detalhe/privacidade com visitante e duas contas descartáveis, incluindo links antigos e públicos expirados por privacidade; registrar API/navegador/limpeza e preservação de dados anteriores separadamente e só então liberar a experiência. Falhas induzidas permanecem locais.

## 6. Propagação incremental por família

- [ ] 6.1 Revisar Home/catálogo e suas mensagens/hero/CTAs com os tokens e prateleiras aprovados; validar foco, dobra inicial, títulos longos, grid/resultados e falhas parciais sem alterar o carregamento P0, registrando capturas comparáveis.
- [ ] 6.2 Modernizar ficha compartilhada e avaliações nos quatro tipos sem confundir nota/progresso/listas, preservando seletor acessível e spoilers; testar identidade externa/Jikan, complementos lentos, nota decimal e cliques de lista, com evidência por tipo e largura.
- [ ] 6.3 Ajustar biblioteca e Minhas listas, conservando diretório público agrupado e gerenciamento; testar filtros/itens/paginação/privacidade já existentes e links novos, registrando redundâncias condensadas e alternativas preservadas.
- [ ] 6.4 Ajustar perfil, conexões e diálogo de edição com feedback por campo; verificar nome/bio/banner/avatar longos, autoria/seguir/denunciar e foco, sem migrar storage de avatar/banner, registrando capturas desktop/celular.
- [ ] 6.5 Modernizar login/cadastro/recuperação usando composição e mascotes ativos; testar rotas, rótulos/autocomplete/colagem/mostrar senha, etapas e erros com fixtures sem alterar contratos de autenticação ou envio, registrando contraste e navegação.
- [ ] 6.6 Refinar apresentação do feed/compositor/discussão preservando foto principal, obra compacta, likes e comentários sob demanda; testar rascunho, erro, teclado e não duplicação de ações; anexos externos só usam contrato validado da change Cloudinary, sem antecipar ativação.
- [ ] 6.7 Investigar em cenário autorizado a origem da atividade de criação de listas relatada no feed, comparando com os contratos locais; registrar prova ou ausência de reprodução e apresentar recomendação específica antes de alterar eventos. Não criar autopost nem remover dados/handlers por hipótese.
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
