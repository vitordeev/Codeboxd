# TMDB: restauração com acesso de rede — 20/10/2026

## Relato, causa e correção

Usuário relatou que a API TMDB não retornava várias seleções depois da rodada
anterior. O servidor normal havia sido relançado pelo agente dentro do ambiente
com rede restrita. HTML local/fixtures funcionavam, mas conexões externas do
backend falhavam com ConnectError. O smoke HTTP 200 da restauração anterior
comprovava apenas a disponibilidade local, não acesso aos provedores.

Reprodução isolada: TMDB_READ_TOKEN configurado (valor não exibido), sem proxy
HTTP/HTTPS/ALL no ambiente; GET TMDB falhou com WinError 10013, acesso ao socket
proibido. Logs do app registravam ConnectError para TMDB, Kitsu e Open Library.
Não houve evidência de chave inválida, HTTP 401 do TMDB ou lista vazia legítima.

Após aprovação de execução com rede, quatro consultas autenticadas TMDB
responderam HTTP 200, com 20 resultados cada: movie/now_playing,
movie/top_rated, movie/upcoming e tv/popular; idioma pt-BR/região BR.
Somente método/caminho público, status e quantidade foram exibidos.

App normal reiniciado em produção na porta 3030 por processo autorizado com
acesso de rede; apenas launchers Reflex deste workspace/porta foram substituídos,
por identidade de PID e horário de criação. Log local normal-restored-tmdb-network.log.
Chaves, .env, contratos Xano e código de produto não foram alterados.

## Validação real no navegador

Ferramenta tools/check_tmdb_browser.py executada no Edge headless em 1440px,
contra o app normal com TMDB real, sem fixtures. Resultado sanitizado em
[tmdb-rede-browser-2026-10-20.json](tmdb-rede-browser-2026-10-20.json):

| Fileira | Cards |
| --- | --- |
| Agora nos cinemas | 20 |
| Filmes muito bem avaliados | 20 |
| No radar: próximos filmes | 20 |

Essa evidência comprova retorno das três seleções; não encerra medições de
performance de todas as jornadas, quota, autorização administrativa ou testes
dos demais provedores. Não houve gravação Xano, login ou envio de e-mail.

## Prevenção e testes

tools/real_login_measurement.py passa a verificar transporte externo por HEAD
público sem credenciais antes de substituir o app normal. Em bloqueio, retorna
false com mensagem explícita e não encerra nem relança o servidor existente.
O HEAD verifica conectividade, não valida chave, payload ou todos os provedores.

tools/performance_continuation_browser.py verifica conectividade antes de criar
resultados/iniciar o servidor de teste ou mudar o frontend gerado. Isso impede
que este executor volte a produzir a restauração restrita observada. Executores
históricos que não fazem preflight inicial ainda exigem cuidado operacional;
todos que usam restore_normal_app recebem a proteção na restauração.

Quatro novos testes offline aprovados em test_normal_app_restoration.py:
preservação do processo em bloqueio, HEAD sem segredo, tratamento de falha de
conexão e bloqueio antecipado do executor de navegador. Sete testes existentes
de test_real_login_measurement.py também passaram (11 testes pertinentes).
Sem recompilar o produto nesta correção de utilitários; o reinício aprovado
fez build de produção. Os 259 testes da rodada anterior são evidência histórica,
não uma suíte completa reexecutada neste atendimento.

## Operação e rollback

Executar o app normal em terminal com acesso aos provedores. Quando a ferramenta
do agente estiver sob restrição de rede, pedir execução autorizada fora dessa
restrição; não remover proteções nem alterar chaves para contornar o bloqueio.
Verificar pelo menos uma consulta pública real e a UI após restaurar o processo.
HTTP 200 de uma página estática isoladamente não comprova integração disponível.

Rollback de utilitários: reverter apenas as guardas de conectividade e remover
o novo teste/ferramenta de conferência; não voltar a iniciar app normal no
contexto restrito. Não há migração de dados. Change mantém 11/37 tarefas;
esta correção operacional não encerra critérios globais de performance.
