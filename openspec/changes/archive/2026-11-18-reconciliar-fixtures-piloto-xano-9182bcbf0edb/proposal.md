## Why

O piloto `cbshared_9182bcbf0edb` foi interrompido após criar as contas 48/49 e as listas 119/120, deixando a lista 119 pública. O usuário autorizou reconciliar exatamente essas fixtures para remover a exposição e desativar as contas.

## What Changes

- Confirmar por leitura a identidade, propriedade, visibilidade e ausência de referências das listas 119/120 antes de alterá-las.
- Tornar a lista 119 privada, excluir somente as listas 119/120 e desativar somente as contas 48/49, registrando recibos e verificações posteriores.
- Documentar que a reconciliação administrativa não comprova o aceite funcional de autoria entre contas.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. Reconciliação pontual de fixtures, sem mudança de comportamento do produto (`skip_specs: true`).

## Impact

Somente registros de teste no workspace Xano 147717, recibos desta change e documentação OpenSpec. Nenhuma alteração de schema, endpoints publicados ou dados fora dos IDs explicitamente autorizados.
