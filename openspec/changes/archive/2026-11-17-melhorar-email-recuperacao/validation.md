# E-mail de recuperação — 10/11/2026

## Resultado e limites atuais

Novo template publicado no endpoint de recuperação do Xano, com marca Codeboxd, cartão escuro, código contínuo destacado, prazo/uso único e instrução de segurança. HTML de 2630 bytes, sem imagens, links ou fontes externos; alternativa text/plain e rastreamento desativado nessa mensagem. Mesma regra de aceitação SendGrid 202, timeout, ausência de retry, hash e controles de recuperação.

Interface atualiza estado “Enviando…” antes de esperar pela rede, impede cliques redundantes e bloqueia novo pedido ao mesmo endereço por 60 segundos após resposta aceita. O bloqueio local complementa o cooldown existente no servidor. Não altera velocidade SMTP e não prova entrega mais rápida.

## Medições e causa do atraso

Histórico Xano: seis solicitações com durações [0.359, 0.421, 0.565, 0.035, 0.062, 0.323] segundos, mediana 0.341s. Inclui respostas de cooldown/sem envio; não usar como SLA de entrega. Fonte: consulta administrativa de leitura do histórico sem exibir entradas ou destinatários.

Atividade SendGrid consultada somente de leitura, sem novo envio: duas mensagens entregues após 27s e 70s; uma ainda em processing com sete adiamentos. Todas tiveram adiamentos SMTP 421 / 4.7.32, com indicadores de SPF/DKIM/DMARC. Relatório sanitizado em [activity.json](activity.json), sem endereços, IDs de mensagem, motivos completos ou conteúdo.

[Google — erro 4.7.32](https://support.google.com/mail/answer/14229414) documenta rate limiting por From sem alinhamento ao domínio autenticado SPF/DKIM. Remetente atual gmail.com verificado pelo SendGrid não confere controle de DNS desse domínio. A correção da causa exige domínio próprio autenticado e endereço correspondente; usuário consultado sobre disponibilidade/acesso DNS. Ver [configuração oficial SendGrid](https://www.twilio.com/docs/sendgrid/ui/account-and-settings/how-to-set-up-domain-authentication).

**Não há comprovação de redução do tempo até a caixa após a alteração.** Não concluir tarefa 2.3 nem apresentar o novo design/rastreamento desativado como solução para o erro 4.7.32. Nenhuma configuração DNS, domínio ou remetente alterada nesta rodada.

## Validação local e sandbox

- `.venv/Scripts/python.exe -B -m tools.build_recovery_email`: HTML gerado a partir de `xano/templates/recovery_email.html`, slot de código único, preview com dígitos fictícios em `.local/recovery-email-preview.html`.
- `.venv/Scripts/python.exe -B -m tools.recovery_email_release`: sandbox SendGrid HTTP 200 sem entrega, validando estrutura HTML/texto e tracking_settings. Prévia Xano HTTP 200 limitada a uma query, env/records false. [Relatório](preview.json).
- Playwright/Edge headless: preview HTML em 320/390/700px, código visível, sem overflow horizontal; nenhuma rede externa permitida. [Geometria](browser.json). Capturas privadas `.local/recovery-email-{largura}.png`; captura 390px inspecionada. É prévia em navegador, não teste em cliente Gmail/Outlook.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_password_recovery.py -q`: 14 testes aprovados, incluindo yield antes da rede, bloqueio de submissão duplicada e reenvio sem HTTP no intervalo.
- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado após ajustes finais.

## Publicação e rollback

`.venv/Scripts/python.exe -B -m tools.recovery_email_release --apply`: prévia revalidada, assinatura do estado anterior/endpoint conferida, backup privado sem segredos salvo em `.local/recovery-email-release/before-without-secrets.xs`, publicação HTTP 200. Exportação posterior confirmou somente GUID do endpoint de solicitação alterado. [Relatório](deployment.json). Sem alteração de ambiente, tabelas ou registros.

Rollback: extrair somente a query de recuperação do backup sem segredos e submeter após dry-run com partial=true, env=false, records=false e delete=false. Não aplicar exportação integral.

## Conferência documental

`openspec validate melhorar-email-recuperacao --type change` e `git diff --check` aprovados. Backup privado confirmado ignorado pelo Git; nenhum segredo em templates/relatórios. Sem novos e-mails ou alterações de senha/conta realizados nos testes. Medição comparativa de entrega aguarda configuração de domínio/ensaio controlado. Quatro de cinco tarefas concluídas; 2.3 permanece aberta.
