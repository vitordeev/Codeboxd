## 1. Mensagem e experiência

- [x] 1.1 Preparar HTML/texto com identidade visual e payload sem rastreamento, validar sandbox SendGrid e preview desktop/mobile sem entrega real.
- [x] 1.2 Implementar feedback imediato e cooldown de reenvio, testar ordem de eventos, ausência de requisições redundantes e compilar Reflex.

## 2. Publicação e evidências

- [x] 2.1 Publicar somente endpoint após backup/prévia e validar delta remoto restrito sem alterar ambiente.
- [x] 2.2 Registrar medições disponíveis e seus limites, testes/preview, executar validação OpenSpec e diff.
- [ ] 2.3 Medir tempo de chegada de mensagem real e comparar antes/depois em caixa controlada; não concluir por sandbox ou tempo de API.

Evidências: [validation.md](validation.md). Causa identificada: adiamentos Gmail 421 4.7.32 por alinhamento SPF/DKIM com From. Aguardar domínio próprio e DNS antes de planejar configuração que elimine essa causa. Nenhuma redução de entrega comprovada apenas pela alteração de template.
