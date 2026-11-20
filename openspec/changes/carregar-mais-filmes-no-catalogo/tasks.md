## 1. Paginação independente por prateleira

- [x] 1.1 Adaptar a busca de páginas das coleções TMDB, Kitsu e Open Library para avançar pela mesma seleção de cada trilho, mantendo página por chave, deduplicação e estado de esgotamento; `reflex compile --dry` passou e o diff confirma os parâmetros próprios de cada provedor.
- [x] 1.2 Conectar cada prateleira ao carregamento automático no fim, remover setas e rodapés manuais de todos os trilhos e ocultar a barra sem impedir rolagem por toque, trackpad ou teclado; compilação Reflex passou e a classe CSS mantém `overflow-x: auto` e foco de teclado.

## 2. Validação

- [x] 2.1 Validar os artefatos com `openspec validate carregar-mais-filmes-no-catalogo --type change`, executar `git diff --check` e registrar evidências; busca e paginação de categorias não foram alteradas.
