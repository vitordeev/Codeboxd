# Obras iniciais nas abas — 20/10/2026

**Escopo corrigido pelo usuário:** o pedido se refere às abas do dashboard
administrativo, não à descoberta. A implementação abaixo foi retirada após
o esclarecimento. Os resultados permanecem como histórico, sem representar
o comportamento atual. A entrega correta está em
[dashboard: catálogo inicial](../changes/gerenciamento-website/validation/catalogo-inicial-2026-10-20.md).

Complemento ativo de descoberta (`specs/media-discovery/`) e confiabilidade
operacional posterior à change `corrigir-erros-operacionais`.
Pedido: exibir algumas obras nas abas Filmes, Séries e Livros do catálogo.

- [x] Consultar disponibilidade real do catálogo persistido.
- [x] Usar obras persistidas nas categorias sem termo quando o provedor falha.
- [x] Preencher destaques de filmes/séries com obras salvas quando não há populares.
- [x] Validar regressões, compilação e navegador.

GET público real `/media?per_page=50`: HTTP 200, 7 filmes, 3 séries, 1 livro e
1 anime. TMDB continua sem chave local. A implementação utiliza registros reais
do Xano, mantém o filtro por tipo e os avisos de falha dos provedores. Busca
textual continua exigindo relevância. Não foram criadas obras nem avaliações.

Validação local: 150 testes passaram (dois novos cenários cobrem as três
categorias, manutenção do tipo, vínculo da ficha e destaques com provedor
indisponível). Compilação Reflex `--dry` e `git diff --check` passaram.
Navegador Edge headless, servidor local em `http://localhost:3000/`, sem login:
ao clicar nas categorias foram exibidos 7 filmes, 3 séries e 13 livros.
Livros combinaram resultados Open Library com o catálogo salvo. Não foi
necessário configurar TMDB ou publicar mudanças no Xano.
