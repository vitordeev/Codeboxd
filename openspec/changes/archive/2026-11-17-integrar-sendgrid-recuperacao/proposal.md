## Why

17/11/2026 — [Aceite concluído](fechamento-2026-11-17.md), 5/5, usando evidência real de 12/11 e conferência atual de leitura. O usuário definiu domínio próprio fora do escopo; mantém-se remetente individual verificado. O diagnóstico original abaixo precede a implantação. Restauração de conta e comparação de latência continuam nas changes responsáveis.

O usuário forneceu uma chave SendGrid e autorizou seu uso na recuperação por código. O endpoint atual usa Resend e não comprovou entrega.

## What Changes

- Configurar SENDGRID_API_KEY no .env privado e documentar SENDGRID_FROM.
- Adaptar somente o emissor Xano para SendGrid, mantendo geração, hash, prazo, cooldown e validação existentes.
- Validar contrato local e configuração; distinguir publicação, aceitação e recebimento reais.

## Capabilities

### New Capabilities

- `recovery-email-delivery`: Envio do código pelo SendGrid com configuração privada e erros sanitizados.

### Modified Capabilities

Nenhuma. A change recuperar-senha-codigo-6-digitos preserva seus critérios de ciclo completo e histórico Resend.

## Impact

.env privado, .env.example, endpoint Xano de solicitação e testes/evidências. Sem alteração de UI, senha de contas, Docker ou infraestrutura de hospedagem.
