# user-authentication Specification

## Purpose

Definir como os usuários criam contas, realizam autenticação e acessam áreas protegidas do Codeboxd de forma segura e consistente.

## Requirements

### Requirement: User registration

The system SHALL allow a new user to create an account.

The registration process SHALL require a username, email address and password.

The system SHALL reject registration when required information is missing or invalid.

#### Scenario: Successful registration

- **WHEN** a user provides valid and complete registration information
- **THEN** the system SHALL create a new user account

#### Scenario: Missing required registration information

- **WHEN** a user submits the registration form with required information missing
- **THEN** the system SHALL reject the registration and inform the user about the missing information

### Requirement: Unique user identity

The system SHALL require each user account to have a unique username and email address.

#### Scenario: Duplicate username

- **WHEN** a user attempts to register with a username already associated with another account
- **THEN** the system SHALL reject the registration and inform the user that the username is unavailable

#### Scenario: Duplicate email address

- **WHEN** a user attempts to register with an email address already associated with another account
- **THEN** the system SHALL reject the registration and inform the user that the email address is already in use

### Requirement: User authentication

The system SHALL allow registered users to authenticate using their account credentials.

#### Scenario: Successful login

- **WHEN** a registered user provides valid authentication credentials
- **THEN** the system SHALL authenticate the user and create an authenticated session

#### Scenario: Invalid login credentials

- **WHEN** a user provides invalid authentication credentials
- **THEN** the system SHALL deny access and inform the user that the credentials are invalid

### Requirement: Protected user functionality

The system SHALL require authentication before allowing users to access functionality that modifies personal or social data.

#### Scenario: Unauthenticated access to protected functionality

- **WHEN** an unauthenticated user attempts to perform an action that requires authentication
- **THEN** the system SHALL deny the action and require the user to authenticate

### Requirement: User logout

The system SHALL allow an authenticated user to end their current session.

#### Scenario: Successful logout

- **WHEN** an authenticated user requests to log out
- **THEN** the system SHALL end the user's authenticated session

### Requirement: Authentication failure handling

The system SHALL prevent authentication when account credentials cannot be validated.

#### Scenario: Authentication service failure

- **WHEN** the system cannot validate user credentials due to a temporary authentication failure
- **THEN** the system SHALL inform the user that authentication could not be completed

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
