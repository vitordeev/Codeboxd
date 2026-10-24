# Jornada principal autenticada — 24/10/2026

## Plano antes da implementação do executor

Usuário aprovou realizar a prioridade proposta: buscar obra, avaliar, conferir
biblioteca, criar/editar lista e adicionar/remover obra, criar/editar/excluir
post de teste, conferir perfil e sair. Change ativa `otimizar-performance-app`,
14/37; Git inicialmente limpo no commit 8571c0d. Cobertura 5.3/6.3 e parcial
5.4/6.4/7.3/9.1; não encerrar tarefas amplas por um único cenário.

Usar servidor normal já disponível em 3030, sem reinício ou build. Login manual
em janela Edge temporária, somente membro ativo. Token obtido da sessão real
do próprio navegador e confirmado por `/auth/me`; nunca fabricar identidade.
Testar 1440 e 390px na mesma sessão; logout ao final. Pausas de 22 s entre
etapas para não repetir o burst de 429 observado. Não alterar o transporte do
produto ou atribuir pausas do executor à performance do aplicativo.

Executor novo `tools/main_journey_browser.py` e testes offline de seus limites.
Instrumentar tempos de ação e contagens/bytes WebSocket do navegador; chamadas
API feitas para conferir persistência serão registradas separadamente. **Não
afirmar que o navegador mede as chamadas Python do servidor normal.** Sem
screenshots, traces, cookies, credenciais, corpos de resposta, nomes de conta
ou conteúdo existente nos relatórios. Exceções registradas somente por classe
e etapa para não copiar DOM privado das mensagens do Playwright.

Antes de mutações: confirmar acesso de metadados já configurado privadamente,
ler tabelas necessárias e snapshots em memória dos registros existentes da
conta. Escolher obra já persistida, sem interação desse membro. Gravar crítica
com marcador aleatório e notas 4,5/3,5; nenhuma avaliação anterior será editada.
Listas e posts serão novos, com o mesmo marcador; preservar ID ao editar.
Não criar mídia, conta, privilégios ou schema. Journal privado em `.local/`
com marcador e IDs necessários para recuperar limpeza, sem token/senha.

Conferir gravações pela API e restauração em bloco `finally`. Como não há DELETE
público de interação, usar metadados somente para limpar fixtures cuja autoria,
marcador e ausência no snapshot original forem confirmados. Nunca remover IDs
preexistentes, nem executar limpeza por título genérico. Comparar hashes dos
registros originais da conta antes/depois. Recusar mutações se a pré-verificação
de limpeza não estiver disponível. Interromper a jornada ao primeiro erro/429,
respeitando Retry-After antes da limpeza; nenhuma gravação será repetida
automaticamente. Limites de paginação, chamadas e tempo por etapa no executor.

Validar primeiro as salvaguardas offline. Depois executar com rede/navegador
autorizados e pedir apenas a interação de login. Registrar todos os resultados
e manter abertos critérios sem evidência. Risco: falha entre gravação e resposta;
o marcador permite recuperar fixtures mesmo sem receber o ID. Rollback do
instrumento: remover somente executor/testes novos; recuperação de dados sempre
pela limpeza restrita descrita, sem restaurar tabelas inteiras.

Preparação: seis testes offline aprovados em
`tests/test_main_journey_browser.py`: exclusão de obra já avaliada como candidata,
limpeza somente de registros novos/marcados/autoria correta, proteção de IDs
originais, detecção de alteração externa sem apagar o registro, 429 sem retry
e métricas sanitizadas, ausência de limpeza antes da pré-verificação.

Servidor 3030 e credenciais locais de metadados presentes foram confirmados por
checagens somente de leitura. Não foi necessário reiniciar ou compilar o app.

## Validação local e primeira tentativa real

A suíte completa executada nesta rodada aprovou **333 testes** (45,803 s),
incluindo as seis salvaguardas do executor. `git diff --check` e
`openspec validate otimizar-performance-app --type change` passaram.

A [primeira tentativa](jornada-real-2026-10-24.json) expirou aguardando a
navegação para `/conta`: o usuário informou ter entrado como administrador
por engano. Nenhuma etapa da jornada ou chamada de verificação foi executada;
não houve criação de fixtures nem necessidade de limpeza remota. O campo
`passed: false` descreve a execução interrompida, sem provar falha funcional
do aplicativo. Uma segunda tentativa usa arquivo separado para preservar
essa evidência e exige login manual de membro novamente.

A segunda tentativa também foi interrompida em `manual-login`, com erro do
Playwright e sem chamadas de verificação ou mutações. O relatório registra
apenas a classe `Error`; não permite determinar a causa exata. Para distinguir
espera do login de erro de pré-verificação na próxima execução, o executor
passa a registrar uma etapa explícita `member-preflight`, sem mensagem de erro
ou DOM. Os seis testes de salvaguarda e a validação OpenSpec passaram novamente.

## Pausa para atualização do repositório

Usuário pediu parar para executar `git pull`. A terceira tentativa foi
encerrada antes do login; relatório em
`jornada-real-2026-10-24-tentativa-3.json`, com zero etapas e zero chamadas de
verificação. As três tentativas preservadas não fizeram mutações remotas.
Executor encerrado; servidor normal não foi reiniciado. Ferramenta, testes e
evidências permanecem como alterações locais sem commit. Não foi executado
pull, stash ou commit pelo agente. Retomar a validação real após atualizar o
repositório e conferir novamente seu estado e a versão em execução.
