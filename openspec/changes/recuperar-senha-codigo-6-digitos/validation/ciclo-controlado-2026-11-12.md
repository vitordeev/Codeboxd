# Ensaio controlado de recuperação — 12/11/2026

O usuário autorizou um ensaio em conta/caixa controladas, limitado a dois
pedidos de recuperação, uma troca temporária, verificações de login/reuso e
tentativa de restauração. Não houve alteração de DNS, remetente ou configuração
Xano.

O primeiro pedido foi aceito e o usuário informou o recebimento do código na
janela privada. O executor confirmou a identidade da conta, salvou a senha
temporária, confirmou login com ela e rejeição da senha anterior, do código
consumido e da sessão anterior. O segundo pedido de recuperação também foi
aceito. Após o usuário informar o segundo código, a validação de credencial de
recuperação retornou HTTP 403 antes de qualquer escrita de restauração.

O registro sanitizado permanece com `passed=false` e
`restoration_needed=true`. A conta de teste **não foi restaurada**. O usuário
não autorizou um terceiro pedido; portanto, nenhum pedido ou tentativa adicional
foi executado. Não marcar a task 3.2 como concluída. A janela local foi mantida
aberta para preservar o estado supervisionado; não repetir o código rejeitado
nem fechar a janela enquanto a restauração estiver pendente.

Evidência detalhada sem dados privados:
[relatório sanitizado](ciclo-controlado-retomada-2-2026-11-12.json).
