# Checkpoint atual do Codeboxd

- Cards de obras preservam o pÃ´ster inteiro no enquadramento.
- A pÃ¡gina de detalhes mostra serviÃ§os legais de streaming informados pelo TMDB para filmes e sÃ©ries no Brasil.

Estado salvo em 23/09/2026.

- A busca filtra resultados por palavras completas do título.
- A homepage usa fileiras horizontais verticais para filmes, séries, livros e animes.
- A numeração sobre as capas foi removida.
- A homepage tem três fileiras de animes: mais bem avaliados, populares e em destaque agora.
- A homepage tem cinco fileiras de livros, incluindo livros conhecidos (`1984`, `Duna`, `Harry Potter`, `Sapiens` e `O Hobbit`) e a busca específica `Teoria dos Jogos`.
- A capa padrão está em `assets/default-movie-cover.png`.
- Animes usam Kitsu. Registros antigos da Jikan são resolvidos pelo mapeamento MyAnimeList/Kitsu.
- O endpoint remoto `POST /media` do Xano foi atualizado para aceitar Kitsu e evitar duplicação de obras antigas.
- Diagnóstico das APIs: `docs/KITSU.md`.
- Última validação: 86 testes passaram e `reflex compile --dry` foi concluído com sucesso.

Para continuar, revisar primeiro `Codeboxd_main/services/catalog.py`, `Codeboxd_main/pages/social.py` e `Codeboxd_main/state/social.py`.
