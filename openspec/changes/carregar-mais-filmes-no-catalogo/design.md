## Context

Veja `proposal.md` e a delta de `media-discovery`. A home combina trilhos populares de filmes/séries com coleções pagináveis de filmes, séries, livros e animes. Cada trilho precisa avançar pela fonte/categoria já definida para não misturar seleções editoriais.

## Goals / Non-Goals

**Goals:** dar carregamento incremental independente a cada prateleira da home, manter identidade e ordenação, e ocultar controles visuais redundantes sem desativar a rolagem nativa.

**Non-Goals:** alterar busca, páginas de categoria, APIs Xano, provedores, conteúdo inicial, ordenação, layout dos cards ou comportamento de rotas.

## Decisions

- Reutilizar os estados e a paginação dos trilhos populares de filmes/séries; generalizar a função de `home_collection` para aceitar número de página conforme o provedor: `page` para TMDB/Open Library e `page[offset]` para Kitsu.
- Manter página atual, estado de carregamento e exaustão por `home_collection` (chave da prateleira), sem compartilhar resultado entre coleções. Acrescentar os itens de forma imutável ao estado Reflex e deduplicar pelo `identity_key`.
- Quando uma resposta de página não contém novas identidades e não houve erro, marcar aquela prateleira como esgotada. Erros não avançam a página nem são tratados como fim normal.
- Aplicar ao evento `on_scroll` de cada trilho um script cliente que verifica proximidade do fim e devolve um booleano ao callback Reflex. Throttle no evento e guardas de loading/exhaustion no estado reduzem tráfego e concorrência.
- Remover setas e footers manuais de todas as prateleiras da home. Ocultar scrollbar por classe CSS comum às prateleiras, preservando `overflow-x: auto`, snap e foco de teclado. Os botões de paginação de buscas/categorias não usam essa classe e permanecem iguais.

Alternativas consideradas: uma paginação popular genérica misturaria o conteúdo de coleções como “agora nos cinemas”, “livros de fantasia” e “animes atuais”; esconder controles sem paginação por coleção deixaria alguns trilhos sem conteúdo novo. A paginação por chave conserva a semântica de cada prateleira.

## Risks / Trade-offs

- [Providers usam formas de paginação e tamanhos diferentes] → adaptar os parâmetros por tipo de coleção e considerar esgotamento somente quando uma página não traz identidades novas.
- [Vários trilhos simultaneamente no fim] → throttling no cliente e estados de loading independentes por trilho; requisições continuam limitadas pelos semáforos atuais de provedor durante a carga inicial.
- [Scrollbar invisível reduz descoberta da rolagem] → preservar rolagem nativa por toque, trackpad e teclado, com `tab_index=0`.
- [Provider falha durante uma página adicional] → manter página e cards, expor o erro existente e permitir nova tentativa em outro evento de rolagem.

## Migration Plan

Sem migração de dados ou API. Restaurar o markup/CSS anterior reverte a mudança; a busca e a paginação de categoria não são afetadas.
