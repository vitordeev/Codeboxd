# Conclusao - 04/11/2026

Change completa: **10/10**. A tarefa 3.2 reune o aceite de API publicado em
03/11 e o aceite de navegador final desta rodada. Migracao, concorrencia,
paginacao de 102 itens e preservacao de avaliacoes/personalizadas estao nas
evidencias de API anteriores; nao foram reexecutadas nem somadas como novos testes.

## Navegador real

`tools.list_status_browser_fixtures setup` criou duas contas pelo signup normal,
uma obra e um post descartaveis. O leitor nao tinha posts, conexoes ou status de
lista no inicio. Journal privado separado em
`.local/conexoes-feed-listas/browser-2026-11-04/`.

`tools.list_status_browser --frontend-workdir .local/frontends/status-real-15580
--private-dir .local/conexoes-feed-listas/browser-2026-11-04
--output openspec/changes/corrigir-conexoes-feed-listas/validation/browser-real-2026-11-04-attempt3.json`
aprovou tres cenarios: seguir autor e carregar feed sem posts proprios;
alternar/remover status exclusivo, recarregar e revisitar em 1440px; repetir
os controles e persistencia em 390px. Sem erro JavaScript ou overflow.

63 chamadas pelo proxy, zero 429. `/likes` retornou 404; o fallback existente
preservou a jornada. Proxy de validacao com intervalo minimo de 2,4 s e timeout
de transporte de 60 s: isto nao comprova performance do produto sem proxy.
Servidor separado em producao local 3035, encerrado no finally; servidor normal
preservado. Screenshots e diagnosticos ficaram somente em .local.

Primeira tentativa preservada: AssertionError com limite padrao de 5 s nas
assercoes. Corrigido apenas o executor para usar 120 s tambem no expect.
Segunda tentativa: timeout de prerender na geracao do build, antes de requisicoes
remotas. Terceira tentativa completa aprovada. Navegacao interna por links
funcionou; nao houve correcao de infraestrutura ou promessa sobre acesso HTTP
direto a URLs dinamicas, achado separado da rodada anterior.

`tools.list_status_browser_fixtures cleanup` terminou com
`fixture_cleanup_complete=true`: exclusoes por IDs proprios, resposta de bulk
confirmada com success_total para cada conjunto. Duas contas, uma obra, post,
interacao, conexao e listas de teste removidos; journal de usuarios/obras vazio.
Nenhuma republicacao ou migracao nessa validacao.

## Verificacao local

- `.venv/Scripts/python.exe -B -m unittest discover -s tests`: **482 OK**, 69,170 s.
- Build de producao isolado da tentativa final aprovado, compilacao 7 s e build 29 s.
- `openspec validate corrigir-conexoes-feed-listas --type change`: aprovado.
- As tres skills Reflex exigidas foram lidas; ambiente .venv com Reflex 0.9.11.post1.
- Sem Docker; sem alteracao de provedores, senhas existentes ou privilegios.

Requisitos novos: confirmacao idempotente de follow, feed independente de
publicacao propria e exclusividade das listas padrao. Sincronizar esses tres
requisitos nas respectivas specs principais antes do arquivo, preservando
todos os requisitos/cenarios preexistentes.
