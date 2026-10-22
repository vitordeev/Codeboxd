## 1. Contratos de recuperação

- [x] 1.1 Implementar esquema aditivo, geração de seis dígitos, prazo de 15 minutos, cooldown e e-mail; verificar contratos no dry-run e confirmar geração/hash/cooldown em execução controlada.
- [x] 1.2 Implementar validação de formato, conta ativa, prazo, cinco tentativas persistidas, uso único e token temporário de cinco minutos; verificar rejeições, concorrência e consumo no Xano real.

## 2. Interface e testes locais

- [x] 2.1 Ajustar campo e mensagens para seis dígitos e bloquear entradas inválidas sem requisição; verificar testes de formato, troca, falhas e não persistência do token.
- [x] 2.2 Verificar formulário em desktop/celular e código inválido no navegador, preservando a senha; registrar screenshots privados e resumo sem segredos.
- [x] 2.3 Executar suíte, compilação e validação estrita OpenSpec, atualizar P.6/contexto/evidências e registrar os limites das verificações.

Complemento da retomada em 20/10, necessário para executar o fluxo real:

- [x] 2.4 Separar IDs dos e-mails nas duas etapas do formulário e conferir envio do campo correto no navegador, sem alterar os nomes da API. [Diagnóstico e validação](validation/retomada-2026-10-20.md).

## 3. Publicação e entrega real

- [x] 3.1 Exportar estrutura, revisar delta limitado e publicar contratos de reset; verificar dry-run posterior sem mudanças, sem importar registros/segredos.
- [ ] 3.2 Comprovar chegada do e-mail com seis dígitos, troca de senha, novo login e rejeição de reutilização em conta com caixa controlada; registrar resultado e restauração segura da conta de teste.
- [x] 3.3 Capturar resultado do serviço de e-mail e impedir sucesso silencioso quando o provedor retorna erro dentro de HTTP 200; verificar rejeição sanitizada e preservação dos caminhos genéricos, registrando separadamente validação local e publicação.
- [ ] 3.4 Integrar Resend no endpoint Xano com chave/remetente no ambiente privado; verificar contrato, falhas sanitizadas e envio aceito, publicar somente o endpoint após backup e conferir delta. Manter entrega/ciclo real em 3.2.

Evidências e limites: [implementacao-2026-10-14.md](validation/implementacao-2026-10-14.md).

Retomada em 22/10/2026: preparado `tools/password_recovery_remote.py` para
solicitação de e-mail real com login privado, código informado da caixa pelo
usuário, troca por senha temporária, login, rejeição da senha antiga e código
usado, restauração da senha original e confirmação de login. Senhas, código e
tokens ficam em memória; relatório registra apenas cenários/status/resultados.
Dois cenários com transporte HTTP simulado passaram: fluxo completo e
restauração após timeout. OpenSpec e `git diff --check` aprovados. Janela local
iniciada; aguarda interação do usuário. Simulação e resposta genérica de envio
não comprovam entrega. 3.2 permanece aberta até evidência real completa.

Diagnóstico posterior em 22/10: login e solicitação reais retornaram 200, mas
usuário não recebeu e-mail. Leitura do Xano confirmou conta ativa e geração
de código/hash com prazo de 15 minutos. Chamada ao serviço nativo de e-mail
existe no endpoint publicado; aceitação/entrega pelo provedor não comprovadas.
Não houve troca de senha nem republicação. 3.2 continua aberta.
[Resultado e próximos critérios](validation/diagnostico-entrega-2026-10-22.md).

Continuação para concluir hoje: executar diagnóstico isolado do util.send_email
com mensagem estática sem código, destinada somente à conta já informada no
teste, sem publicar endpoint ou alterar senha; capturar apenas retorno/erro
sanitizado do serviço. Usar o resultado para definir eventual correção antes
de uma nova solicitação real. Entrega e ciclo completo continuam obrigatórios.

Resultado: diagnóstico isolado retornou `status=error`,
`error=Workspace admin not found`, `remaining=100` dentro de HTTP 200.
[Evidência sanitizada](validation/provedor-email-2026-10-22.json).
Captura de `$delivery` e rejeição sanitizada implementadas localmente;
`xano workspace push -d xano -w 147717 --dry-run -i api/authentication/reset/request_reset_link_GET.xs`
aprovado com exatamente um endpoint atualizado. OpenSpec e diff aprovados.
Sem publicação nesta rodada. 3.3 permanece aberta para validação de execução
e publicação; 3.2 depende da correção/configuração do provedor e entrega real.
Solicitado ao usuário serviço existente ou caminho privado da configuração,
sem solicitar chave pelo chat. Não atribuir o erro a papel admin do aplicativo.

Preparação Resend após usuário informar configuração: endpoint local agora
usa POST /emails do Resend, lê RESEND_API_KEY/RESEND_FROM no ambiente privado
Xano, exige HTTP 2xx e ID da mensagem, sanitiza exceções e não faz retry.
Dry-run limitado aprovado: exatamente um endpoint atualizado. OpenSpec e
diff aprovados. Não houve publicação, configuração remota de segredos ou envio
Resend: verificações booleanas confirmaram ausência das duas variáveis no
`.env` salvo, também sem chave no `.env.example` ou ambiente do processo.
Solicitado caminho correto ou salvamento do editor, sem revelar segredos.
Checklist atual 7/10; 3.2/3.3/3.4 abertas até validação de execução/publicação.

Publicação Resend em 22/10: nova chave/remetente salvos privadamente e
configurados no ambiente Xano. Preview reconheceu duas variáveis privadas e
um endpoint atualizado, sem tabelas/records. Backup sem segredos em
`.local/resend-deployment-2026-10-22/before-without-secrets.xs`; comparação
posterior confirmou somente endpoint esperado modificado e variáveis presentes.
Três cenários no interpretador Xano com respostas fictícias (400, 200 com ID,
200 sem ID) confirmaram decisão correta. Conta inexistente real manteve 200
genérico; conta controlada real com falha do provedor retornou erro sanitizado
400. 3.3 concluída. Tentativa inicial com login 403 preservada separadamente;
login corrigido passou, sem troca de senha nesta rodada.

Resend real rejeitou mensagem estática com 403 validation_error: remetente
onboarding@resend.dev permite somente destinatário proprietário da conta
Resend, diferente do e-mail Codeboxd testado. Consulta somente de leitura
confirmou que não existe conta Codeboxd correspondente ao e-mail permitido.
Nenhuma conta criada, privilégio alterado ou chave copiada para evidências.
3.4 segue aberta por faltar envio aceito e 3.2 por faltar recebimento/ciclo
completo. Atual: 8/10. [Entrega e evidências](validation/resend-integracao-2026-10-22.md).
