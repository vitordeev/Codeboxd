# Executor supervisionado com dois códigos — 11/11/2026

## Implementação local vinculada à tarefa 3.2

`tools/password_recovery_remote.py` substitui o fluxo histórico incompatível.
A restauração é outra recuperação, com código recebido da caixa e credencial
reset-only nova. Nenhuma atualização usa a sessão comum do login inicial.
Essa sessão é usada somente para conferir rejeição em `/auth/me` após a troca.

Máquina de estados impede repetir a primeira troca, reenviar automaticamente
ou restaurar duas vezes. Antes da escrita de senha, o relatório registra
restauração pendente. Timeouts não são interpretados como rollback; o operador
confirma login original ou solicita a segunda recuperação após o cooldown.
Resultado incerto na restauração permite conferir o login original sem repetir
a escrita. Sem confirmação, a pendência continua explícita.

No máximo duas solicitações de e-mail, duas tentativas de escrita de senha e
24 chamadas ao todo; intervalo mínimo local de 2,2s e cooldown de 61s contado
após a resposta do primeiro pedido. Sem redirects ou retries. Ao esgotar código,
credencial, rede ou orçamento, interromper o ensaio e usar recuperação manual.
O executor não garante restauração se a caixa/rede ficar indisponível ou o
processo for encerrado à força. A senha temporária não é guardada em disco.

Relatório de destino exige criação exclusiva; credenciais, e-mail, código,
senha e corpos de resposta nunca são incluídos. Somente referência de aprovação
em SHA-256, fases, contagens e checks fixos. Transporte MockTransport é marcado
como simulado. Identidade retornada em cada credencial é conferida antes de
alterar a senha. Falha de escrita de evidência impede a próxima chamada remota.

O tempo `operator_observation_seconds` inclui espera/digitação do operador:
nunca usá-lo como latência SMTP, tempo exato de chegada ou melhoria antes/depois.
Não fecha a tarefa 2.3 de melhorar-email-recuperacao.

## Validação

- `python -B -m unittest discover -s tests -p test_recovery_acceptance.py -q`:
  **14 testes passaram**, transporte em memória, sem rede real.
- Casos: ciclo completo/restauração, timeout com e sem commit na primeira troca,
  timeout na restauração, código rejeitado/expirado, identidade divergente,
  formato inválido sem rede, cooldown/replay, envio incerto sem retry,
  evidência já existente, falha de journal, contrato de login malformado,
  orçamento esgotado e CLI sem autorização sem rede/leitura de configuração.
- Teste completo confere os dois tokens reset-only distintos, retorno à senha
  original e ausência dos valores privados conhecidos no JSON.
- `python -B -m unittest discover -s tests -q`: **580 testes passaram em
  21,244s**, após as alterações finais de código. Log privado:
  `.local/tests-executor-2026-11-11.log`.
- `openspec validate recuperar-senha-codigo-6-digitos --type change` e
  `openspec validate integrar-sendgrid-recuperacao --type change`: aprovados;
  avisos preexistentes de requisitos longos preservados.
- `git diff --check`: aprovado. Diff revisado; alteração restrita ao executor,
  seu teste e acompanhamento OpenSpec. Aplicativo Reflex não foi modificado,
  compilação/reinício não necessários.

Não há evidência de interface GUI real nesta rodada; a janela não foi iniciada.
Não houve envio real, login remoto, troca de senha, alteração de domínio,
publicação, push ou merge. Tarefa 3.2 permanece aberta.

## Ensaio concreto para autorização específica

Destino: API de autenticação configurada no `.env` privado existente; a janela
aceita somente uma conta controlada indicada pelo usuário. Usar a mesma caixa
nas duas etapas. Escopo: até dois e-mails, uma senha temporária e retorno à
original (duas escritas), login novo, rejeição da senha anterior/código usado e
sessão inicial, até 24 chamadas. Contas, tabelas e imagens não serão criadas ou
excluídas. Sem alteração de DNS, remetente ou configuração Xano/SendGrid.

Somente após autorização registrada, executar na worktree de e-mail:

```powershell
& 'D:/Repositorios GIT/Codeboxd/.venv/Scripts/python.exe' -B -m tools.password_recovery_remote --execute --approval-reference '<referência da autorização específica>' --config 'D:/Repositorios GIT/Codeboxd/.env' --output 'openspec/changes/recuperar-senha-codigo-6-digitos/validation/ciclo-real-sendgrid-2026-11-11.json'
```

`--execute` e referência são guardas operacionais, não prova de autorização.
Não executar o comando antes da aprovação específica deste escopo. Se o
relatório já existir, escolher outro nome e preservar a tentativa anterior.

Na janela privada: informar e-mail/senha Codeboxd, solicitar primeiro código,
confirmá-lo e executar verificações. Após 61s, solicitar a restauração e
informar o código dessa segunda mensagem. Verificar fase restored e confirmação
de login original. Não enviar senhas ou códigos no chat. Se houver timeout,
não repetir escritas: usar a conferência de login original e seguir o estado
indicado. Se não restaurado, manter pendência e recuperar pela interface normal.

