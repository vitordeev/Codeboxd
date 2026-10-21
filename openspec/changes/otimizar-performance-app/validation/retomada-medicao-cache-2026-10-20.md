# Retomada da medição após cache — 20/10/2026

## Trabalho autorizado

Usuário aprovou reiniciar, corrigir o marco de cada visita e repetir a medição
real. Executor passou a observar deltas do ciclo `busy=true` → perfil atualizado
→ `busy=false`, sem reter payloads WebSocket. Hidratação antiga não conclui uma
visita. Sete testes offline da instrumentação passaram, incluindo essa regressão.
Consulta ao código gerado e transporte Reflex confirmou os nomes de estado e
Socket.IO. Nenhuma alteração nova no comportamento do aplicativo nesta rodada.

O novo resultado usa `login-real-apos-cache-2026-10-20.json`, preservando a
medição anterior `login-real-2026-10-20.json`. Executor agora tenta restaurar
automaticamente a instância habitual em 3030 ao finalizar, encerrando somente
processos deste projeto identificados por comando, portas e tempo de criação.

## Falha antes de abrir navegador

Inicialização encontrou `.web/reflex.json` com versão 0.9.12, enquanto `.venv`
usa Reflex e reflex-base 0.9.11.post1. O framework tentou inicializar/recriar o
frontend e falhou com `PermissionError: [WinError 5]` ao remover
`.web/node_modules/.bin/react-router.exe`. A tentativa automática de restauração
encontrou o mesmo erro. O frontend gerado ficou incompleto após essa operação
do framework. Não foi executada exclusão manual pelo agente.

Inspeção de processos não encontrou Python, Bun ou React Router ainda mantendo
o arquivo aberto; não atribuir causa definitiva a processo ativo. Atributo do
arquivo é Archive, com ACL de modificação para usuário/grupos locais. A diferença
de versão explica a tentativa de reinicialização, mas não comprova a origem do
acesso negado. Não atualizar pacotes para contornar sem aprovação.

`pip check` passou. Versões conferidas: Reflex 0.9.11.post1,
reflex-base 0.9.11.post1, components-core 0.9.9 e Playwright 1.64.0.
Resultado sanitizado da tentativa: zero chamadas remotas, zero amostras, sem
login, `failure=RuntimeError` e `normal_restored=false`. Nenhuma evidência de
redução de HTTP 429 real nesta rodada. Servidor normal ficou parado.

## Aprovação pendente

Solicitado ao usuário preservar `.web` em cópia dentro de `.local/` e gerar
frontend novo com a versão instalada. Motivo: recuperação reversível dos
artefatos gerados, sem alterar código, `.env`, uploads ou dados de conta.
Não executar essa movimentação antes da resposta; conferir caminhos absolutos
dentro do workspace antes de mover, preservando a pasta anterior.

Depois da recuperação aprovada: iniciar teste, solicitar login manual, medir,
restaurar execução normal e registrar cada resultado. Enquanto isso, manter
tarefas de validação real abertas.

## Recuperação aprovada na rodada seguinte

Usuário autorizou preservar/recriar. Caminhos absolutos foram verificados
dentro do workspace, e `.web` foi movida (sem exclusão) para
`.local/web-before-recovery-20261020-121044`. A movimentação foi concluída
sem alterar ACL, uploads, `.env` ou código de produto.

`reflex compile --dry` inicializou frontend novo e compilou com sucesso.
`.web/reflex.json` confirmou versão 0.9.11.post1, alinhada à `.venv`.
Sete testes da instrumentação passaram novamente. Resultado da tentativa
anterior preservado em
[login-real-apos-cache-inicializacao-falhou-2026-10-20.json](login-real-apos-cache-inicializacao-falhou-2026-10-20.json).

Executor real retomado com aprovação de execução escalonada. Build de produção
concluiu e log confirmou app na porta 3031. Janela Edge visível aberta para
login manual, solicitado ao usuário. Ainda sem novo resultado de performance
neste checkpoint. Executor restaurará app normal em 3030 ao terminar; conferir
resultado e disponibilidade efetivos na conclusão.

Resultado posterior confirmado: dez visitas e nove chamadas 200, sem 429;
instância normal restaurada e conferida. Ver
[relatório final desta rodada](resultado-login-real-apos-cache-2026-10-20.md).
