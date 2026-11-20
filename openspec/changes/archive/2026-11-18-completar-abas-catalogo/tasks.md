## 1. Exibir resultados externos sem persistir

- [x] 1.1 Complementar series, animes e livros com resultados externos somente de leitura e manter 35 por pagina; testar deduplicacao contra obras persistidas.
- [x] 1.2 Exibir resultados externos sem marcador de cadastro e esconder edicao; confirmar que nenhuma chamada de escrita ocorre.
- [x] 1.3 Cobrir consulta paginada, falha parcial do provedor, busca por termo e contagens combinadas com testes direcionados.

## 2. Validar e registrar

- [x] 2.1 Executar testes direcionados, `reflex compile --dry`, `git diff --check` e `openspec validate completar-abas-catalogo --type change`; registrar evidencias.
- [ ] 2.2 Conferir no navegador as quatro categorias, paginacao, exibicao dos resultados externos e ausencia de controles de gravacao em desktop/mobile.

## Evidencias locais (2026-11-18)

- Series, animes e livros combinam registros persistidos com resultados externos de leitura ate 35 na primeira pagina; candidatos repetidos sao ignorados.
- Resultados externos aparecem como obras comuns, sem marcador de cadastro, e nao oferecem edicao; a requisicao simulada confirma que nao ha gravacoes no Xano.
- Navegacao duplicada no topo removida; categorias continuam acessiveis pela navegacao existente.
- Testes direcionados: 13 aprovados, incluindo busca por termo, duplicidade, falha parcial de provedor e ausencia de marcador/abas redundantes.
- Consulta externa real somente de leitura: TMDB retornou 20 series, Kitsu 12 animes e Open Library 12 livros na primeira pagina.
- `.venv\Scripts\python.exe -m reflex compile --dry`: compilacao concluida com sucesso.
- `git diff --check`: passou; apenas avisos de normalizacao LF/CRLF.
- `openspec validate completar-abas-catalogo --type change`: change valida.
- A conferencia visual no navegador permanece pendente.
