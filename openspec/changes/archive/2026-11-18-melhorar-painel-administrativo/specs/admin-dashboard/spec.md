## ADDED Requirements

### Requirement: Indicadores do dashboard abrem suas áreas administrativas
O dashboard MUST permitir abrir a área administrativa correspondente a cada indicador que tenha uma seção de gerenciamento existente. O card de publicações MUST permanecer informativo enquanto não houver uma seção administrativa de publicações.

#### Scenario: Administradora abre usuários pelo indicador
- **WHEN** a administradora seleciona o indicador de usuários
- **THEN** o sistema abre a área de usuários e apresenta uma listagem inicial paginada sem exigir um termo de busca

#### Scenario: Administradora abre o catálogo pelo indicador
- **WHEN** a administradora seleciona o indicador de obras cadastradas
- **THEN** o sistema abre a seção existente de catálogo, com acesso às abas por tipo de obra

#### Scenario: Administradora abre reports pelo indicador
- **WHEN** a administradora seleciona o indicador de reports pendentes
- **THEN** o sistema abre a fila de reports com o filtro de pendentes aplicado

#### Scenario: Indicador sem área administrativa correspondente
- **WHEN** o dashboard apresenta o indicador de publicações e não existe seção administrativa de publicações
- **THEN** o indicador permanece informativo e não leva a uma área sem relação ou inexistente

### Requirement: Identificação compacta da pessoa administradora
As páginas administrativas MUST apresentar um controle de avatar circular para a sessão administrativa validada. Ao ativá-lo, o controle MUST mostrar o nome de exibição, o nome de usuário e o cargo da sessão atual. A identidade e o cargo MUST vir de dados verificados pelo servidor, e a interface MUST oferecer fallback legível quando não houver avatar ou perfil completo.

#### Scenario: Administradora abre os dados da própria sessão
- **WHEN** uma administradora autenticada ativa seu avatar no cabeçalho
- **THEN** o painel mostra o nome, o nome de usuário e o cargo administrativo associados à sessão atual

#### Scenario: Perfil sem foto ou dados complementares
- **WHEN** a sessão administrativa não possui foto ou algum dado opcional de perfil
- **THEN** o cabeçalho mostra um fallback visual e usa somente os dados disponíveis da sessão sem bloquear a navegação

#### Scenario: Pessoa sem acesso administrativo tenta obter a identidade administrativa
- **WHEN** uma pessoa visitante ou membro solicita os dados destinados ao cabeçalho administrativo
- **THEN** o backend rejeita a solicitação sem revelar dados administrativos
