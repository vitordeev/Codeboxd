# Retomada para conclusão — 23/10/2026

Usuário pediu terminar a change de performance, seguindo sua documentação.
Preservar IDs e critérios originais, inclusive validação real; não arquivar
com verificações obrigatórias ausentes. As alterações da rodada anterior estão
preservadas no working tree.

## Plano antes das alterações

1. Instrumentar uma medição pública isolada da home usando os handlers reais,
   sem autenticação e sem a seção comunitária Xano. Cinco amostras frias e
   aquecidas, tempos individuais, mediana/pior e chamadas por serviço; registrar
   primeiro conteúdo e conclusão separadamente. É medição Python/provedores,
   não navegador nem jornada autenticada. Usar timeout por amostra e interromper
   novas amostras ao primeiro 429 ou falha; nunca persistir headers ou conteúdo.
2. Corrigir classificação do domínio atual `kitsu.app` na instrumentação,
   mantendo o domínio legado reconhecido; testar que hosts semelhantes não
   sejam classificados como Kitsu.
3. Executar regressões pertinentes e as verificações aplicáveis. Caso a rede
   restrita impeça medição real, solicitar execução com rede pelo mecanismo
   de permissões, sem registrar falha de rede como sucesso funcional.
4. Validações autenticadas aguardam login manual de contas adequadas. Pergunta
   enviada ao usuário; não extrair senhas, fabricar sessões ou promover contas.

Arquivos: `tools/public_home_measurement.py`, `tools/performance_probe.py`,
testes de instrumentação e medição, tasks.md e evidências desta change.
Escopo coberto pelas tarefas 1.2/1.3/1.4 e 4.1/4.4. Risco: quota pública e
dependência de provedores; limitar cinco pares, interromper em falha/429,
sem retries novos. Rollback: remover o executor e apenas a classificação nova.
Não alterar contratos remotos, dados ou processo do servidor nesta etapa.

## Resultado público e próxima verificação

`home-publica-2026-10-23.json`: 22 falhas de rede na execução restrita;
nenhum resultado funcional aceito. Execução com rede autorizada preservada
separadamente em `home-publica-rede-2026-10-23.json`: cinco pares completos,
110 respostas 200 e nenhuma 429. Mediana/pior do primeiro conteúdo frio:
538,569/809,641 ms; aquecido: 27,853/46,393 ms. Conclusão fria:
5930,250/8384,601 ms; aquecida: 29,722/50,957 ms. Chamadas: 22 frias e zero
aquecidas em todos os pares. Nenhum reinício ou browser nessa medição.

Custo de requisição por serviço nas amostras frias (durações HTTP, sem somar
como tempo de página, pois há concorrência): TMDB 50 chamadas, mediana
453,81 ms/pior 565,139 ms; Kitsu 15 chamadas, 894,87/1459,245 ms;
Open Library 45 chamadas, 1218,98/5867,924 ms. Conteúdo principal foi publicado
sem esperar o provedor mais lento. O compartilhamento de consultas concorrentes
foi aprovado pelo pedido atual de otimização/conclusão e sua regressão está em
`catalogo-concorrente-2026-10-23.md`; não atribuir ganho de cache histórico a esse
incremento novo.

Metas numéricas propostas ao usuário após a linha de base; aprovação ainda
pendente. Não completar 1.5 nem 4.4 por essa proposta.

Próxima etapa local autorizada pelo pedido de conclusão: repetir os oito cenários
de feed/listas em 1440/390px usando `tools/feed_lists_browser.py`, com backend
fictício e diretório de frontend isolado já existente, saída nova nesta change.
O executor mantém o servidor normal intacto e encerra somente seu subprocesso.
Escopo: regressão de jornada 9.1; não substitui persistência ou performance real.

## Resultado do navegador e conclusão local

- `feed-listas-browser-2026-10-23/result.json`: tentativa restrita não iniciou
  casos, por bloqueio de escrita no cache npm. Registro e log preservados.
