## Purpose

Oferece às pessoas administradoras uma visão confiável da atividade e das pendências do Codeboxd para orientar o gerenciamento diário do website.

## ADDED Requirements

### Requirement: Dashboard restrito a administradores
O sistema MUST permitir acesso ao dashboard somente a sessões autenticadas cujo papel administrativo seja confirmado pelo backend. A proteção deve valer também para os dados e operações solicitados pela página.

#### Scenario: Administrador acessa o dashboard
- **WHEN** uma pessoa autenticada com papel de administradora abre a área de gerenciamento
- **THEN** o sistema apresenta o dashboard e seus dados autorizados

#### Scenario: Pessoa sem papel administrativo tenta acessar
- **WHEN** uma pessoa visitante ou membro abre a área administrativa ou solicita seus dados
- **THEN** o sistema bloqueia o acesso e não revela informações administrativas

### Requirement: Indicadores baseados em dados reais
O dashboard MUST apresentar indicadores de usuários, publicações, obras catalogadas e reports pendentes com valores obtidos dos dados persistidos disponíveis. Quando uma métrica não puder ser carregada, o sistema MUST sinalizar a indisponibilidade sem apresentar um valor inventado como real.

#### Scenario: Indicadores carregados
- **WHEN** os dados necessários estão disponíveis
- **THEN** o dashboard mostra os totais correspondentes e indica a atualização conforme os dados recebidos

#### Scenario: Fonte de uma métrica indisponível
- **WHEN** uma consulta de indicador falha
- **THEN** o dashboard mostra um estado de erro ou indisponibilidade para essa métrica sem substituir a falha por um total fictício

### Requirement: Atividade recente e pendências
O dashboard MUST apresentar atividade recente e itens que requerem atenção quando existirem dados para essas seções.

#### Scenario: Existem atividades e pendências
- **WHEN** há atividade recente ou reports pendentes
- **THEN** o dashboard apresenta esses itens com contexto suficiente para abrir a área correspondente

#### Scenario: Não há itens para exibir
- **WHEN** não há atividade recente ou pendências
- **THEN** o dashboard apresenta estados vazios claros para as respectivas seções

### Requirement: Estados de carregamento
O dashboard MUST informar quando seus dados estão carregando ou quando uma seção não pode ser carregada, mantendo disponíveis as demais seções que tenham sido carregadas com sucesso.

#### Scenario: Carregamento parcial
- **WHEN** uma das fontes do dashboard falha e outras respondem
- **THEN** o sistema mostra os dados disponíveis e indica a falha somente na seção afetada

### Requirement: Login administrativo dedicado
O sistema MUST oferecer a rota `/admin/login` com formulário de e-mail e senha integrado ao serviço de autenticação existente. Somente uma sessão validada com papel `admin` MUST acessar o painel. Contas válidas sem esse papel não devem receber sessão administrativa.

#### Scenario: Administrador faz login
- **WHEN** uma pessoa informa credenciais válidas de uma conta com papel `admin`
- **THEN** o sistema valida a sessão e redireciona para `/admin`

#### Scenario: Credenciais válidas sem papel administrativo
- **WHEN** uma pessoa com credenciais válidas de membro usa `/admin/login`
- **THEN** o sistema não concede acesso ao painel e mostra uma mensagem de permissão insuficiente

#### Scenario: Credenciais inválidas
- **WHEN** uma pessoa envia credenciais incorretas
- **THEN** o sistema mantém o formulário disponível e mostra uma mensagem de erro sem revelar detalhes sensíveis

#### Scenario: Sessão administrativa existente
- **WHEN** uma pessoa administradora autenticada abre `/admin/login`
- **THEN** o sistema redireciona para `/admin` sem solicitar as credenciais novamente
