# Filme atual no card principal — 20/10/2026

Complemento ativo de descoberta. Pedido: trocar o filme do card principal por
um mais atual. O destaque passa a priorizar a primeira obra da seleção
“Agora nos cinemas”; filmes populares continuam como alternativa em falha.

Consulta real TMDB `movie/now_playing`, pt-BR/região BR: primeiro resultado
Street Fighter, ID 1153576, lançamento 15/10/2026. A escolha acompanha a seleção
do provedor em vez de fixar permanentemente um filme no código.

- [x] Priorizar a seleção de cinema no destaque.
- [x] Conferir compilação e título exibido no navegador.

Compilação Reflex `--dry` e diff sem erros. Edge headless confirmou o título
“Street Fighter” no `.spotlight-title` do servidor local. Sem publicação remota.