- `feed-listas-browser-rede-2026-10-23/result.json`: **8/8 aprovados**, 1440/390px,
  sem erros JavaScript ou overflow. Backend local fictício; edição, remoção de
  referência, busca/inclusão sem duplicação e inclusão pela ficha preservadas.
  Build de produção isolado concluído em aproximadamente 14 segundos. Servidor
  normal não modificado; subprocesso de teste encerrado pelo executor.
- Regressão nova da home confirmou destaque de cinema, capa preservada, ordem
  das quatro séries sem duplicatas e falha isolada de uma categoria de livros.
  Nove testes dirigidos da home aprovados. Instrumentação tem três regressões
  novas (execução do handler sem Xano, interrupção em 429 e timeout sem sucesso
  fabricado); classificação de Kitsu atual/legada e host impostor verificada.
- `.venv/Scripts/python.exe -m unittest discover -s tests`: **315 testes
  aprovados**, 9,557 segundos na execução final.
- `openspec validate otimizar-performance-app --type change` e
  `git diff --check`: aprovados no fechamento; somente avisos LF/CRLF.
- Build alterou automaticamente apenas `reflex.lock/package.json` entre os
  arquivos rastreados de dependência. Estava limpo antes desta execução; seus
  bytes originais foram restaurados de HEAD após conferir o diff. Nenhuma
  atualização de dependências integra a entrega.

Tarefas 4.1/4.2 concluídas por diagnóstico real por provedor e incremento local
autorizado, com regressões/compilação. Estado **13/37**. Não concluir 4.4, 1.3,
1.5 ou 9.1: faltam metas aprovadas, viewport/cache no browser real e demais
jornadas. Consulta de login manual e proposta de metas enviadas ao usuário;
nenhuma resposta recebida até este registro. Não arquivar nem sincronizar uma
aceitação global de performance enquanto esses critérios estiverem abertos.

## Autorização posterior e próxima execução

Após o relatório e o pedido de logins/aprovação das metas, o usuário respondeu
“então faça”. Considerado autorização para preparar as janelas interativas e
aprovação das metas propostas da home: mediana fria de até 1000 ms no primeiro
conteúdo e 10000 ms na conclusão; aquecida de até 200/500 ms; até 22/0 chamadas
fria/aquecida. Todas atendidas na medição Python/provedores já registrada; não
extrapolar para browser ou outras jornadas. 1.5 continua aberta pelo orçamento
das demais jornadas ainda não medido/aprovado.

Executar primeiro `tools/admin_reads_remote.py` com saída nova nesta change,
login manual de admin ID 14 ativo, leituras limitadas, sem mutações. Dependência
com gerenciamento-website preservada; execução vinculada ao diagnóstico 8.1.
Adicionar métricas sanitizadas de duração por requisição ao executor, mantendo
limite de 40 chamadas e interrupção em 429. Testes devem conferir ausência de
credenciais, payloads, query e nomes privados no resultado. Não altera contratos
ou servidor Reflex; rollback remove apenas as métricas extras.

Primeira execução admin: login legítimo confirmado, 23 checks aprovados e
11 chamadas totais (dez 200, uma 429 em GET `/admin/catalog`). Executor parou
sem retry; relatório `admin-real-2026-10-23.json`. Token descartado conforme
workflow original. Não inferir quota global exata a partir dessa ocorrência.

Retomada diagnóstica: incluir Retry-After normalizado em 429 e opção `--pause`,
usar três segundos entre chamadas numa execução nova, mantendo 40 chamadas,
interrupção imediata em 429 e novo login manual. O intervalo conservador é um
experimento do executor, não aumento de quota nem alteração do produto.

Próximo diagnóstico de membro: reutilizar formulário loopback e descarte de
token do executor, parametrizando apenas o tipo de probe e rótulo do login.
Novo `tools/member_reads_remote.py` aceita somente membro ativo, mede cinco
amostras de sete leituras (perfil próprio, primeira página da biblioteca,
listas próprias/públicas, feed, posts próprios e comunidade), intervalo 3 s,
limite 40 chamadas incluindo login, sem writes ou dados de teste. Conferir
formato e status sem salvar conteúdo, nomes, IDs pessoais ou tokens. Sem cache
de aplicação ou viewport, o resultado é diagnóstico API, não aceitação de
tempo da jornada no navegador. Cobertura parcial 1.3/6.4/7.1/9.1.

