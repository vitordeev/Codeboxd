# Medição real de login/perfil — 20/10/2026

## Escopo aprovado

Usuário autorizou criar instrumentação/testes/registros e medir com sua conta,
digitando credenciais somente no navegador. Cenário: login e até cinco acessos
ao perfil em cada largura (1440/390), interrompendo novas chamadas no primeiro
429; não criar conteúdo ou alterar a conta. Nenhuma senha/token solicitado no chat.

`tools/real_login_measurement.py` inicia instância de produção em 3031 e proxy
local em 3041, apontando para os serviços HTTPS já configurados, sem editar `.env`.
Somente POST login e GET auth/me, mídia e perfis são encaminhados; escrita de
perfil, cadastro, recuperação e operações sociais são bloqueadas no proxy.
Máximo de 80 chamadas remotas e três tentativas manuais de login; não há retry
adicionado pelo instrumento. Chamadas já em voo ao receber 429 podem terminar,
mas novas são bloqueadas localmente. Retry-After vira segundos no relatório.

Instrumentação exporta apenas método, rota sanitizada, status, duração, offset,
contagens e tempos da interface. Não salva screenshots, vídeo, traces, cookies,
corpos ou cabeçalhos. Janela Edge usa contexto temporário. Estado Reflex de teste
é explicitamente em memória (`REFLEX_STATE_MANAGER_MODE=memory`), verificado
contra a configuração instalada. Browser bloqueia assets externos; isso limita
comparabilidade de fonte/imagens com a experiência normal.

O proxy adiciona um salto local e conexão HTTP de saída; custos entram no tempo.
Não interpretar como medição direta sem instrumentação. Primeiro acesso inclui
login manual; timestamp é observado localmente no evento submit, sem ler valores
do formulário. Demais acessos são revisitas com o estado/cache existente, sem
rotular todos como cache frio. O executor aguarda até dez minutos pelo login.

## Verificação local do instrumento

Seis testes simulados passaram: rotas permitidas/bloqueadas, parada após 429,
orçamento/limite de login, encaminhamento sem credenciais no relatório,
bloqueio antes de acessar upstream e ausência de redirecionamento externo.
Nenhuma chamada remota foi feita nesses testes. O resultado real, se houver,
será escrito em `login-real-2026-10-20.json` sem sobrescrever dados simulados.

## Estado da execução e resultado posterior

Build concluiu e usuário fez login na janela Edge. Executor finalizou com
`user_logged_in=true`, sem exceção, e `stop_reason=remote-429`.
[Resultado sanitizado](login-real-2026-10-20.json): dez respostas 200, seguidas
de um 429 na 11ª chamada remota, GET `/auth/me`, Retry-After de 20 segundos.
As 11 chamadas começaram em uma janela de aproximadamente 13,3 segundos.
Isso identifica a resposta que disparou o aviso no cenário, mas não comprova
que a quota é exclusiva do endpoint, da conta ou global da instância.

Foram cinco GET `/auth/me`, três GET de detalhe de perfil, dois GET de
referências (`media` e `profiles`) e um POST login. A segunda validação de
sessão ocorreu logo após a primeira, no acesso ao perfil pós-login. Cache
evitou repetir algumas referências, mas não evitou o limite. A coleta parou
no desktop: cinco entradas no relatório, sendo a quinta interrompida; celular
não executado. Nenhuma edição, upload ou gravação de conteúdo da conta.

O marco login→perfil foi 5.832 ms nesta amostra. Os tempos das revisitas não
devem ser tratados como latência completa confiável: o predicado atual aceita
perfil pré-existente e pode observar `busy=false` antes do evento on_load
iniciar após hidratação. São insuficientes para encerrar a linha de base ou
comparar percentis. Contagens/status/duração no proxy continuam sendo eventos
HTTP reais, independentemente dessa limitação do predicado da interface.
Uma revisão futura deve correlacionar cada visita com seu ciclo de carga.

Instância de medição e proxy encerrados pelo executor. Para restaurar a
instância normal, identificada e encerrada somente a árvore verificada
16904→1340→2912. Novo build em 3030 iniciado com configuração habitual e log
`reflex-live-after-measurement.log`. Build concluiu e env gerado voltou a 3030;
GET `/login` retornou 200 e portas de teste 3031/3041 foram conferidas fechadas.
Instância normal restaurada. IDs são históricos, não reutilizar sem verificar.

Rollback da instrumentação: retirar somente os arquivos desta intervenção e
suas referências se aprovado. Código de comportamento do aplicativo não foi
alterado. Aviso preexistente de parse de `.env` persiste, sem expor seu conteúdo.
