## Why

As abas de s?ries, animes e livros devem mostrar mais resultados mesmo quando h? poucos registros no cat?logo persistido. O usu?rio escolheu consultar fontes externas sem gravar esses resultados.

## What Changes

- Solicitar at? 35 registros por p?gina em filmes, s?ries, animes e livros.
- Complementar s?ries, animes e livros com resultados reais dos provedores existentes, marcados como externos e n?o cadastrados.
- Remover a??es e grava??es de importa??o em lote; resultados externos servem somente para consulta.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `admin-catalog-management`: padronizar 35 resultados por p?gina e exibir resultados externos sem persist?ncia ou edi??o.

## Impact

Afeta a tela e o estado do cat?logo administrativo e os adaptadores de leitura TMDB, Kitsu e Open Library. N?o altera contratos Xano nem grava resultados externos.
