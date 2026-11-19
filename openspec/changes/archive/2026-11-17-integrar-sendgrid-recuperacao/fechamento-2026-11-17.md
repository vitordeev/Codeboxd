# Conclusão da integração SendGrid — 17/11/2026

## Critério verificado e decisão

A pendência 2.2 exige recebimento e ciclo de recuperação com caixa controlada, mantendo vínculo com 3.2 da change original. A implementação deste provedor não modifica geração, consumo de código nem restauração de contas (proposal/spec). A decisão de não usar domínio próprio foi explicitada pelo usuário nesta rodada; o remetente individual verificado permanece configurado.

A evidência mais recente do ciclo real, de **12/11**, confirmou individualmente recebimento, identidade da conta, troca por senha temporária, novo login e rejeição de senha/código/sessão anteriores. Esse conjunto completa o aceite funcional do provedor nesta change. Não se trata de concluir por HTTP 202, simulação ou relato sem login.

O mesmo ensaio teve falha posterior na restauração da conta, com HTTP 403 no segundo código. Esse resultado permanece **passed=false/restoration_needed=true** no relatório original. Não foi alterado nem descartado. Restauração continua sendo critério explícito de `recuperar-senha-codigo-6-digitos` 3.2, que permanece aberta; não é tarefa implementada pelo adaptador SendGrid. Esta conclusão não declara sucesso integral do ensaio nem fecha a change de recuperação.

## Evidências usadas

| Critério SendGrid | Evidência |
| --- | --- |
| Publicação/configuração privada preservada | [Recibo da implantação](deployment.json): somente emissor atualizado, backup/prévia e ambiente preservado |
| Código recebido, troca e novo login no app | [Confirmação manual de 11/11](../2026-11-17-recuperar-senha-codigo-6-digitos/validation/aceite-usuario-2026-11-11.md) |
| Jornada supervisionada com caixa controlada | [Registro real de 12/11](../2026-11-17-recuperar-senha-codigo-6-digitos/validation/ciclo-controlado-retomada-2-2026-11-12.json): checks individuais verdadeiros de chegada, troca, novo login, rejeições e revogação |
| Código publicado ainda é SendGrid/202, erro sanitizado, sem retry | [Conferência somente de leitura de 17/11](conferencia-2026-11-17.json) |
| Remetente configurado verificado atualmente | GET `/verified_senders` HTTP 200; comparação privada do remetente, somente booleano no relatório |
| Regressões locais da jornada e política | 45 testes aprovados: password_recovery 22, recovery_acceptance 19, resend_readiness 3, reset_password_policy 1 |

A conferência de 17/11 exportou apenas contratos (`env=false/records=false`), verificou referências às variáveis privadas e consultou o remetente na conta SendGrid local. Não exportou valores remotos de ambiente. Nenhum e-mail, novo login, código, troca de senha ou publicação remota nesta rodada. Primeira tentativa restrita retornou ConnectError; consulta autorizada fora do sandbox passou e substituiu somente o relatório desta nova conferência.

## Domínio próprio e limites mantidos

O usuário determinou que não haverá domínio próprio. [Single Sender Verification](https://www.twilio.com/docs/sendgrid/ui/sending-email/sender-verification) verifica uma caixa individual; [Sender Identity](https://www.twilio.com/docs/sendgrid/for-developers/sending-email/sender-identity) descreve essa opção quando não há DNS próprio. As recomendações do provedor sobre domínio autenticado e os adiamentos observados continuam documentados como limites de entregabilidade, não como obrigação de compra/configuração do projeto.

Recebimento histórico comprovado não garante prazo, chegada de todas as mensagens ou alinhamento SPF/DKIM do domínio de terceiro. Medição comparativa continua em `melhorar-email-recuperacao` 2.3, agora sem exigir domínio próprio. Restauração continua em recuperação 3.2; a recusa histórica de novo pedido não foi revogada por este fechamento. Não houve reenvio.

Resultado desta change: **5/5**. A spec do provedor foi sincronizada e comparada integralmente com `openspec/specs/recovery-email-delivery/spec.md`, preservando HTTP 404 para conta ausente/inativa. O texto anterior de resposta genérica era anterior à regra consolidada de elegibilidade e não a sobrescreveu. Ferramentas históricas de implantação não devem ser reexecutadas sem nova change ativa e caminhos revisados.

## Arquivamento executado

Conferência final após arquivamento: `.venv/Scripts/python.exe -m unittest discover -s tests -q` aprovou 736 testes em 234,414 s; log local em `.local/close-small-changes-final-tests.log`. `openspec validate --all --no-interactive` aprovou 37/37 itens (30 specs e sete changes ativas). `git diff --check` passou, com avisos de normalização LF/CRLF. Essas verificações são locais e não substituem restauração da conta, comparação real de entrega ou publicação remota.

Arquivada em `openspec/changes/archive/2026-11-17-integrar-sendgrid-recuperacao`. A sincronização foi feita e verificada antes da movimentação; o CLI recebeu `--skip-specs` apenas para evitar reaplicar um delta já sincronizado. Também foram arquivadas as duas changes documentais completas, `finalizar-projeto-2026-11-17` e `reconciliar-estado-changes-abertas`, ambas 4/4 e sem deltas de spec.

Os três caminhos de origem/destino foram resolvidos e verificados dentro do workspace antes do arquivo. Uma prévia de manutenção de links foi gerada antes das movimentações; depois delas, 19 destinos em 12 documentos foram rebaseados com conferência de hash do conteúdo anterior. Textos históricos e relatórios reais reprovados não foram convertidos em aceites.
