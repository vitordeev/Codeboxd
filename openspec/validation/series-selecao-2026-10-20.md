# Seleção de séries conhecidas — 20/10/2026

Complemento ativo de descoberta. O usuário esclareceu que deseja Stranger
Things, The Boys, Reacher e La Casa de Papel na fileira “Séries populares”.

- [x] Confirmar os quatro IDs e títulos com consultas reais ao TMDB (HTTP 200).
- [x] Priorizar esses títulos na homepage, deduplicando com os populares externos.
- [x] Validar testes, compilação e ordem dos cards no navegador.

A fileira passa a ter seleção editorial inicial solicitada pelo usuário,
seguida dos resultados de popularidade do TMDB. Buscas por texto e categorias
continuam com seus critérios originais; a seleção afeta apenas a homepage.
Ao visitar a home, séries são reconsultadas para substituir caches anteriores.
Falha em uma das quatro fichas não impede o restante da seleção.

155 testes locais, compilação Reflex `--dry` e diff sem erros passaram.
Edge headless confirmou os quatro primeiros cards nesta ordem: Stranger Things,
The Boys, Reacher, La casa de papel. Total observado: 23 séries após deduplicação
da seleção editorial com o TMDB. Sem alteração de registros remotos.
