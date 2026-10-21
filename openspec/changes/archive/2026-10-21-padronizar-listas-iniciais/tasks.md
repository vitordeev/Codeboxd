## 1. Contrato e preparação

- [x] 1.1 Confirmar exclusão de listas e itens e permissão para listas personalizadas futuras; registrar escopo autorizado.
- [x] 1.2 Conferir signup remoto e garantir duas listas vazias na transação do cadastro; verificar contrato sem duplicar implementação existente.
- [x] 1.3 Implementar migração única com backup integral de listas/itens, plano e bloqueio de repetição; verificar testes de falhas e escopo restrito.

## 2. Execução e validação

- [x] 2.1 Inventariar contas, salvar backup privado e verificar integridade antes de qualquer exclusão.
- [x] 2.2 Executar reset uma vez e conferir exatamente duas listas base vazias por conta, sem alterar outras tabelas.
- [x] 2.3 Verificar criação de lista personalizada e preservação na navegação após reset; registrar testes e limites por camada.
- [x] 2.4 Consolidar evidências sanitizadas e caminho do backup privado, atualizando documentos centrais.

Migração validada no Xano; signup publicado e conferido por exportação. Criação/
preservação de personalizada verificadas localmente pelos handlers, sem navegador
ou novo cadastro real. [Execução, recuperação do 429 e limites](validation/execucao-2026-10-21.md).
