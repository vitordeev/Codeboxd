## Implementation

- [x] 1.1 Corrigir hierarquia da foto/miniatura e controles de curtida no cartão, com fallback e acessibilidade.
- [x] 1.2 Substituir comentários ao fim do feed por painel contextual responsivo com composer e autoria preservada.
- [x] 1.3 Proteger leituras e mutações por contexto, loading, replay e falha sem perder rascunho ou repetir escritas.

## Validation

- [x] 2.1 Testar concorrência, respostas antigas, falha e recuperação, likes legados e regressões sociais.
- [x] 2.2 Executar compilação e navegador em 1440/390px com fotos/obras, estados de comentários e interações; separar fixtures de remoto.
- [x] 2.3 Registrar evidências, limitações e validar a change no OpenSpec.

Evidências: [validation.md](validation.md). 432 testes na suíte final, build de
produção e oito cenários de navegador com backend fictício aprovados. Sem
validação de conta real, publicação Xano ou reinício da instância normal.
