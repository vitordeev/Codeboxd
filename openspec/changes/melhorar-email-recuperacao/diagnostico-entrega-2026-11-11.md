# Entrega adiada — 11/11/2026

## Evidência desta execução

Usuário informou que o código não chegou. Leitura de histórico Xano e atividade
SendGrid executada às 14:29 UTC, sem novo envio ou mudança de conta/configuração.
Destino do pedido mais recente comparado ao destinatário das mensagens somente
em memória. Nenhum e-mail, ID de mensagem, código, token ou corpo registrado.

[Relatório sanitizado](delivery-diagnostic-2026-11-11.json):

- Histórico Xano GET 200; pedido de recuperação mais recente retornou 200.
- SendGrid GET `/v3/messages` e detalhe da mensagem: 200.
- Uma mensagem correspondente à caixa do pedido recente encontrada: processing,
  um evento processed e cinco deferred, nenhum evento delivered.
- Último evento disponível: 11/11/2026 14:27:20 UTC.
- Motivo contém marcadores SPF/DKIM/DMARC/alignment e códigos SMTP 421/4.7.32.

Não é entrega nem falha definitiva: servidor destinatário está adiando a
mensagem. Não há confirmação de chegada pelo operador. Não medir melhoria de
latência ou concluir recuperação/SendGrid por resposta 200/aceitação do provedor.

## Interpretação e dependência externa

A [documentação Google](https://support.google.com/mail/answer/14229414) define
4.7.32 como limitação por From sem alinhamento ao domínio autenticado SPF ou DKIM.
Isso corresponde aos motivos observados nesta mensagem, não apenas ao histórico
de 10/11. A consulta anterior desta rodada confirmou zero domínios autenticados
na conta SendGrid e remetente de provedor de e-mail de consumidor.

A [autenticação de domínio SendGrid](https://www.twilio.com/docs/sendgrid/ui/account-and-settings/how-to-set-up-domain-authentication)
exige registros no DNS de domínio controlado. Não inventar registros SPF/DKIM,
alterar domínio de terceiros ou apresentar novo template/reenvio como correção.
Usuário consultado sobre domínio próprio/provedor DNS. Antes de qualquer escrita,
preparar registros exatos e proposta de remetente e obter autorização específica.

## Estado do ensaio

Relatório de retomada da recuperação: awaiting_first_code, login confirmado,
um pedido de e-mail no total e restoration_needed=false. Nenhum código consumido
ou tentativa de escrita de senha até a consulta; ensaio não concluído.
Não reenviar automaticamente, não renovar validade nem gerar código por canal
administrativo para contornar comprovação da caixa. Se o código chegar após
expirar, não usar como aceite; organizar novo ensaio autorizado após a correção.

Manter melhorar-email 2.3, SendGrid 2.2 e recuperação 3.2 abertas. Nenhuma
alteração de código nesta investigação; somente evidência/acompanhamento.

## Novo destinatário e acompanhamento posterior

Usuário autorizou outro teste. Relatório do executor `outro-email` confirma
login e pedido HTTP 200, awaiting_first_code e restoration_needed=false;
operador informou novamente que não funcionou. Nenhuma escrita de senha.

Consulta posterior de eventos mostrou delivered após cinco adiamentos para a
mensagem anterior, último evento 14:29:42 UTC. A conferência dos timestamps do
histórico Xano mostrou que o pedido mais recente disponível ali era 14:23:11,
anterior ao segundo ensaio iniciado 14:32. Portanto **não atribuir essa entrega
ao segundo destinatário**, nem afirmar que chegou na caixa do usuário. O
[relatório da consulta](delivery-diagnostic-outro-email-2026-11-11.json) registra
explicitamente essa limitação; status final da segunda mensagem não confirmado.

O problema de alinhamento já comprovado na mensagem anterior permanece
relevante. Correção proposta: domínio controlado pelo usuário, autenticação
SendGrid com os registros DNS gerados para esse domínio e remetente coerente,
após revisão e autorização específica. Depois medir envio/entrega/caixa e ciclo
completo. Não alterar ou enfraquecer expiração de código para mascarar atrasos.

Usuário informou nesta continuação que não possui domínio próprio. Autenticação
DNS do remetente atual não pode ser concluída nesta rodada. Nenhum domínio,
plano ou serviço adquirido/configurado. Preservar integração existente e
pendências de entrega. Testes locais e sandbox permanecem possíveis, mas o
[sandbox SendGrid](https://www.twilio.com/docs/sendgrid/for-developers/sending-email/sandbox-mode)
valida formato sem entregar mensagem e não satisfaz aceite da caixa.

## Cadastro no app e nova recuperação — 11h42/11h43 locais

Usuário informou criar conta, sair e solicitar recuperação, depois relatou não
encontrar o usuário no banco. Consulta somente de leitura confirmou cadastro
HTTP 200 às 14:42:06 UTC na branch v1/workspace 147717. Comparação do e-mail
apenas em memória encontrou exatamente um user ativo, um profile e duas listas
na fonte live. A solicitação às 14:43:04 UTC corresponde à mesma conta, HTTP 200.
[Evidência sem identidade](../recuperar-senha-codigo-6-digitos/validation/cadastro-persistencia-2026-11-11.json).

Na consulta de atividade da rodada do app, a mensagem correspondente estava
processing, com um processed e três deferred; marcadores de alinhamento
SPF/DKIM/DMARC e SMTP 421/4.7.32. Último evento 14:44:33 UTC.
[Resumo](delivery-diagnostic-app-2026-11-11.json). Sem delivered nessa consulta.
Não há evidência de falha de persistência do cadastro neste caso; orientar
conferência de workspace, branch, fonte e filtros da tabela. Nenhuma conta,
senha ou configuração alterada na investigação.
