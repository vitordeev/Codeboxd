## Context

Ver proposal.md. O envio ocorre no Xano; .env local não configura variáveis remotas. A integração SendGrid foi publicada em 10/11, substituindo Resend, e mantém os controles de segurança da change de recuperação. [Fechamento de 17/11](fechamento-2026-11-17.md): jornada até recebimento/troca/novo login comprovada em 12/11; restauração permanece em 3.2 da change de recuperação. Domínio próprio não será usado por decisão do usuário; remetente individual verificado mantido.

## Goals / Non-Goals

Configurar a chave autorizada e preparar envio SendGrid. Não alterar geração ou consumo do código, nem senhas reais para testar.

## Decisions

- Usar POST https://api.sendgrid.com/v3/mail/send, Bearer SENDGRID_API_KEY, personalizations.to, from.email e content text/html. Exigir HTTP 202; o corpo de sucesso pode ser vazio, portanto não exigir ID JSON como no Resend.
- SENDGRID_FROM deve conter somente o endereço de remetente verificado. Não inferir remetente a partir da chave ou reutilizar onboarding@resend.dev.
- Preservar timeout, ausência de retry e erros públicos sanitizados. Não registrar corpo do provedor ou código.
- Guardar chave apenas no .env ignorado e manter exemplos sem valores. Documentar separadamente configuração local e publicação.
- Preparar contrato local mesmo sem remetente, mas manter publicação/entrega pendentes até configuração completa. Backup e dry-run restrito são obrigatórios antes de publicar; rollback restaura apenas o endpoint e variáveis criadas, preservando configurações existentes.

## Risks / Trade-offs

Chave sem permissão de leitura pode impedir descoberta do remetente; isso não prova impossibilidade de envio. HTTP 202 comprova aceitação, não chegada na caixa. Chave enviada no chat deve ser rotacionada posteriormente sem copiar valor para evidências.

## Migration Plan

Salvar ambiente local, preparar contrato, verificar configuração sem imprimir segredos, executar testes locais. Com remetente confirmado, revisar backup/dry-run antes da publicação e validar envio/ciclo com caixa controlada. Histórico Resend permanece preservado.

## Open Questions

Resolvida em 10/11/2026: endereço fornecido salvo no ambiente privado e verificação confirmada pela API. Entrega/troca/novo login comprovados no ensaio real de 12/11, reconciliados em `fechamento-2026-11-17.md`; restauração e latência comparativa continuam nas changes responsáveis. Sem domínio próprio, conforme decisão do usuário.