Resultado administrativo com intervalo de 3 s:
`admin-real-intervalo-2026-10-23.json`, **44 checks aprovados**, 18 respostas
HTTP 200 e nenhum 429. Mediana das leituras 261,382 ms; pior 4156,909 ms.
Inclui login/autorização, dashboard, usuários e filtros, quatro tipos de
catálogo, reports e filtros. São leituras API, não operações de gravação,
auditoria, medições de viewport ou demonstração administrativa no navegador.

Regressões após os instrumentos: **318 testes aprovados**, 12,455 s.
`openspec validate otimizar-performance-app --type change` e `git diff --check`
aprovados, somente avisos LF/CRLF. O executor de membro foi iniciado em janela
Edge visível e aguarda login local; testes offline não comprovam essa etapa real.

## Login de membro e desconexão do formulário

Usuário confirmou que realizou o login de membro. Login/autorização foram
aceitos e as consultas prosseguiram com checks aprovados. Ao responder à página
local, Windows abortou uma conexão (`ConnectionAbortedError`); a captura genérica
do formulário a classificou incorretamente como `login_failed` e tentou escrever
novamente no socket fechado. Não houve evidência de senha incorreta.

Correção do instrumento, vinculada a 1.2: tratar somente erros de desconexão
durante envio da página como desconexão de cliente e sinalizar autenticação
aceita antes de responder. Preservar falhas reais de autenticação e dados em
memória. Testar escrita/headers abortados sem propagação. A execução em andamento
mantém seu código original; não editar seu JSON para apagar a ocorrência.

## Resultado final de membro

`membro-real-2026-10-23.json`: **70 checks aprovados**, 39 respostas HTTP 200,
nenhum 429. São 35 leituras (sete endpoints × cinco amostras), além de duas
sequências de login/validação. O orçamento de 40 chamadas foi respeitado.
O relatório bruto conserva `failure_type=login_failed` da desconexão de página
descrita acima; `passed=true`, todos os 70 checks e todos os status 200 comprovam
que a autenticação e as leituras foram bem-sucedidas. Não apagar a inconsistência
histórica do arquivo. O tratamento foi corrigido para as execuções futuras.

| Leitura | Mediana HTTP (ms) | Pior amostra (ms) |
| --- | ---: | ---: |
| Perfil próprio | 233,196 | 250,902 |
| Biblioteca, primeira página | 205,523 | 3330,577 |
| Listas próprias | 196,440 | 559,102 |
| Listas públicas | 263,995 | 769,025 |
| Feed | 201,786 | 2680,402 |
| Posts próprios | 195,406 | 286,923 |
| Comunidade | 185,957 | 783,924 |

Valores são tempo HTTP sem a espera artificial de 3 s entre chamadas. Não são
tempo de renderização, percentil representativo, comparação antes/depois nem
aceitação da jornada completa. Biblioteca foi conferida como pertencente ao
membro autenticado; não foram criados itens, contas ou coleções grandes para
alegar cobertura de paginação/isolamento entre duas contas.

1.2 concluída: instrumentos, arquivos de evidência e execução interativa foram
propostos, autorizados antes da execução e validados, sem dados fictícios na
API real nem necessidade de reiniciar o servidor. Scripts de navegador existentes
permanecem separados das leituras API. Estado **14/37**; demais tarefas abertas
preservam seus critérios de browser, mutações, metas e comparações completas.

Validação após a correção do formulário: **319 testes aprovados** em 7,795 s;
`openspec validate otimizar-performance-app --type change` e `git diff --check`
aprovados. O teste novo cobre desconexão ao escrever headers/corpo da página,
sem reclassificá-la como rejeição de credenciais. Execução de membro encerrada,
token descartado e janela fechada pelo executor.
