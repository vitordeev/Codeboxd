# Retomada da medição de entrega — 17/11/2026

Escopo: tarefa 2.3, única aberta (4/5). A integração SendGrid foi arquivada; este aceite mede chegada, sem trocar senha, validar código ou alterar remetente/DNS.

## Procedimento preparado

1. Aguardar autorização específica para um único pedido à conta controlada. A recusa anterior a novo pedido continua válida até resposta explícita. Não executar o fluxo completo de `tools/password_recovery_remote.py`, pois ele também troca senha.
2. Identificar privadamente a conta e o endpoint canônico já configurados. Registrar instante UTC anterior ao pedido e duração da resposta separadamente. Executar uma única solicitação, sem retry; resposta aceita não comprova entrega.
3. Pedir somente confirmação de chegada e horário observado, sem código no chat. Registrar se o horário veio do cabeçalho da mensagem ou da observação do usuário; esta última inclui atraso de percepção/comunicação.
4. Se disponível, consultar a atividade SendGrid somente por leitura, correlacionando destinatário e janela em memória. Registrar apenas tempos, estados e contagens; não guardar e-mail, identificador da mensagem, código, token ou corpo.
5. Distinguir pedido → chegada observada, pedido → resposta da API e processed → delivered. Não comparar intervalos diferentes como se fossem equivalentes. Os 27s/70s históricos são tempos do provedor, não baseline comprovada anterior à mudança de template.
6. Comparar apenas amostras equivalentes cuja posição antes/depois esteja demonstrada. Sem baseline equivalente, registrar a nova observação e manter a comparação pendente; uma amostra não comprova melhoria geral. Não republicar template antigo nem enviar mensagens adicionais para fabricar baseline.
7. Registrar atrasos, ausência de entrega ou falta de acesso honestamente. Sem entrega/comparação comprovadas, manter 2.3 aberta e não arquivar a change. Nenhum domínio próprio é necessário.

## Estado desta retomada

Planejamento e evidências anteriores revisados. O usuário autorizou explicitamente: “Autorizado pode realizar”, para um único pedido sem troca de senha. Como o destinatário controlado não está salvo no `.env`, foi aberta uma janela local para entrada privada, com botão de envio único e confirmação de chegada, sem solicitar senha ou código.

Executor privado: `.local/measure-recovery-mail-20261117.py`; `python -m py_compile` aprovado. A saída sanitizada será `medicao-autorizada-2026-11-17.json`, criada exclusivamente antes da chamada para impedir reexecução. Sem retry, redirecionamento ou persistência do destinatário. Falha de rede será registrada como resultado incerto, sem novo pedido. Confirmação pelo botão mede até a observação do operador, incluindo seu atraso de reação; não é horário exato de entrada na caixa.

## Resultado real

[Relatório sanitizado](medicao-autorizada-2026-11-17.json): um pedido às 14:11:07,804 UTC, HTTP 200 em 4,521 s; operador confirmou chegada na janela às 14:11:32,767 UTC, 24,962 s após o início. Zero retries e zero trocas de senha. Nenhum código foi solicitado ou validado. A confirmação de chegada veio da ação explícita do operador, não da resposta da API.

Esse intervalo inclui observação/reação do operador. Os 27s/70s históricos medem processed → delivered, sem baseline pré-template equivalente; portanto não é válido afirmar redução percentual ou melhoria antes/depois comparando esses números. Não republicar o template antigo nem fazer um segundo envio sob esta autorização. `comparison_available=false` permanece explícito no relatório. A parte de chegada real foi demonstrada, mas a tarefa 2.3 continua aberta pela comparação não comprovada, 4/5.

Validação desta retomada: compilação sintática do executor, `openspec validate melhorar-email-recuperacao --type change` e `git diff --check` aprovados. Não houve alteração de código do aplicativo ou publicação Xano. O teste não restaura a conta e não conclui a tarefa 3.2 da recuperação.
