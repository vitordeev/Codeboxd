## Why

O usuário solicitou auditar e implementar restrições faltantes na redefinição. Código, cooldown, conta ativa, tentativas e revogação já estão implementados; o endpoint final ainda aceita sessão comum e permite repetir a senha atual, com validações/mensagens inconsistentes.

## What Changes

- Restringir endpoint final a credencial temporária de recuperação vigente, com conta ativa.
- Exigir nova senha diferente da atual sob bloqueio transacional e validar política antes da gravação.
- Formalizar limite de 128 caracteres na redefinição, mantendo mínimo de oito, letra e número já usados pelo produto; confirmação obrigatória.
- Distinguir erro de código, rejeição de nova senha e expiração de autorização na UI; limpar sessão local da mesma conta após sucesso.
- Validar com testes locais e uma conta member descartável criada exclusivamente para os testes remotos, sem envio de e-mail; removê-la ao final.

## Capabilities

### New Capabilities

- `password-reset-restrictions`: Autorização exclusiva de recuperação e política consistente de nova senha.

### Modified Capabilities

Nenhuma spec central altera seus critérios; reconciliar contrato ativo de recuperação. A decisão explícita do usuário sobre rejeitar e-mail sem conta permanece.

## Impact

Endpoint reset/update_password, SessionState, campos/hints da página, testes e ferramentas de publicação/validação da change. Nenhuma mudança no serviço de e-mail, DNS, papéis ou senhas de contas reais. Helpers históricos que usam sessão normal para trocar/restaurar senha não podem ser reutilizados sem adaptação.
