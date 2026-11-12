05/11/2026: ambiente publicado conferido diretamente: chave presente, consulta
de dominios Resend com essa chave retornou 401 restricted_api_key (permissao
restrita, nao prova chave invalida); remetente de testes permanece.
[Evidencia e limites](validation/configuracao-publicada-2026-11-05.md).
Sem envio/troca reais; 3.2/3.4 continuam abertas, 8/10.

04/11/2026: executor preparado com destino de evidencia explicito, sem sobrescrever
historico. [Retomada e dependencia de caixa controlada](validation/retomada-2026-11-04.md).
7 testes locais passaram; nenhum envio ou troca real nesta rodada. 8/10 mantido.

> Estado reconciliado em 26/10/2026: 8/10 tarefas concluídas. Resend integrado e publicado em 22/10 após falha do serviço nativo. Provedor/remetente já escolhidos; resta destinatário elegível ou domínio verificado, envio aceito e chegada/ciclo completo. 3.2 e 3.4 continuam abertas; não arquivar. As seções e rodadas anteriores abaixo preservam o planejamento e sua evolução; o checklist e a evidência datada prevalecem sobre resumos antigos.

## 1. Contratos de recuperação

11/11/2026: [revisão de aceite e bloqueios](../integrar-sendgrid-recuperacao/aceite-2026-11-11.md).
25 testes pertinentes locais aprovados; estrutura publicada inspecionada sem
registros/ambiente. 3.2 permanece aberta por falta da evidência de replay e
restauração no ciclo controlado. A integração SendGrid que substituiu Resend
foi reconciliada e atende a 3.4; ver registro junto ao item.

- [x] 1.1 Implementar esquema aditivo, geração de seis dígitos, prazo de 15 minutos, cooldown e e-mail; verificar contratos no dry-run e confirmar geração/hash/cooldown em execução controlada.
- [x] 1.2 Implementar validação de formato, conta ativa, prazo, cinco tentativas persistidas, uso único e token temporário de cinco minutos; verificar rejeições, concorrência e consumo no Xano real.

## 2. Interface e testes locais

- [x] 2.5 Preservar confirmação após troca concluída e bloquear submits posteriores do código consumido; testar repetição sem chamadas HTTP, novo pedido no estado e compilar Reflex. Registrar validação local e limite da instância em execução. [Evidência](validation/repeticao-apos-sucesso-2026-11-10.md). A ação visual secundária e a reinicialização ao reabrir a rota foram cobertas na task 2.6.

- [x] 2.1 Ajustar campo e mensagens para seis dígitos e bloquear entradas inválidas sem requisição; verificar testes de formato, troca, falhas e não persistência do token.
- [x] 2.2 Verificar formulário em desktop/celular e código inválido no navegador, preservando a senha; registrar screenshots privados e resumo sem segredos.
- [x] 2.3 Executar suíte, compilação e validação estrita OpenSpec, atualizar P.6/contexto/evidências e registrar os limites das verificações.

Complemento da retomada em 20/10, necessário para executar o fluxo real:

- [x] 2.4 Separar IDs dos e-mails nas duas etapas do formulário e conferir envio do campo correto no navegador, sem alterar os nomes da API. [Diagnóstico e validação](validation/retomada-2026-10-20.md).
- [x] 2.6 Permitir iniciar outra jornada de recuperação após sucesso: ao reabrir `/redefinir-senha` ou acionar uma opção textual secundária discreta na confirmação, voltar ao formulário de solicitação com e-mail preservado, sem envio automático. Testar os dois caminhos e confirmar que o código consumido continua bloqueado. Evidência local: 22 testes `test_password_recovery.py` passaram; `reflex compile --dry` aprovado; `openspec validate recuperar-senha-codigo-6-digitos --type change` aprovado. Os testes confirmam limpeza da confirmação sem requisição e preservação do e-mail; o código usado continua protegido pelo bloqueio de repetição já testado.

## 3. Publicação e entrega real

