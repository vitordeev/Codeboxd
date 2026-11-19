# Repetição após sucesso — 10/11/2026

## Diagnóstico remoto somente de leitura

Histórico Xano mostrou emissão do código às 14:30 UTC, validação magic-link-login HTTP 200 às 14:34:04 UTC e update_password HTTP 200 às 14:34:05 UTC (11:34 em São Paulo). Três tentativas seguintes do validador retornaram 401. Comparação em memória confirmou mesmo e-mail e código nas três repetições; nenhum valor foi impresso ou persistido. Não houve alteração remota de dados nesta investigação.

O código correto foi aceito e consumido, seguido de troca concluída. A interface anterior permitia novo submit depois do sucesso e substituía a confirmação pelo erro da reutilização. Usuário relatou recebimento do código e erro; confirmação de login com nova senha solicitada e ainda pendente.

## Correção local

SessionState mantém reset_completed após confirmação da troca. Novo submit retorna sem chamadas HTTP nem apagar sucesso. Botão desabilitado apresenta “Senha atualizada”; link para login existente preservado. Novo pedido explícito e válido de código reinicia a jornada. Segurança e uso único do Xano mantidos.

Documentação consultada pelas skills reflex-docs e reflex-process-management: [estado](https://reflex.dev/docs/state/overview/) e [eventos](https://reflex.dev/docs/events/events-overview/).

## Validações

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_password_recovery.py -q`: 9 testes passaram, incluindo repetição sem requisições e reinício por novo pedido.
- `.venv/Scripts/python.exe -m reflex compile --dry`: compilação aprovada.
- Instância identificada com `venv/Scripts/reflex.exe run` (modo de desenvolvimento), backend ouvindo em 8000. Não reiniciada nem convertida para produção; esse processo admite recarga automática, mas comportamento atualizado no navegador não foi verificado.
- Não houve nova solicitação de código, login com credenciais do histórico, alteração de senha ou publicação Xano nesta correção.

Entrega/consumo/troca no Xano observados no teste do usuário não substituem confirmação de novo login, senha antiga rejeitada e demais critérios de 3.2. Manter tarefa aberta.
