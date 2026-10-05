# Integração Kitsu e diagnóstico das APIs

Verificação em 23/09/2026. Estes são resultados pontuais, não uma garantia de disponibilidade contínua.

## Integração

- Busca, navegação por categoria, ranking, detalhes, obras relacionadas, críticas públicas (quando disponíveis) e trailers usam `https://kitsu.app/api/edge`.
- Não há integração com AniList nem consultas de catálogo à Jikan.
- Consultas públicas não precisam de chave. Respostas bem-sucedidas da Kitsu ficam em cache por cinco minutos, com limite de 128 entradas por processo.
- Itens marcados `nsfw` ou com classificação `R18` são excluídos. O filtro remoto `filter[nsfw]` não é aceito e não é enviado.
- Animes antigos com `external_source=jikan` são resolvidos pelo mapeamento `myanimelist/anime`; IDs numéricos de serviços diferentes nunca são tratados como equivalentes sem mapeamento.
- `POST /media` no Xano aceita Kitsu e reaproveita a obra antiga quando o mapeamento MyAnimeList aponta para um registro existente. As avaliações e listas permanecem associadas ao registro original.
- Algumas sinopses e títulos da Kitsu são fornecidos em inglês; o app não os traduz automaticamente.

## Retornos observados

| API / consulta | Retorno | Diagnóstico |
| --- | --- | --- |
| Jikan `/v4/top/anime` | HTTP 504 | `Jikan failed to connect to MyAnimeList. MyAnimeList may be down/unavailable or refuses to connect` |
| Kitsu, busca e detalhes | HTTP 200 | Consultas concluídas. |
| Kitsu, ranking com `filter[nsfw]` durante o teste inicial | HTTP 400, código 102 | `Filter not allowed`: `nsfw is not allowed.` Parâmetro removido da integração. |
| Kitsu, ranking com os parâmetros finais | Sucesso | 20 animes retornados. |
| Kitsu, críticas de Cowboy Bebop | HTTP 200, lista vazia | Ausência de críticas nesse endpoint, não erro. |
| TMDB, filmes populares | HTTP 200 | 20 filmes retornados. |
| Open Library, busca por Duna | HTTP 200 | Resultados retornados. |
| Xano, login e catálogo | HTTP 200 | Conta de teste e leitura do catálogo funcionando. |
| Xano, salvar Cowboy Bebop como Kitsu | HTTP 200 | Reutilizou o registro antigo, sem duplicação. |
| Xano, Kitsu com categoria incorreta em teste negativo | HTTP 400 | Rejeição esperada de dados inválidos. |

O ambiente restrito de execução também retornou `ConnectError / WinError 10013` por bloqueio de rede. Isso não era erro HTTP das APIs: ao repetir com acesso à rede, obtivemos os resultados acima.

## Observabilidade e validação

O servidor registra `catalog_failure` com provedor, caminho, status e motivo. Cabeçalhos de autenticação e parâmetros de consulta não são registrados. A interface diferencia erro HTTP, limite de consultas, tempo esgotado, falha de conexão e resposta inválida. Um `Retry-After` longo é respeitado, sem novas tentativas prematuras.

- 86 testes automatizados passaram e o Reflex compilou.
- Teste real: 20 animes no ranking; quatro resultados relevantes para Cowboy Bebop; detalhes com capa; três obras relacionadas; um trailer.
- Compatibilidade real: Naruto, MyAnimeList ID 20, foi resolvido para Kitsu ID 11 mantendo a identidade antiga.
- Atualização remota limitada a um endpoint (`POST /media`) após prévia; nenhuma tabela ou registro foi excluído.

Referência: https://hummingbird-me.github.io/api-docs/
- Navegador: homepage exibiu 20 animes da Kitsu; busca abriu a ficha de Cowboy Bebop; nenhum erro JavaScript foi registrado.
