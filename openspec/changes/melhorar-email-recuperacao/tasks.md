## 1. Mensagem e experiência

11/11/2026, ensaio real: usuário sem código; mensagem correspondente em
processing com cinco adiamentos SMTP 421/4.7.32 e zero delivered.
[Diagnóstico de entrega atual](diagnostico-entrega-2026-11-11.md).
Sem reenvio ou alteração DNS; 2.3 continua aberta por dependência de domínio e
comparação real. Não confundir aceitação do provedor com chegada.

11/11/2026: [revisão conjunta de aceite](../integrar-sendgrid-recuperacao/aceite-2026-11-11.md).
Zero domínios autenticados na conta SendGrid confirmado por leitura. Sem nova
medição de chegada ou comparação antes/depois; 2.3 continua aberta, 4/5.

- [x] 1.1 Preparar HTML/texto com identidade visual e payload sem rastreamento, validar sandbox SendGrid e preview desktop/mobile sem entrega real.
- [x] 1.2 Implementar feedback imediato e cooldown de reenvio, testar ordem de eventos, ausência de requisições redundantes e compilar Reflex.

## 2. Publicação e evidências

- [x] 2.1 Publicar somente endpoint após backup/prévia e validar delta remoto restrito sem alterar ambiente.
- [x] 2.2 Registrar medições disponíveis e seus limites, testes/preview, executar validação OpenSpec e diff.
- [ ] 2.3 Medir tempo de chegada de mensagem real e comparar antes/depois em caixa controlada; não concluir por sandbox ou tempo de API.

Evidências: [validation.md](validation.md). Causa identificada: adiamentos Gmail 421 4.7.32 por alinhamento SPF/DKIM com From. Aguardar domínio próprio e DNS antes de planejar configuração que elimine essa causa. Nenhuma redução de entrega comprovada apenas pela alteração de template.
