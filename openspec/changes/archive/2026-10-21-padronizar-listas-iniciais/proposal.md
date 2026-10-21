## Why

O usuário solicitou padronizar todas as contas com duas listas base vazias.
Confirmou excluir listas e itens existentes, permitindo criar listas personalizadas depois.

## What Changes

- **BREAKING** Migração única apaga listas atuais e seus itens, com backup anterior.
- Recriar `Quero ver / ler` e `Já assisti / li` vazias para todas as contas existentes.
- Garantir as duas listas no cadastro, mantendo criação de listas personalizadas.
- Preservar contas, catálogo, avaliações, notas e demais dados sociais.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `data-user-lists`: inicialização padrão e reset único autorizado das listas.

## Impact

Xano: user_list, user_list_item e contrato auth/signup. Utilitário de migração,
testes e evidências OpenSpec. Não executar reset ao navegar ou fazer login.
Execução local com `.venv`, sem Docker. Backup privado em `.local/`.
