> Estado reconciliado em 26/10/2026: 8/10 tarefas concluídas. Resend integrado e publicado em 22/10 após falha do serviço nativo. Provedor/remetente já escolhidos; resta destinatário elegível ou domínio verificado, envio aceito e chegada/ciclo completo. 3.2 e 3.4 continuam abertas; não arquivar. As seções e rodadas anteriores abaixo preservam o planejamento e sua evolução; o checklist e a evidência datada prevalecem sobre resumos antigos.

## Why

O usuário exige recuperação de senha com código de exatamente seis dígitos enviado
ao e-mail cadastrado. O fluxo atual usa um UUID como código e ainda não tem
validação de entrega real; a pendência P.6 passa a ser acompanhada nesta change.

## What Changes

- Gerar código numérico de seis dígitos no Xano e enviar por e-mail.
- Validar formato, prazo, uso único e limite de tentativas; restringir reenvio.
- Preservar respostas genéricas para não revelar se um e-mail está cadastrado.
- Ajustar o formulário e validar backend, interface e entrega em conta controlada.
- **BREAKING**: códigos UUID antigos deixam de ser aceitos; solicitar um novo código.

## Capabilities

### New Capabilities

- `password-recovery`: Recuperar senha por e-mail com código numérico de seis dígitos.

### Modified Capabilities

Nenhuma: autenticação comum permanece coberta pelos contratos consolidados.

## Impact

Função `Quick Start/generate_magic_link`, endpoints de reset Authentication,
objeto `user.password_reset`, SessionState, página `/redefinir-senha` e testes.
Execução local com `.venv`, sem Docker. Migração aditiva, publicação limitada ao
reset e evidências sem códigos, hashes, senhas, tokens ou e-mails pessoais.
