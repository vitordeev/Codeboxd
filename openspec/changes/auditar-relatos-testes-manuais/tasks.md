# Tasks

## 1. Auditoria documental
- [x] 1.1 Investigar os seis relatos em estados, páginas, transporte e contratos Xano; registrar evidências e limitações na auditoria.
- [x] 1.2 Criar backlog com seis IDs, prioridades, dependências, aceite e propostas independentes sem criar changes de correção.
- [x] 1.3 Verificar documentos, preservar alteração local e branch, registrar evidências e executar openspec validate auditar-relatos-testes-manuais --type change.

## Evidências — 29/10/2026

- [Auditoria](../../../docs/planning/codeboxd-auditoria.md): seis registros com observado/esperado, localização e grau de certeza; [backlog](../../../docs/planning/codeboxd-backlog.md): prioridades, dependências e aceite por ID.
- `git status --short` inicial: apenas M reflex.lock/package.json. Final: a mesma alteração preexistente e os diretórios novos docs/planning/ e desta change. Nenhuma ferramenta escreveu no arquivo preexistente. `git branch --show-current`: develop antes/depois; sem troca de branch.
- `git diff --check`: código 0, com aviso de conversão LF/CRLF no arquivo preexistente. Arquivos documentais novos revisados separadamente, pois ainda não rastreados.
- `openspec status --change auditar-relatos-testes-manuais --json`: proposal/design/tasks presentes, specs skipped por escopo documental.
- `openspec validate auditar-relatos-testes-manuais --type change`: válida; zero deltas aceitos por skip_specs.
- Validação funcional local/simulada, Xano remoto e navegador: não executadas nesta rodada. Nenhum bug marcado como reproduzido. Os testes históricos citados não são novos resultados.
- Changes corretivas somente sugeridas; nenhuma criada. Sem alteração de código/configuração do produto, sem commit, PR, implantação, sincronização ou arquivo de specs.

## Workflow follow-up
- Correções e respectivas reproduções funcionais aguardam autorização do usuário; não fazem parte das tarefas documentais concluídas acima.
