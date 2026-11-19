## Why

Os documentos centrais do OpenSpec ainda exibem contagens e estados anteriores, embora as sete changes ativas e seus checklists já tenham avançado. Uma visão reconciliada é necessária para priorizar o encerramento sem confundir evidências históricas, testes locais e critérios remotos ainda bloqueados.

## What Changes

- Atualizar apenas as seções de estado atual em `openspec/README.md`, `openspec/CONTEXTO.md`, `openspec/PENDENCIAS.md` e `openspec/RELATORIO_STATUS.md`, preservando registros datados e históricos.
- Reconciliar a tabela das sete changes ativas com `openspec list --json` e os checklists atuais; documentar o total de tarefas e os critérios/bloqueios pendentes com links para evidências.
- Diferenciar claramente trabalho local, validação simulada, aceite remoto e validação de navegador; não marcar tarefas como concluídas nem arquivar changes nesta atualização documental.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. Esta mudança é exclusivamente documental e não altera comportamento do produto; `skip_specs: true` está definido no `.openspec.yaml`.

## Impact

Afeta somente os resumos documentais centrais em `openspec/`. A fonte de verdade será o status do CLI, os `tasks.md` das changes ativas e suas evidências mais recentes. Não altera código, contratos Xano, credenciais, dados, dependências, publicação, histórico arquivado ou a decisão de execução local sem Docker.
