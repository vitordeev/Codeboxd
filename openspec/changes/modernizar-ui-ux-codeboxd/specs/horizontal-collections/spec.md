## Purpose

Permitir exploração previsível das coleções horizontais do Codeboxd com mouse,
toque, trackpad e teclado, preservando alternativas sem gestos e acesso às obras.

## ADDED Requirements

### Requirement: Arrasto de mouse previsível
Coleções horizontais SHALL permitir arrastar com o botão primário do mouse após distinguir intenção de arrasto de clique, sem selecionar texto/imagens acidentalmente ou abrir um card durante esse arrasto.

#### Scenario: Arrastar sobre um card
- **WHEN** o usuário pressiona o mouse em um card e desloca horizontalmente além do limiar de intenção
- **THEN** a coleção SHALL acompanhar o deslocamento e não abrir o card ao soltar o ponteiro

#### Scenario: Clique sem arrasto
- **WHEN** o usuário clica sem ultrapassar o limiar de arrasto
- **THEN** a ação normal do card SHALL ocorrer uma única vez

#### Scenario: Cancelar ou perder captura
- **WHEN** o gesto é cancelado, o ponteiro perde captura ou a coleção é desmontada
- **THEN** o comportamento SHALL restaurar a interação normal sem travar seleção, rolagem ou cliques posteriores

### Requirement: Toque e rolagem de página preservados
Coleções SHALL oferecer rolagem horizontal nativa com dedo/trackpad e preservar rolagem vertical e zoom da página. Gestos horizontais SHALL permanecer confinados à coleção, sem exigir precisão incompatível com toque.

#### Scenario: Swipe horizontal
- **WHEN** o usuário desliza horizontalmente no trilho em celular/tablet
- **THEN** as obras SHALL se deslocar de forma previsível, sem ativação acidental dos cards

#### Scenario: Gesto vertical ou zoom
- **WHEN** o usuário inicia rolagem vertical sobre a coleção ou amplia a página
- **THEN** a página SHALL manter seu comportamento normal sem bloqueio global de gesto

### Requirement: Alternativas funcionais ao arrasto
As coleções SHALL manter controles identificados de anterior/próximo e acesso por teclado. Ação de carregar mais resultados SHALL permanecer distinta de apenas deslocar a área visível.

#### Scenario: Usuário não utiliza gestos
- **WHEN** o usuário aciona anterior/próximo por clique ou teclado
- **THEN** ele SHALL conseguir explorar a coleção sem arrastar e reconhecer seus limites

#### Scenario: Foco no trilho
- **WHEN** a coleção recebe foco e o usuário usa esquerda/direita ou início/fim
- **THEN** a região SHALL revelar os itens correspondentes sem capturar teclas de formulários ou mudar a rolagem vertical indevidamente

#### Scenario: Foco em um card fora da área
- **WHEN** o usuário chega por Tab a um item parcialmente oculto
- **THEN** o item e seu foco SHALL ser revelados, mantendo Enter/Space conforme o controle nativo

### Requirement: Controles e estados acessíveis
Cada coleção SHALL ter nome acessível, foco visível, controles associados à região e estados coerentes de início/fim. A área interativa SHALL atender à política de alvos da interface e não depender apenas de hover.

#### Scenario: Coleções repetidas na página
- **WHEN** existem várias prateleiras
- **THEN** cada controle SHALL identificar e operar somente sua própria coleção sem IDs ambíguos

#### Scenario: Todos os itens já visíveis
- **WHEN** a coleção não tem overflow ou chega a um extremo
- **THEN** seus controles SHALL comunicar o limite sem mover a página ou simular que novos dados foram carregados

### Requirement: Movimento discreto e preferências respeitadas
As coleções SHALL usar movimento previsível, sem autoplay obrigatório ou loop infinito. Movimento reduzido SHALL desabilitar deslocamentos animados não essenciais, mantendo todos os itens alcançáveis.

#### Scenario: Movimento reduzido ativo
- **WHEN** o usuário aciona uma seta ou navega pelo teclado com essa preferência
- **THEN** o deslocamento SHALL ser imediato ou reduzido, sem perda de foco ou de acesso às obras

### Requirement: Interação horizontal leve e consistente
Arrastar e rolar SHALL reutilizar um comportamento comum entre páginas e não gerar chamadas ao backend nem atualizações reativas remotas por movimento. Carregamento de novos itens SHALL preservar paginação, identidade e isolamento já existentes.

#### Scenario: Arrasto contínuo
- **WHEN** o usuário realiza um gesto completo sobre a coleção
- **THEN** o tráfego de backend causado pelo gesto SHALL ser zero e a quantidade de itens SHALL permanecer estável até uma ação explícita de carregamento

#### Scenario: Renderizar novamente a página
- **WHEN** a coleção atualiza seus itens ou volta a aparecer após navegação
- **THEN** uma ação SHALL produzir um único deslocamento sem listeners acumulados ou interferência em outras coleções
