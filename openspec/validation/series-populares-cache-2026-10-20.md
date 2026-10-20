# Recuperação da lista de séries populares — 20/10/2026

Complemento ativo de descoberta/confiabilidade operacional. Relato: somente
três séries populares. O catálogo salvo tinha três séries; `load_home` pulava
a consulta externa sempre que a lista não estava vazia, inclusive em fallback.

- [x] Distinguir lista popular carregada de alternativa local em cache.
- [x] Reconsultar primeira página e substituir fallback quando TMDB volta.
- [x] Fazer “Carregar mais” recuperar página 1 antes de paginar o fallback.
- [x] Verificar testes, compilação e navegador.

Consulta real autorizada a `tv/popular`, pt-BR, página 1: HTTP 200, 20 séries.
Filmes recebem a mesma correção. Listas externas carregadas e sua paginação
continuam preservadas entre visitas; falha de rede mantém os cards existentes.

Validação: 154 testes locais e compilação Reflex `--dry` passaram; diff sem erros.
Novas regressões cobrem substituição das três séries alternativas por 20 do
provedor e recuperação da página 1 antes de avançar. Edge headless confirmou
20 cards em “Séries populares” e 40 após “Carregar mais séries”. Nenhuma
alteração de dados remotos ou conta administrativa foi realizada.
