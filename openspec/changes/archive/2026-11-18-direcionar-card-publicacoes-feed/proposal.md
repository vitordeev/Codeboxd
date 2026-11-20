## Why

O indicador de publicacoes no dashboard administrativo hoje nao leva a uma area util. A equipe deve conseguir abrir o feed do Codeboxd diretamente por esse card e encontra-lo no fim da fileira de indicadores.

## What Changes

- Tornar o card de publicacoes um link para o feed principal em `/feed`.
- Posicionar o card de publicacoes por ultimo na fileira de indicadores do dashboard.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `admin-dashboard`: definir destino e posicao do card de publicacoes.

## Impact

Afeta a apresentacao do dashboard administrativo e o contrato OpenSpec `admin-dashboard`. Nao altera dados, endpoints ou permissoes.