Confirmação posterior do usuário em 11/11/2026: recebeu código, trocou a senha,
entrou com a senha nova e localizou o cadastro.
[Evidência manual e limites por critério](validation/aceite-usuario-2026-11-11.md).
Ainda não fechar 3.2: replay, rejeição da senha/sessão antiga e restauração
específica desta conta não foram confirmados neste ciclo. Registros anteriores
de ausência de recebimento preservam o estado das respectivas consultas.

Ensaio autorizado em 11/11/2026: login e pedido aceitos, mas usuário não recebeu
o código. [SendGrid confirmou adiamentos 421/4.7.32](../melhorar-email-recuperacao/diagnostico-entrega-2026-11-11.md).
Nenhuma troca de senha executada até esse diagnóstico; 3.2 permanece aberta.

Investigação posterior do cadastro feito pelo usuário no app confirmou por
leitura user ativo, perfil e duas listas em workspace 147717/v1/live; recuperação
da mesma conta retornou 200, mensagem adiada no SendGrid. [Persistência confirmada](validation/cadastro-persistencia-2026-11-11.json).
Sem alterações remotas e sem concluir entrega pela aceitação do pedido.

Preparação local de 3.2 em 11/11/2026: adaptar executor para segundo código na
restauração, testar fluxo completo/timeout/replay e ausência de segredos; manter
3.2 aberta até ensaio real especificamente autorizado e caixa controlada.

Executor adaptado e 14 testes simulados aprovados:
[evidência, limites e roteiro para autorização](validation/executor-dois-codigos-2026-11-11.md).
Sem execução real, sem fechamento de 3.2.

- [x] 3.1 Exportar estrutura, revisar delta limitado e publicar contratos de reset; verificar dry-run posterior sem mudanças, sem importar registros/segredos.
- [ ] 3.2 Comprovar chegada do e-mail com seis dígitos, troca de senha, novo login e rejeição de reutilização em conta com caixa controlada; registrar resultado e restauração segura da conta de teste. [Bloqueado: depende de caixa controlada, domínio autenticado e validação real de entrega.]

Ensaio controlado em 12/11/2026: recebimento do primeiro código informado pelo
usuário; troca por senha temporária, novo login, rejeição da senha anterior,
código consumido e sessão anterior confirmados. O segundo pedido foi aceito,
mas a validação do segundo código retornou HTTP 403 antes da restauração. A conta
permanece com restauração pendente; o usuário recusou um terceiro pedido, que
não foi executado. 3.2 continua aberta.
[Registro sanitizado e limites](validation/ciclo-controlado-2026-11-12.md).
- [x] 3.3 Capturar resultado do serviço de e-mail e impedir sucesso silencioso quando o provedor retorna erro dentro de HTTP 200; verificar rejeição sanitizada e preservação dos caminhos genéricos, registrando separadamente validação local e publicação.
- [x] 3.4 Integrar Resend/SendGrid no endpoint Xano com chave/remetente no ambiente privado; verificar contrato, falhas sanitizadas e envio aceito, publicar somente o endpoint após backup e conferir delta. SendGrid substituiu Resend: publicação restrita a um endpoint após backup, variáveis privadas verificadas e ambiente anterior preservado ([recibo sanitizado](../integrar-sendgrid-recuperacao/deployment.json)); o endpoint exige aceitação HTTP 202 e as falhas sanitizadas foram verificadas na implementação/testes da integração. O usuário confirmou recebimento do código, troca da senha e novo login ([aceite manual](validation/aceite-usuario-2026-11-11.md)). A entrega da integração não conclui o ciclo completo nem os critérios de replay/restauração, que permanecem em 3.2.

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

Retomada em 28/10: 24 testes locais de recuperação, cooldown e não repetição
de solicitação passaram; OpenSpec válido. A documentação oficial atual do
Resend confirma que `onboarding@resend.dev` só aceita o e-mail proprietário;
domínio verificado é necessário para outra caixa. Nenhuma solicitação, credencial,
conta ou senha real foi usada. **3.2 e 3.4 continuam abertas; 8/10 mantido.**
[Comandos, fontes e próximo passo](validation/elegibilidade-resend-2026-10-28.md).
