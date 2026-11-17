## Why

O usuário pediu menor espera no envio e melhor design do e-mail de recuperação. O endpoint responde em menos de um segundo nas seis amostras recentes, mas ainda não há medição de chegada à caixa.

## What Changes

- E-mail com identidade Codeboxd, código em destaque, instruções curtas e versão texto simples.
- Desativar rastreamento no e-mail transacional, sem recursos externos nem agendamento.
- Feedback imediato e bloqueio de reenvio por 60 segundos no cliente, alinhado ao backend.
- Validar payload sem envio, publicar somente o endpoint após backup e medir limites sem prometer latência de entrega não comprovada.

## Capabilities

### New Capabilities

- `recovery-mail-experience`: E-mail acessível e experiência de solicitação com feedback imediato e reenvio controlado.

### Modified Capabilities

Nenhuma; prazo, uso único e validação existentes preservados.

## Impact

Endpoint de solicitação Xano, template HTML/texto, SessionState/página, testes e evidências. Sem alteração de domínio, DNS, senha de conta ou serviço de e-mail.
