## MODIFIED Requirements

### Requirement: Indicadores do dashboard abrem suas areas administrativas
O dashboard MUST permitir abrir a area relacionada a cada indicador. Os cards de usuarios, catalogo e reports MUST abrir suas respectivas areas administrativas existentes. O card de publicacoes MUST abrir o feed principal do Codeboxd em `/feed` e MUST aparecer por ultimo na fileira de indicadores.

#### Scenario: Administradora abre usuarios pelo indicador
- **WHEN** a administradora seleciona o indicador de usuarios
- **THEN** o sistema abre a area de usuarios e apresenta uma listagem inicial paginada sem exigir um termo de busca

#### Scenario: Administradora abre o catalogo pelo indicador
- **WHEN** a administradora seleciona o indicador de obras cadastradas
- **THEN** o sistema abre a secao existente de catalogo, com acesso as abas por tipo de obra

#### Scenario: Administradora abre reports pelo indicador
- **WHEN** a administradora seleciona o indicador de reports pendentes
- **THEN** o sistema abre a fila de reports com o filtro de pendentes aplicado

#### Scenario: Administradora abre o feed pelo indicador de publicacoes
- **WHEN** a administradora seleciona o card de publicacoes no dashboard
- **THEN** o sistema abre o feed principal do CodeBoxd em `/feed`

#### Scenario: Card de publicacoes aparece ao final
- **WHEN** o dashboard apresenta a fileira de indicadores
- **THEN** o card de publicacoes aparece depois dos cards de usuarios, catalogo e reports

#### Scenario: Indicador sem area administrativa correspondente
- **WHEN** o indicador de publicacoes nao possui uma secao administrativa propria
- **THEN** o card abre o feed principal relacionado em `/feed` sem direcionar para uma area administrativa sem relacao
