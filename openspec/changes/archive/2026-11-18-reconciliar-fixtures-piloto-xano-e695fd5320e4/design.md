## Plano estrito

- Alvo: run `cbshared_e695fd5320e4`; user IDs 50/51; listas customizadas 125/126; workspace 147717.
- Pré-condições: confirmar usernames, role member, status ativo, dono 50, marcadores exatos, `default_key=null`, listas privadas e zero referências; confirmar admin 14 ativo.
- Remover listas pelo endpoint de metadata porque os tokens dos proprietários foram perdidos. As rotas da aplicação exigem `list.user_id == auth.id`; não existe bypass administrativo para delete. A exclusão direta não cria evento de auditoria da aplicação.
- Desativar usuários 51 e 50 pelo endpoint administrativo. Verificar os dois eventos `admin_account_status_changed` do ator 14 com os IDs-alvo.
- Nenhum retry; abortar em divergência, erro ou escrita incerta. Preservar recibo por ação e conferir itens/linhas não alvo.

## Limite

O lote funcional já passou nos checks registrados em `pilot-execution-e695fd5320e4-2026-11-18.json`; esta change cobre somente a reconciliação pendente, não repete nem invalida essas verificações.
