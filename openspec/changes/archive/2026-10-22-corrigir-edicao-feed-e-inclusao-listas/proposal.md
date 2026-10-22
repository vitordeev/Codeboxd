## Why

Editar um post está criando outra publicação. Nas listas, o seletor atual limita
a inclusão às obras já carregadas e a ficha só oferece atalhos para listas base.
O usuário pediu edição sem duplicação, referência opcional e inclusão por busca
ou diretamente pela ficha.

## What Changes

- Preservar identidade de post durante edição, com ou sem referência a obra.
- Permitir manter, trocar ou remover a obra associada sem criar outro post.
- Buscar filmes, séries, animes e livros dentro de uma lista própria para adicionar.
- Escolher qualquer lista própria na ficha de uma obra e adicionar com confirmação.
- Preservar autoria, privacidade, imagens, rascunho em falhas e proteção de duplicatas.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `social-feed`: referência opcional e edição preservando o post original.
- `user-lists`: inclusão por busca no catálogo e pela ficha da obra.

## Impact

Estado e páginas sociais Reflex, estilos, testes e contratos Xano pertinentes
se a investigação demonstrar necessidade. Provedores TMDB/Kitsu/Open Library
existentes. Sem novas dependências, migração destrutiva ou Docker. Evidências
locais, simulação, navegador e remoto serão registradas separadamente.
