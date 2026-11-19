# Elegibilidade da recuperação — 10/11/2026

## Resultado

Endpoint publicado rejeita e-mail sem conta ativa com HTTP 404 antes da função geradora e do SendGrid. Interface mantém endereço e etapa inicial com mensagem “Não encontramos uma conta ativa com esse e-mail. Confira o endereço ou crie uma conta.” Erro 400 de envio também deixa de ser convertido em sucesso. Fluxo de conta ativa, cooldown e template existentes preservados.

Isso verifica cadastro ativo no Codeboxd, não existência ou recebimento de caixa externa. A decisão anterior de ocultar a existência de contas foi substituída por solicitação explícita do usuário, com consequência comunicada: o fluxo agora permite inferir se há conta ativa. Nenhuma consulta pública de usuários ou detalhe de conta adicionado.

## Implementação e contratos

- Consulta mínima id/account_status no endpoint; rejeição precede geração de código e envio.
- SessionState trata 404 e 400 como erro, sem marcar sucesso/avançar. 404 preserva o endereço e limpa etapa de código; não ativa cooldown local de sucesso.
- Executor `tools/recovery_email_release.py` aceita --change com nome validado, diretórios privados/relatórios separados e change planejada obrigatória, preservando evidências de publicações anteriores.
- Deltas ativos das changes recuperar-senha-codigo-6-digitos e simplificar-pagina-recuperacao reconciliados por nota datada e atualização de cenários; evidências históricas mantidas.

## Verificações

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_password_recovery.py -q`: 16 testes passaram. Contempla avanço de conta ativa com transporte simulado, 404 sem avanço/endereço preservado, 400 sem sucesso falso, cooldown, eventos e troca de senha existentes.
- `.venv/Scripts/python.exe -m reflex compile --dry`: compilação aprovada.
- `.venv/Scripts/python.exe -B -m tools.recovery_email_release --change impedir-recuperacao-email-sem-conta`: sandbox SendGrid 200 sem entrega e prévia Xano 200 com apenas uma query. [Relatório](preview.json).
- Mesmo comando com --apply: assinatura conferida e backup privado sem segredos em `.local/impedir-recuperacao-email-sem-conta/before-without-secrets.xs`; publicação 200 e exportação posterior confirmou apenas o endpoint de solicitação alterado, env/records false. [Relatório](deployment.json).
- Requisição real com endereço aleatório no domínio reservado example.invalid retornou 404. Sem registro de endereço/código ou chamada ao provedor. [Resultado](api-validation.json).
- Playwright/Edge headless em localhost:3000/redefinir-senha, 390x900: preenchimento de outro endereço sintético e submit usando backend publicado. Erro de conta ativa exibido, primeira etapa e um input visível, sem campo de código, endereço preservado e botão habilitado para correção. [Resultado](browser.json). Screenshot privado `.local/missing-reset-account-mobile.png`.

## Limites

Não foi solicitado novo código para conta real nem enviada mensagem real, criada conta ou alterada senha. Caminho ativo verificado por regressões simuladas e preservação de contrato, não por nova entrega de e-mail nesta rodada. Atrasos Gmail por autenticação do domínio continuam no escopo de melhorar-email-recuperacao.

## Conferência final

`openspec validate <change> --type change` aprovado para impedir-recuperacao-email-sem-conta, recuperar-senha-codigo-6-digitos e simplificar-pagina-recuperacao. `git diff --check` aprovado e `git check-ignore` confirmou backup privado ignorado. Quatro tarefas concluídas com evidências acima. Sem sincronização ou arquivamento nesta rodada.
