# Retomada da recuperação de senha — 28/10/2026

## Validação local

Executado com `.venv/Scripts/python.exe -B -m unittest tests.test_password_recovery tests.test_session_navigation_performance tests.test_api_rate_limit -q`: **24 testes passaram** em 0,653 s. Os transportes de e-mail/API são mocks; nenhum endereço, senha, código ou token real foi usado. `openspec validate recuperar-senha-codigo-6-digitos --type change`: válida. `git status --short` estava limpo antes desta atualização.

## Estado do provedor

O histórico sanitizado de 22/10 mostra o remetente `onboarding@resend.dev`
rejeitando o destinatário Codeboxd com HTTP 403. A documentação oficial do
Resend confirma que o domínio compartilhado de testes só envia para o e-mail
proprietário da conta Resend; para outros destinatários, o remetente precisa
usar domínio verificado. A página oficial de testes lista `delivered@resend.dev`
como endereço de simulação de entrega. Por simularem eventos, esses endereços
não comprovam que o titular recebeu e consegue ler um código de recuperação real.

Referências atuais:

- [Resend — Send Test Emails](https://resend.com/docs/dashboard/emails/send-test-emails)
- [Resend — API Errors](https://resend.com/docs/api-reference/errors)

## Pendência e próximo passo

As tarefas 3.2 e 3.4 continuam abertas. Para fechar 3.4 e 3.2, precisa existir
uma destas condições, sem compartilhar segredos no chat:

1. uma conta Codeboxd controlada cujo e-mail seja também o proprietário da conta
   Resend, e acesso a essa caixa; ou
2. domínio do usuário verificado no Resend, `RESEND_FROM` desse domínio já
   configurado no workspace Xano e uma caixa controlada nesse domínio.

Depois, o executor interativo existente solicita login da conta Codeboxd,
envia uma única mensagem, aguarda o código informado pelo titular e testa
troca, login novo, rejeição da senha/código anterior e restauração da senha
original. Não iniciar a janela nem enviar uma solicitação sem destinatário
elegível: isso apenas falharia novamente e poderia consumir o cooldown.

Nenhum envio, leitura de mailbox, uso de credencial em chamada, troca de senha,
escrita Xano, publicação ou alteração de conta ocorreu em 28/10. O registro
anterior de 403 permanece intacto; não foi sobrescrito.