Somente considerar 3.2/SendGrid 2.2 concluídas após revisar evidência real e
confirmação do operador; execução local/testes não satisfazem esses critérios.

## Início do ensaio autorizado

Após apresentação do escopo acima, o usuário respondeu «pode prosseguir».
A janela foi iniciada com execução fora do sandbox e configuração privada
existente. Relatório exclusivo criado às 14:11 UTC de 11/11/2026 em
`ciclo-real-sendgrid-2026-11-11.json`. No primeiro acompanhamento, checks vazios:
aguardando preenchimento pelo operador, sem chamadas ou alterações remotas.
Isso registra início supervisionado, não aceite ou entrega. Não iniciar outro
executor enquanto esta janela estiver aberta.

## Interrupção no login e correção de diagnóstico

Usuário informou não conseguir entrar. Primeiro executor terminou com código 1;
evidência preservada: uma chamada tentada, phase initial_login, checks vazios,
zero pedidos de e-mail e restoration_needed=false. Não houve tentativa de troca.
A versão inicial não persistia status HTTP ou motivo fixo da falha, portanto
esse JSON sozinho não distingue rejeição, rede ou formato de resposta.

Consulta somente de leitura ao histórico Xano retornou 200 e encontrou três
logins recentes com 403 e um 200; não foram obtidos timestamps no resumo,
portanto não atribuir automaticamente um desses status à tentativa do executor.
[Resumo sem inputs/corpos](login-diagnostico-2026-11-11.json).

Executor corrigido para registrar somente último status HTTP e motivo fixo do
erro, mostrar instrução de uso da senha atual Codeboxd e permitir até três
tentativas MANUAIS quando a chamada inicial retorna 401/403. Nenhuma repetição
automática, envio ou mudança de senha antes do login válido. Senha rejeitada é
descartada da memória do Probe e do campo. Outros erros continuam interrompendo
sem repetir chamadas. Referência da autorização original continua válida para
o mesmo ensaio e a mesma conta controlada; primeiro relatório não sobrescrito.

`test_recovery_acceptance.py`: **16 testes passaram** após a correção, incluindo
nova tentativa manual sem envio prévio, status sanitizado e bloqueio da quarta
tentativa. OpenSpec da change e git diff --check aprovados. Suíte de 580 é
evidência anterior; não reexecutada integralmente após este ajuste de diagnóstico.

## Login aceito e ação fora de etapa

A tentativa2 confirmou controlled_account_login=true e pedido de código aceito,
com duas chamadas HTTP 200, um pedido de e-mail, phase awaiting_first_code e
restoration_needed=false. Usuário informou operation_not_available: nenhum novo
envio ou escrita ocorreu com essa ação rejeitada. Executor terminou com código
1 após fechar a janela. Aceitação do pedido não comprova recebimento.

Corrigida disponibilidade de botões conforme a fase, instruções em português e
contagem para cooldown. Entrada incorreta sem mudança de fase não apaga o código.
Retomada de pedido pendente exige evidência compatível, mesma referência de
autorização, idade inferior a 15min, zero troca iniciada e exatamente um pedido.
Solicita novamente login da mesma conta, sem enviar primeiro e-mail outra vez;
mantém orçamento de dois pedidos e herda contagem de chamadas. Não calcula
latência de observação no caso de retomada. Backend continua autoritativo para
expiração/identidade do código, que pode ter expirado durante a interação.

`test_recovery_acceptance.py`: **19 testes passaram**, incluindo disponibilidade
por fase, retomada completa com somente dois pedidos ao todo e recusa de retomar
uma troca já iniciada. OpenSpec e git diff --check aprovados. Janela corrigida
aberta em modo pending-request; relatório novo `ciclo-real-sendgrid-2026-11-11-retomada.json`,
preservando tentativa2. Nenhum código/senha foi recuperado de disco; operador
precisa informar novamente na janela privada. Aceite real continua aberto.

Após as correções finais, suíte completa executada: **585 testes passaram em
27,146s**, log privado `.local/tests-retomada-2026-11-11.log`. Acompanhamento da
retomada confirmou login 200 e fase awaiting_first_code, sem escrita de senha
ou outro pedido de e-mail, aguardando código pelo operador.

Após diagnóstico de adiamento do primeiro destinatário, usuário solicitou
explicitamente reabrir para testar outro e-mail. Processo anterior confirmado
encerrado, restoration_needed=false, sem troca de senha. Novo ensaio iniciado
com referência própria de autorização e relatório exclusivo
`ciclo-real-sendgrid-2026-11-11-outro-email.json`, sem pending-request. Mantidos
os limites por ensaio (dois pedidos, duas escritas e 24 chamadas); dados da nova
conta serão informados exclusivamente pelo operador na janela privada. Isso
não corrige nem encerra o bloqueio de alinhamento do remetente já documentado.
