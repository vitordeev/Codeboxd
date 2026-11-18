## Why

O piloto `cbshared_e695fd5320e4` concluiu os testes de persistência, privacidade e rejeição de mutação cruzada, mas o executor parou ao interpretar uma resposta de lista como objeto. As credenciais temporárias dos proprietários se perderam; é necessário reconciliar somente as fixtures comprovadas sem repetir o lote.

## What Changes

- Verificar identidade e ausência de referências somente nas listas 125/126 e contas 50/51.
- Excluir apenas as listas próprias e vazias usando a API de metadata, preservando os itens e demais listas; desativar as contas via endpoint administrativo autenticado.
- Registrar o desvio de auditoria das exclusões de listas; preservar e verificar os eventos administrativos de desativação.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. Reconciliação pontual de fixtures, sem mudança do produto (`skip_specs: true`).

## Impact

Somente registros do piloto no workspace Xano 147717, recibo sanitizado e documentos OpenSpec. Sem alterações de schema, contratos, outros usuários ou registros.
