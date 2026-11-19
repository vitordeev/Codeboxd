## 1. Verificação e remoção controlada

- [x] 1.1 Revalidar `user_list.id=110` contra a identidade autorizada e conferir zero linhas em `user_list_item` referenciando-a; salvar recibo write-ahead sem payload privado. Recibo registra hash exato e referências vazias.
- [x] 1.2 Enviar exatamente um DELETE para `user_list.id=110`, sem retry; confirmar que a linha sumiu e que todos os outros hashes de listas e itens permanecem iguais. HTTP 200; lista 110 ausente, outros 30 hashes de lista e seis itens preservados.
- [x] 1.3 Registrar resultado no recibo e validar `openspec validate remover-lista-orfa-110 --type change` e `git diff --check`. Evidência: `deletion-execution.json` aprovado; validação OpenSpec aprovada.
