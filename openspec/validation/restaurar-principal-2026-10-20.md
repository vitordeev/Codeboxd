# Restaurar catálogo da página principal — 20/10/2026

Complemento ativo de descoberta e confiabilidade operacional. O usuário pediu
restaurar também o comportamento da página principal após esclarecer o trabalho
do dashboard. A retirada anterior está preservada no histórico de
`catalogo-abas-2026-10-20.md`.

- [x] Restaurar obras persistidas como alternativa nos destaques e nas categorias.
- [x] Preservar alterações administrativas e resultados dos provedores disponíveis.
- [x] Verificar testes, compilação e navegador.

TMDB_READ_TOKEN continua ausente: as obras salvas permitem exibir filmes/séries,
mas não substituem o catálogo completo do TMDB, nem listas de lançamentos ou
melhores avaliados. Não foram recuperadas credenciais do histórico.

Validação local: 152 testes e compilação Reflex `--dry` passaram; diff sem erros.
Navegador Edge headless no servidor local: 7 filmes, 3 séries e 13 livros nas
categorias. O script foi ajustado para esperar a aba selecionada e os cards,
evitando contar antes do processamento do clique. Não houve escrita remota.
