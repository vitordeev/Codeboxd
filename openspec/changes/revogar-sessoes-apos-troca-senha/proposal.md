## Why

A verificação remota da change proteger-credenciais-expostas comprovou que sessões anteriores continuam aceitas após trocar a senha. É necessário invalidá-las no backend para concluir a tarefa 2.3 daquela change.

## What Changes

- Versionar sessões por conta, emitir claims de versão/finalidade e verificar todas as rotas autenticadas do workspace.
- Alterar senha e versão de forma atômica, invalidando sessões e credenciais de recuperação anteriores sem afetar outras contas.
- Separar finalidade de sessão comum e recuperação; token de recuperação não concede acesso social/administrativo.
- **BREAKING**: tokens legados sem versão deixam de ser aceitos e exigem novo login na implantação.
- Publicar alteração limitada no Xano após backup sem dados/segredos, dry-run revisado e validação local/remota. Preservar dados e outras changes; operação local sem Docker.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `user-authentication`: revogação após mudança de senha, rejeição de tokens legados e isolamento de credenciais de recuperação.

## Impact

Tabela user, emissão e validação de tokens Xano, rotas protegidas incluindo catálogo legado e logs, testes e ferramentas de publicação/validação. Não implementar refresh token, notificações, alteração de papéis ou revogação global por logout. Git commit/push serão executados manualmente pelo usuário.
