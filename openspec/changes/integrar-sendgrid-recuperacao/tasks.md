## 1. Configuração e contrato

Revisão de 11/11/2026: [aceite, testes e bloqueios](aceite-2026-11-11.md).
Remetente verificado e zero domínios autenticados reconfirmados por GET.
2.2 permanece aberta; nenhuma nova entrega ou troca executada.

- [x] 1.1 Salvar SENDGRID_API_KEY no .env privado, documentar variáveis vazias em .env.example e verificar presença sem imprimir valores e git check-ignore.
- [x] 1.2 Adaptar endpoint para SendGrid e verificar payload, HTTP 202, falhas sanitizadas e recuperação com testes locais e dry-run Xano quando acessível.

## 2. Ativação e evidências

Continuação de 11/11/2026: usuário confirmou recebimento, troca e novo login com
senha nova no app. [Aceite manual e critérios restantes](../recuperar-senha-codigo-6-digitos/validation/aceite-usuario-2026-11-11.md).
Substitui a ausência de recebimento dos registros anteriores desta data; não
comprova melhoria de latência ou os demais critérios de 3.2. 2.2 segue aberta.

11/11/2026: ensaio real interrompido antes da troca; código não recebido.
[Mensagem adiada por alinhamento SPF/DKIM, sem delivered](../melhorar-email-recuperacao/diagnostico-entrega-2026-11-11.md).
Manter 2.2 aberta, sem reenvio automático ou alteração de configurações.

- [x] 2.1 Confirmar remetente verificado, configurar ambiente Xano após backup/prévia restrita e verificar publicação e aceitação real sem alterar configurações alheias.
- [ ] 2.2 Comprovar recebimento e ciclo completo em caixa controlada; manter vínculo com 3.2 da change original sem concluir por simulação.
- [x] 2.3 Registrar validações/limitações e executar openspec validate integrar-sendgrid-recuperacao --type change e git diff --check.

Evidências e limites: [validation.md](validation.md). Remetente confirmado e integração publicada no Xano com backup e conferência de preservação do ambiente. Envio/recebimento reportados pelo usuário e consumo/troca HTTP 200 observados no histórico; 2.2 aguarda login e demais critérios do ciclo completo.
