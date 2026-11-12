## 1. Restrições e interface

- [x] 1.1 Restringir finalidade de credencial, política 8..128/confirmação, conta ativa e rejeição da senha atual sob lock no backend; verificar testes da lógica real e dry-run.
- [x] 1.2 Validar fronteiras na UI, mensagens por etapa e limpeza seletiva da sessão; executar regressões de recuperação e compilar Reflex.
- [x] 1.3 Registrar inventário das restrições existentes e reconciliar contrato ativo, validando OpenSpec e preservando histórico.

## 2. Publicação e validação

- [x] 2.1 Publicar apenas endpoint final após backup/prévia assinada e verificar delta remoto restrito sem alterar ambiente/tabelas.
- [x] 2.2 Executar matriz real em uma conta member descartável: sessão comum, credenciais inválidas, política, confirmação, mesma senha, sucesso, revogação e login; remover fixture e confirmar ausência, sem envio de e-mail.
- [x] 2.3 Registrar evidências/limites de cada camada e executar OpenSpec e git diff --check.

Evidências e limites em [validation.md](validation.md). Seis tarefas concluídas; demais changes mantêm suas pendências próprias de entrega por e-mail/navegador.
