## Purpose

Garantir que somente prova temporária de recuperação autorize a redefinição e que a nova senha siga as regras do produto sem reutilizar a senha atual.

## ADDED Requirements

### Requirement: Credencial exclusiva de recuperação
O endpoint final MUST exigir conta ativa e credencial vigente com finalidade de recuperação e versão atual da sessão. Sessão normal, credencial expirada ou revogada MUST ser rejeitada antes de alterar a senha.

#### Scenario: Sessão comum
- **WHEN** uma sessão comum tenta usar o endpoint final de recuperação
- **THEN** a operação é rejeitada sem alterar senha ou versão

#### Scenario: Recuperação concluída
- **WHEN** uma credencial válida de recuperação conclui a troca
- **THEN** senha e versão são atualizadas atomicamente e credenciais anteriores deixam de autorizar operações

### Requirement: Nova senha válida e diferente
Nova senha MUST ter de 8 a 128 caracteres, ao menos uma letra ASCII e um dígito ASCII, confirmação idêntica e ser diferente da senha atual. O backend MUST aplicar essas regras sem depender do formulário e sem truncar ou remover espaços da senha.

#### Scenario: Senha inválida ou confirmação divergente
- **WHEN** senha ou confirmação não satisfazem a política
- **THEN** o backend rejeita a alteração e o formulário valida o que puder antes de consumir o código

#### Scenario: Senha igual à atual
- **WHEN** a nova senha corresponde ao hash atual
- **THEN** a alteração é rejeitada sem incrementar a versão, mantendo a senha atual

### Requirement: Feedback e sessão após troca
A interface MUST diferenciar erro do código de falha após sua aceitação e orientar novo pedido quando necessário, sem persistir a credencial de recuperação. Após sucesso MUST limpar sessão local da mesma conta e preservar identidade local de outra conta.

#### Scenario: Falha depois do código aceito
- **WHEN** o código foi aceito e a atualização da senha é rejeitada
- **THEN** a interface informa o problema de senha ou autorização sem afirmar que o código estava incorreto

#### Scenario: Sessão da conta recuperada
- **WHEN** a troca termina e a mesma conta possuía sessão local
- **THEN** a sessão local é limpa e o próximo acesso exige novo login
