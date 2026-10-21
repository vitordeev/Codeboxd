# Perfil no navegador com dados locais — 20/10/2026

## Autorização e ambiente

Usuário autorizou instalar `requirements-dev.txt` e prosseguir com validação
desktop/celular. Instalação no sandbox falhou por rede inacessível; reexecução
escalonada aprovada instalou Playwright 1.64.0, pyee 14.0.0 e greenlet 3.5.6 e
alinhou python-dotenv de 1.2.4 para 1.2.3, conforme requirements.txt. Nenhum
arquivo de dependências foi alterado. `pip check` passou e 188 testes passaram
novamente após a instalação.

Criado `tools/profile_browser_validation.py`: serviço HTTP local fictício em
3040 e instância Reflex de produção em 3031, com XANO_AUTH_URL/XANO_SOCIAL_URL
substituídos somente no ambiente do processo filho. `.env` não alterado. O
serviço responde com usuário, mídia e relações sintéticas; demais endpoints
retornam 404. Browser bloqueia URLs externas. Sem acesso a contas Xano reais,
gravação remota ou envio de e-mail. Edge headless instalado, controlado pelo
Playwright. Logs locais ignorados em `profile-browser-server.log`.

Execução, pela raiz:

```powershell
.venv/Scripts/python.exe -B tools/profile_browser_validation.py
```

Não executar concorrentemente com outra compilação do projeto: o build atualiza
`.web/env.json` e os artefatos frontend compartilhados. Após encerrar teste, a
instância normal precisa de novo build na porta habitual. Processos da instância
de teste e descendentes são encerrados pelo executor, e o fixture é desligado.

## Resultado de navegador

Seis casos passaram na execução final:

| Viewport | Caso | Perfil visível após clicar em Entrar | Editor durante espera |
| --- | --- | --- | --- |
| 1440 × 900 | Catálogo com atraso de 3 s | 2.511 ms | Abriu/fechou antes de terminar |
| 1440 × 900 | Pessoas com atraso de 3 s | 1.471 ms | Abriu/fechou antes de terminar |
| 1440 × 900 | Catálogo com 429/20 s | 1.460 ms | Abriu/fechou; sem espera injetada |
| 390 × 900 | Catálogo com atraso de 3 s | 1.478 ms | Abriu/fechou antes de terminar |
| 390 × 900 | Pessoas com atraso de 3 s | 1.417 ms | Abriu/fechou antes de terminar |
| 390 × 900 | Catálogo com 429/20 s | 1.420 ms | Abriu/fechou; sem espera injetada |

Cada caso usou contexto de browser novo e login sintético pelo formulário real.
Confirmados: identidade visível durante complementos pendentes; status de
carregamento por seção; atividades/seguidores carregados ao finalizar; aviso
de 20 segundos dentro de atividades quando catálogo falha; perfil e seguidores
preservados. Sem pageerror JavaScript ou overflow horizontal nos seis casos.
Dialog de edição abriu/fechou, sem salvar ou enviar upload.

A primeira execução já passou os seis casos, mas testava edição somente após
concluir referências. Foi repetida com a verificação durante a espera para
cobrir a dúvida de interatividade identificada na rodada anterior. JSON final
em [perfil-browser-2026-10-20.json](perfil-browser-2026-10-20.json). Tempos são uma
amostra por cenário da execução final, não percentis nem benchmark com Xano real.

Capturas `perfil-<largura>-<caso>-loading.png` e `*-final.png` nesta pasta.
Foram inspecionadas visualmente a captura desktop durante carregamento e a
mobile final. [Desktop em espera](perfil-1440-slow-media-loading.png),
[celular completo](perfil-390-slow-media-final.png) e
[celular com 429](perfil-390-media-429-final.png).

## Restauração da instância normal

Build de teste alterou configuração gerada para 3031. Foram identificados os
processos da instância normal antiga (5168/5192) e encerrados para restaurar
3030. O primeiro reinício encontrou log bloqueado; o seguinte detectou porta
ocupada por socket herdado. Inspeção identificou worker órfão 18648, filho de
5192 com comando `multiprocessing.spawn`. Somente esse worker foi encerrado
após verificar parentesco/comando, e novo build normal foi iniciado com log
`reflex-restored-final.log`. Não foram encerrados processos de outros programas.
Build concluiu: log confirmou app rodando em 3030, `.web/env.json` voltou a
apontar para 3030 e GET local `/login` retornou 200. As portas de teste 3031 e
3040 foram conferidas como fechadas. Instância normal permanece em execução.

## Limites

Validação comprova UI e integração frontend/backend com serviços locais
fictícios. Não comprova quota remota, latência real, salvamento de perfil,
outras contas, todas as telas nem redução do volume de requisições. O alerta
preexistente de parse da primeira linha do `.env` continua sem alteração.
Metas reais e tarefas amplas da change continuam abertas. Nenhuma nova alteração
de comportamento do app foi feita nesta rodada; mudança foi no ambiente de
testes, executor e evidências. Próxima intervenção deve ser proposta e aprovada.
