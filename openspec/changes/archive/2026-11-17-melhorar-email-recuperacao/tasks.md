## 1. Mensagem e experiência

**Fechamento de 17/11: 5/5.** Após o teste real, o usuário confirmou que está mais rápido e aceitou comparar pela experiência de uso. Critério 2.3 ajustado explicitamente para aceite qualitativo, sem exigir benchmark quantitativo. [Aceite e limites](aceite-final-2026-11-17.md). Os registros abaixo preservam as etapas anteriores.

Retomada de 17/11: [medição real autorizada](roteiro-medicao-2026-11-17.md), um pedido HTTP 200 em 4,521 s, chegada confirmada pelo operador em 24,962 s após o início. Zero retries/trocas de senha. Tempos históricos do provedor não constituem baseline antes/depois equivalente. Chegada real demonstrada; 2.3 continua aberta exclusivamente pela comparação não comprovada, 4/5.

17/11/2026 — Decisão atual: não haverá domínio próprio. 2.3 continua aberta somente pela medição comparativa real com caixa controlada e remetente individual verificado, sem exigir DNS. Os diagnósticos históricos de SPF/DKIM abaixo não são pré-requisitos de compra/configuração. Não há comparação nova nem redução de atraso comprovada nesta rodada.

11/11/2026, ensaio real: usuário sem código; mensagem correspondente em
processing com cinco adiamentos SMTP 421/4.7.32 e zero delivered.
[Diagnóstico de entrega atual](diagnostico-entrega-2026-11-11.md).
Sem reenvio ou alteração DNS; 2.3 continua aberta por dependência de domínio e
comparação real. Não confundir aceitação do provedor com chegada.

11/11/2026: [revisão conjunta de aceite](../2026-11-17-integrar-sendgrid-recuperacao/aceite-2026-11-11.md).
Zero domínios autenticados na conta SendGrid confirmado por leitura. Sem nova
medição de chegada ou comparação antes/depois; 2.3 continua aberta, 4/5.

- [x] 1.1 Preparar HTML/texto com identidade visual e payload sem rastreamento, validar sandbox SendGrid e preview desktop/mobile sem entrega real.
- [x] 1.2 Implementar feedback imediato e cooldown de reenvio, testar ordem de eventos, ausência de requisições redundantes e compilar Reflex.

## 2. Publicação e evidências

- [x] 2.1 Publicar somente endpoint após backup/prévia e validar delta remoto restrito sem alterar ambiente.
- [x] 2.2 Registrar medições disponíveis e seus limites, testes/preview, executar validação OpenSpec e diff.
- [x] 2.3 Medir chegada real em caixa controlada e registrar comparação qualitativa antes/depois aceita pelo usuário em 17/11, usando o remetente individual verificado atual. Pedido HTTP 200, confirmação de chegada em 24,962 s e usuário relata estar mais rápido. Aceite final em `aceite-final-2026-11-17.md`; não equivale a benchmark, redução percentual ou SLA. Domínio próprio/DNS fora do escopo. O critério anterior de comparação quantitativa foi substituído pelo aceite explícito do usuário, sem alterar a evidência bruta.

Evidências históricas: [validation.md](validation.md). Adiamentos Gmail 421 4.7.32 por alinhamento SPF/DKIM permanecem limitação conhecida. Por decisão de 17/11, não haverá domínio próprio/DNS; a comparação de entrega deve usar o remetente individual verificado atual. Nenhuma redução de tempo foi comprovada apenas pela alteração de template.
