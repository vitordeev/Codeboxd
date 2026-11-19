## Why

Durante a edição manual da lista de teste 109, surgiu a linha `user_list.id=110`: pública, vazia e sem dono (`user_id=0`). O usuário autorizou explicitamente excluí-la para remover esse registro órfão do workspace compartilhado.

## What Changes

- Excluir somente `user_list.id=110`, após confirmar identidade exata e ausência de itens/referências.
- Registrar recibo local sanitizado e verificar a ausência após a chamada.
- Não alterar as contas 44/45, listas 106–109, nem outros registros.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. Esta é uma correção operacional pontual de dado órfão, sem mudança de comportamento do produto.

## Impact

Uma remoção controlada na tabela Xano `user_list` do workspace existente. Nenhum arquivo de aplicação ou contrato Xano será publicado.
