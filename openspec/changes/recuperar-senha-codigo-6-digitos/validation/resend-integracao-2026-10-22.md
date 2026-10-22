# Integração Resend — 22/10/2026

## Implementação e publicação reais

GET reset/request-reset-link agora envia via POST https://api.resend.com/emails,
com RESEND_API_KEY e RESEND_FROM do ambiente privado Xano. Valida HTTP 2xx e
ID da mensagem; captura falhas de rede e sanitiza o erro apresentado ao cliente.
Não repete automaticamente o envio e preserva resposta genérica quando não
há conta ativa elegível ou a geração está em cooldown.

Ferramenta `tools/deploy_recovery_resend.py` preparou e aplicou preview com um
endpoint e duas variáveis de ambiente. O dry-run reconheceu has_env=true,
sem erros de parser ou tabelas/records no delta. Aplicação foi seguida de
exportação/comparação em memória: somente o endpoint esperado mudou nas
definições; presença dos valores privados foi conferida sem imprimi-los.
[Resultado sanitizado](resend-deployment-2026-10-22.json).

Backup das definições sem segredos preservado em
`.local/resend-deployment-2026-10-22/before-without-secrets.xs`.
Rollback deve restaurar somente o bloco do endpoint de recuperação desse
backup. Se remover as variáveis Resend, preservar todas as outras variáveis
atuais do workspace; nunca importar um mapa vazio ou uma configuração antiga
por cima de segredos novos. O serviço nativo anterior permanece com falha.

A primeira prévia exploratória com valores fictícios em linha única teve
erro de comparação do parser e has_env=false. Não foi aplicada. A prévia
multilinha aprovada reconheceu corretamente o ambiente. Não interpretar todo
HTTP 200 do dry-run como compilação/execução aprovada sem conferir seu corpo.

## Validação por camada

- Interpretador Xano, resposta fictícia 400: rejeição sanitizada aprovada.
  [Resultado](resend-error-guard-2026-10-22.json).
- Interpretador Xano, resposta fictícia 200 com ID: aceita.
  [Resultado](resend-success-guard-2026-10-22.json).
- Interpretador Xano, resposta fictícia 200 com erro/ID nulo: rejeitada.
  [Resultado](resend-200-sem-id-2026-10-22.json).
- API real, conta inexistente sintética: 200 genérico, sem segredos.
  [Resultado](resend-conta-inexistente-2026-10-22.json).
- Login real: primeira tentativa 403 preservada em
  [registro próprio](email-real-resend-login-rejeitado-2026-10-22.json).
  Tentativa seguinte autenticou; solicitação de e-mail retornou 400 sanitizado,
  comprovando ausência de sucesso silencioso após a publicação.
  [Resultado](email-real-resend-2026-10-22.json).
- Resend real, mensagem estática sem código: HTTP 403 validation_error,
  restrição de destinatário do domínio de teste; não foi enviada.
  [Retorno sanitizado](resend-provedor-real-2026-10-22.json).

## Pendência concreta

O e-mail da conta Codeboxd controlada difere do proprietário da conta Resend.
Não existe conta Codeboxd com o endereço permitido, conforme leitura do banco.
[Comparação booleana](resend-restricao-destinatario-2026-10-22.json).

Usuário recebeu opções para alinhar endereços: cadastro normal de conta de
teste com e-mail Resend; alteração do e-mail proprietário no Resend; ou
domínio próprio verificado. Nenhuma conta foi criada automaticamente.
Solicitações de validação sem destinatário elegível não comprovam entrega.

Checklist 8/10: 3.3 concluída; 3.4 aguarda envio aceito e 3.2 aguarda e-mail
recebido, troca, login, rejeição de senha anterior/código usado e restauração.
Nenhuma senha foi alterada nesta rodada. Não houve nova compilação Reflex ou
novo teste de navegador do app; a janela local é um executor de API separado.
