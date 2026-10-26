## ADDED Requirements

### Requirement: Revoke sessions after password change

O sistema MUST invalidar todas as credenciais autenticadas anteriores da conta quando a senha for alterada com sucesso. A decisão MUST ser aplicada pelo backend em todas as rotas protegidas, preservando as sessões de outras contas.

#### Scenario: Previous token after successful password change

- **WHEN** uma conta troca a senha com sucesso e reutiliza um token anterior
- **THEN** leituras e mutações protegidas rejeitam o token antes de operar sobre dados
- **AND** login com a senha nova cria sessão válida e a senha anterior é rejeitada

#### Scenario: Another account remains authenticated

- **WHEN** uma conta altera a senha
- **THEN** uma sessão válida de outra conta continua válida e suas permissões não mudam

#### Scenario: Concurrent use of a password change credential

- **WHEN** duas alterações tentam consumir credenciais da mesma versão de sessão
- **THEN** a versão é revalidada sob transação e uma credencial revogada não pode efetuar outra alteração

### Requirement: Reject legacy and mismatched session claims

O sistema MUST rejeitar tokens sem versão válida ou com versão diferente da conta, inclusive tokens emitidos antes da implantação desta política. A pessoa MUST poder recuperar acesso por novo login com credenciais válidas.

#### Scenario: Legacy token requests protected data

- **WHEN** um token legado sem versão acessa uma rota autenticada
- **THEN** recebe rejeição de autenticação e nenhum dado protegido é retornado

### Requirement: Restrict recovery credential purpose

Credenciais de recuperação MUST permitir somente a alteração de senha autorizada, respeitando a versão vigente. Elas MUST NOT conceder acesso às funcionalidades pessoais, sociais ou administrativas e MUST ser invalidadas após a alteração.

#### Scenario: Recovery token attempts social access

- **WHEN** uma credencial de recuperação tenta acessar funcionalidade social ou administrativa
- **THEN** o backend rejeita a operação antes de ler ou alterar os dados protegidos

#### Scenario: Recovery token is reused after password change

- **WHEN** uma credencial de recuperação já usada tenta alterar a senha novamente
- **THEN** o backend rejeita o reuso por versão de sessão revogada
