# Restrições de redefinição — 10/11/2026

## Resultado

Reforços publicados somente em reset/update_password: exige finalidade password_reset, conta ativa e versão vigente; valida de 8 a 128 caracteres com letra ASCII/dígito ASCII e confirmação; impede senha igual à atual sob lock, antes de gravar/incrementar versão. Guard global e demais rotas preservados. Não há trim/truncamento da senha.

Frontend valida limite antes de consumir código, diferencia erro de código de rejeição de senha/expiração/resultado incerto e limpa cookie/storage/identidade local somente para a conta recuperada. Campos/hint informam limite e senha diferente. Credencial de recuperação não é persistida como sessão.

Oito caracteres/letra/número são a regra existente do produto, não alegação de conformidade integral com todos os padrões. A orientação de política consistente, uso único, expiração e proteção de solicitações foi conferida na [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html). Mantida a escolha explícita do usuário de rejeitar endereço sem conta ativa, mesmo tornando existência de conta perceptível.

## Inventário da auditoria

| Restrição | Situação |
| --- | --- |
| Conta ativa para solicitar/validar/alterar | Mantida; explícita sob lock no endpoint final |
| Formato de seis dígitos ASCII | Existente no frontend e backend |
| Código em hash, válido por 15 minutos | Existente no esquema/gerador publicado |
| Cinco tentativas por código | Existente, persistida em transação; rejeição após commit |
| Reenvio após 60 segundos | Existente no backend e cliente |
| Código novo invalida anterior; código usado é consumido | Existente |
| Credencial intermediária de cinco minutos | Existente no emissor publicado |
| Credencial exclusiva de recuperação para trocar senha | Implementada nesta rodada; sessão normal rejeitada |
| Senha 8..128, letra/número, confirmação | Limite e validação explícita consistentes implementados |
| Senha diferente da atual | Implementada sob lock |
| Revogação após troca e proteção concorrente | Existente, mantida e revalidada no endpoint publicado |
| Sessão local da mesma conta após troca | Limpa; sessão local de outra conta preservada |
| Erro do código versus erro posterior | Mensagens específicas implementadas |
| Login automático após recuperação | Não ocorre; continua exigindo login |

## Validações locais

- 20 testes de recuperação, quatro de revogação e um da lambda real de política JS aprovados.
- Suíte completa: `.venv/Scripts/python.exe -B -m unittest discover -s tests -q` — **511 testes passaram**. Logs de falhas/rate limit emitidos pelos doubles de transporte são cenários simulados da suíte.
- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado.
- Fronteiras 7/8/128/129, Unicode, espaços sem trim, dígito não ASCII, feedback após código aceito e limpeza seletiva de sessão cobertos.
- CLI histórico tools/password_recovery_remote.py desativado antes de ações: sua restauração dependia de sessão comum e poderia falhar após trocar senha; precisa adaptação antes de novo ensaio com caixa real. Verificação de bloqueio não envia requisições.

## Publicação

`tools.recovery_email_release --change reforcar-restricoes-redefinicao-senha --endpoint update`: prévia HTTP200 com exatamente uma query; assinatura do estado e endpoint conferida na aplicação. Backup privado sem segredos em `.local/reforcar-restricoes-redefinicao-senha/before-without-secrets.xs`.

Mesmo comando com --apply: HTTP200 e exportação posterior confirmou somente GUID do endpoint final alterado, sem ambiente/tabelas/registros. Relatórios: [prévia](preview.json), [publicação](deployment.json).

## Execução remota real

Primeira tentativa via multidoc/debug falhou ao resolver tabela não incluída (`Invalid name`), antes de criar fixture real. Relatório inicial [preservado](remote-validation.json); leitura direta posterior confirmou zero contas correspondentes. Não contabilizar essa tentativa como aceite.

Executor ajustado para signup publicado, geração privada por /function/run sem mailer e consumo público do código. [Relatório real](remote-validation-api.json): **20 checks passaram**. Inclui sessão comum/credencial ausente/corrompida rejeitadas; política e confirmação rejeitadas; senha atual rejeitada sem invalidar sessão; troca com senha Unicode de 128 caracteres; replay e sessão antiga rejeitados; login com nova senha aprovado, senha antiga e variante apenas no último caractere rejeitadas (sem truncamento).

Criada uma única conta member com endereço sintético example.invalid. Sua conta, perfil e duas listas vazias foram removidos e ausência confirmada via metadados no finally. Eventos de auditoria preservados. Senhas, códigos e tokens ficaram em memória; o diário privado tem somente identidade sintética/ID de cleanup. Zero e-mails enviados e zero contas de usuários reais alteradas.

## Limites

Expiração de cinco minutos e bloqueio de conta desativada conferidos nos contratos; não se aguardou cinco minutos nem se alterou estado de uma conta real para revalidar esses casos. Não foi feito novo ciclo de chegada por Gmail nem inspeção visual da segunda etapa no navegador; UI validada por testes de estado e compilação. Entrega do e-mail continua sujeita ao alinhamento de domínio já diagnosticado em melhorar-email-recuperacao. Nenhum DNS, CAPTCHA, serviço de senhas vazadas ou rate limit global foi alterado.

## Conferência final

`openspec validate reforcar-restricoes-redefinicao-senha --type change` e validação de recuperar-senha-codigo-6-digitos aprovadas. `git diff --check` aprovado; backups e diário de fixture confirmados ignorados pelo Git. CLI histórico testado e bloqueou antes de criar saída ou executar requisições. Seis tarefas concluídas; sem sincronização/arquivamento nesta rodada.
