## Purpose

Permite que administradores localizem contas e executem ações de gerenciamento com autorização no servidor, transparência e preservação das informações privadas dos usuários.

## ADDED Requirements

### Requirement: Pesquisar e consultar usuários
O sistema MUST permitir que administradores pesquisem usuários e consultem os dados administrativos necessários para gerenciar uma conta. A consulta MUST excluir senhas, tokens e outros segredos.

#### Scenario: Busca encontra usuários
- **WHEN** uma administradora pesquisa por identificador ou nome disponível
- **THEN** o sistema apresenta somente contas correspondentes e informações não secretas

#### Scenario: Busca sem correspondências
- **WHEN** nenhum usuário corresponde aos filtros
- **THEN** o sistema apresenta um estado vazio e permite ajustar a busca

### Requirement: Acesso administrativo às contas
O sistema MUST validar o papel de administradora no backend antes de retornar dados administrativos ou alterar uma conta.

#### Scenario: Membro tenta consultar ou alterar contas
- **WHEN** uma sessão sem papel administrativo solicita uma operação de gerenciamento de usuários
- **THEN** o backend rejeita a solicitação sem revelar dados da conta nem aplicar alterações

### Requirement: Suspender e reativar contas
O sistema MUST permitir que administradores suspendam e reativem contas por ações explícitas, com confirmação antes da mudança. Uma conta suspensa MUST deixar de usar as capacidades protegidas conforme as regras de autenticação vigentes.

#### Scenario: Suspensão confirmada
- **WHEN** uma administradora confirma a suspensão de uma conta
- **THEN** o sistema atualiza seu estado, informa o resultado e impede novas ações protegidas pela conta suspensa

#### Scenario: Suspensão cancelada
- **WHEN** a administradora cancela a confirmação
- **THEN** o sistema mantém a conta sem alterações

#### Scenario: Conta reativada
- **WHEN** uma administradora confirma a reativação de uma conta suspensa
- **THEN** o sistema atualiza o estado e informa o resultado

### Requirement: Registrar ações administrativas sobre contas
O sistema MUST registrar a ação administrativa aplicada à conta, a pessoa responsável, o horário e o motivo quando informado.

#### Scenario: Ação administrativa concluída
- **WHEN** uma conta é suspensa ou reativada
- **THEN** o sistema preserva um registro auditável da ação e de seu responsável
