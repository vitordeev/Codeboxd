# Recuperação de senha — fechamento em 17/11/2026

**12/12 concluídas.** Usuário confirmou “deu certo”; o executor também comprovou restauração, novo login e identidade da conta em execução real.

## Evidência composta do aceite 3.2

- [Ensaio de 12/11](ciclo-controlado-retomada-2-2026-11-12.json): recebimento do código, senha temporária salva, login com ela, rejeição da senha anterior, do código usado e da sessão antiga. O segundo código retornou 403 antes de restaurar; o JSON histórico continua `passed=false` e não foi sobrescrito.
- [Restauração autorizada de 17/11](restauracao-autorizada-2026-11-17.json): `passed=true`, `phase=restored`, `restoration_needed=false`; código novo recebido, senha original salva, identidade do login e ID/e-mail em `/auth/me` conferidos em memória. Um novo pedido autorizado, seis chamadas totais e nenhuma repetição automática.
- A nova evidência referencia o SHA-256 do ensaio original, `4b8455564d19a1b58d42ca103fb96963652f17cd8d402914d463ec46928d4962`. Confirmação da mesma conta pelo operador na janela e identidade pós-login validada; dados privados não foram persistidos.

O campo `failure_reason=confirm_same_account_and_valid_matching_password` preservado no novo JSON refere-se a entrada local rejeitada antes da rede e corrigida na janela, não a uma falha posterior de restauração. Os estados finais e checks confirmam sucesso. Não afirmar que o erro 403 histórico foi diagnosticado ou corrigido: sua causa permanece indeterminada; uma credencial nova permitiu concluir a restauração pelo fluxo normal.

## Validações e limites

Seis testes novos do executor de restauração e 19 regressões do executor anterior aprovados com transporte simulado. Esses testes são separados do resultado real acima. Não houve publicação de contrato, alteração de DNS/remetente, senha temporária adicional ou acesso administrativo ao código. Sem domínio próprio e sem Docker.

O fechamento considera os critérios completos distribuídos entre ensaio original e restauração vinculada, sem fingir que houve um novo ensaio integral em 17/11. Ferramentas históricas têm caminhos ativos fixos; não devem ser reexecutadas após arquivamento sem nova change ativa, revisão de caminhos e autorização específica.

## Arquivamento executado

Arquivada em `2026-11-17-recuperar-senha-codigo-6-digitos`, com todas as 12 tarefas concluídas. Spec `password-recovery` sincronizada antes do arquivo, três requisitos e 11 cenários comparados integralmente ao delta; `--skip-specs` no CLI evitou reaplicação. Links relativos em 14 documentos ajustados com plano prévio e verificação de hashes. Suíte completa: **742 testes aprovados**, 101,440 s, log privado `.local/close-recovery-20261117-tests.log`. Validação final OpenSpec: **37/37** (32 specs e cinco changes ativas, incluindo a estratégia supersedida). `git diff --check` aprovado, apenas avisos LF/CRLF. Quadro vigente: quatro changes, 35/87 tarefas concluídas, 52 abertas; a estratégia supersedida acrescenta quatro tarefas abertas históricas.
