## Why

O usuário determinou que e-mail sem cadastro não deve avançar à etapa de código. O comportamento anterior avançava deliberadamente por resposta genérica, inclusive em erros 400/404.

## What Changes

- Exigir conta ativa no endpoint antes de gerar ou enviar código; inexistente/inativa retorna 404 sanitizado.
- Manter endereço na etapa inicial e exibir orientação; falhas de envio não serão tratadas como sucesso.
- Preservar cooldown, template, validação/uso único e proteção após troca concluída.
- Registrar substituição explícita da decisão anterior de ocultar existência de contas, sem apagar evidências históricas.

## Capabilities

### New Capabilities

- `recovery-account-eligibility`: Avanço da recuperação somente após solicitação aceita para conta ativa.

### Modified Capabilities

Nenhuma capacidade central alterada. Reconciliar contratos ativos de recuperação e formulário progressivo com a regra solicitada.

## Impact

Endpoint Xano de solicitação, SessionState, testes, executor de publicação com saída por change e artefatos ativos OpenSpec. Sem mudanças em senhas, domínio ou autenticação comum.
