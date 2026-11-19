# Busca e detalhe de listas — validação local (16/11/2026)

## Escopo

Aceite local das tarefas 4.2 e 4.3 da change `modernizar-ui-ux-codeboxd`,
usando fixtures sintéticas e contratos simulados. Nenhuma chamada foi feita ao
Xano real, nenhuma conta ou lista real foi usada e nenhum contrato foi publicado.

## Implementação verificada

- Busca paginada de pessoas e listas públicas mantém consulta, filtros e página
  no endereço; cada escopo consulta somente seu endpoint após submissão.
- Resultados de listas incluem autoria na resposta, sem fanout de perfil por
  resultado (sem N+1); nomes longos continuam dentro do viewport de 390 px.
- A busca distingue vazio, indisponibilidade parcial e HTTP 429. O cooldown
  respeita `retry_after` no escopo limitado sem bloquear o outro escopo.
- O detalhe de lista é endereçável, carrega página de itens, mantém estado
  vazio e oferece link de obra. Falha de clipboard deixa o endereço selecionável.
- A camada local separa detalhe público e contexto autenticado do proprietário;
  mudança de sessão/visibilidade descarta resposta ou conteúdo público obsoleto.

## Evidências

- Testes direcionados: `test_list_details.py` (12), `test_unified_search.py`
  (13) e `test_social_ui_components.py` (7), total de **32 aprovados**.
- Navegador com fixture: `.local/ui-search-task-4-2-20261116-acceptance-final8/result.json`
  — **11 casos aprovados**, zero erros JavaScript. Inclui paginação, histórico,
  detalhe direto, segunda página, lista vazia, cópia/fallback, nomes longos,
  ausência de N+1, recuperação após falha parcial e cooldown em Pessoas/Listas.
- Harness: `python -B -m py_compile tools/ui_unified_search_browser.py` e
  `git diff --check` aprovados.
- Aplicação: `reflex compile --dry` aprovado.

## Limites e próximos contratos

O teste de browser não valida serviço remoto. Privacidade de lista privada,
projeção pública, autorização de proprietário e perda de acesso após mudança de
visibilidade foram cobertas localmente com mocks e verificações dos arquivos
XanoScript; não comprovam que esses contratos estejam publicados ou corretos no
destino remoto. Publicação/revisão independente e aceite integrado com contas
controladas permanecem nas tarefas 5.2–5.4. O ensaio em dispositivo touch físico
permanece separado na tarefa 3.2.
