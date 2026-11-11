# Confirmação do usuário — recuperação no aplicativo, 11/11/2026

O usuário confirmou explicitamente que recebeu o código por e-mail, trocou a
senha e localizou o usuário no banco. Perguntado separadamente sobre novo login,
respondeu: «Sim, entrei com a senha nova».

Isso é evidência manual de recebimento, troca e novo login no app, não resultado
de teste simulado. A persistência do cadastro já havia sido conferida por leitura
independente: um user ativo, um perfil e duas listas no workspace 147717/v1/live.
O código e a nova senha não foram solicitados nem incluídos nos relatórios.

| Critério | Situação nesta rodada |
| --- | --- |
| Receber o código na caixa | Confirmado pelo usuário |
| Trocar a senha | Confirmado pelo usuário |
| Entrar com a senha nova | Confirmado em resposta específica |
| Localizar cadastro/persistência | Usuário confirmou; leitura independente anterior preservada |
| Reutilização do mesmo código rejeitada nessa conta | Ainda sem evidência desta jornada |
| Senha antiga e sessão anterior rejeitadas nessa conta | Ainda sem evidência desta jornada |
| Restauração da conta usada no ensaio | Não executada; o usuário usou o fluxo normal do app |
| Melhoria comparativa do tempo de chegada | Não medida; adiamentos SPF/DKIM não corrigidos |

Os relatórios dos executores encerrados continuam incompletos e não são
convertidos em passed=true por este relato. Validação real histórica de
restrições/revogação permanece apoio separado. SendGrid 2.2 e recuperação 3.2
continuam abertas por vínculo com os demais critérios do ciclo completo; registrar
o avanço sem declarar a change inteira concluída. A tarefa histórica Resend 3.4
continua exigindo reconciliação explícita da substituição por SendGrid.

Nenhum novo e-mail, login automatizado, troca/restauração de senha, alteração DNS
ou publicação foi executado para registrar esta confirmação. Não houve push,
merge ou arquivo. Sem autorização implícita para mutações administrativas.
