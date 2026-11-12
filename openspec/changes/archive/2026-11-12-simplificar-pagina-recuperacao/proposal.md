## Why

A página mostra dois formulários simultâneos e pede o mesmo e-mail duas vezes. O usuário solicitou menos campos e um design mais simples.

## What Changes

- Exibir um cartão compacto com uma etapa por vez: e-mail, código/senha e confirmação final.
- Reutilizar o e-mail informado, permitir trocar endereço e reenviar código.
- Manter confirmação da senha, acessibilidade e proteção contra repetição após sucesso.

## Capabilities

### New Capabilities

- `recovery-progressive-form`: Recuperação progressiva sem e-mail duplicado e conclusão clara.

### Modified Capabilities

Nenhuma; contratos Xano e uso único permanecem os existentes.

## Impact

Página account.py, SessionState, CSS e testes locais. Sem alteração Xano, provedor ou credenciais.
