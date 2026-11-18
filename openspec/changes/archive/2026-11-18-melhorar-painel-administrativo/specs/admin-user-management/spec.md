## ADDED Requirements

### Requirement: Listagem inicial paginada de usuários
A área administrativa de usuários MUST poder mostrar contas existentes em páginas quando a busca estiver vazia, mantendo os filtros e a proteção administrativa existentes. A listagem MUST continuar excluindo senhas, tokens e outros segredos.

#### Scenario: Administradora abre a área sem busca
- **WHEN** uma administradora acessa a área de usuários sem informar um termo de busca
- **THEN** o sistema apresenta a primeira página de contas autorizadas ou um estado vazio claro se não houver resultados

#### Scenario: Administradora navega pelas páginas sem busca
- **WHEN** existem mais contas do que cabem na página atual e a busca permanece vazia
- **THEN** a paginação carrega a página seguinte sem exigir ou inventar um termo de busca

#### Scenario: Pessoa sem acesso administrativo tenta abrir a listagem
- **WHEN** uma pessoa sem papel administrativo solicita a listagem inicial
- **THEN** o backend rejeita a consulta e não revela dados das contas
