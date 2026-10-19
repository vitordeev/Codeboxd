# Validação da revisão documental — 13/10/2026

Este documento preserva a rodada documental inicial. Depois dela houve implementação de correções: 113 testes e compilação no `.venv` passaram. Estado atual e limitações estão no [relatório operacional](changes/corrigir-erros-operacionais/validation/correcoes-2026-10-13.md); as contagens abaixo descrevem a rodada anterior.

## Base de evidência

A reanálise local imediatamente anterior executou:

```powershell
venv\Scripts\python.exe -m unittest discover -s tests -q
venv\Scripts\python.exe -m reflex compile --dry
```

Resultado: 106 testes passaram; compilação Reflex passou. Os logs de falhas Kitsu são cenários negativos simulados da suíte. A primeira tentativa com `.venv` falhou por dependências ausentes; a execução válida usou `venv`. Não houve mudança de implementação entre essa execução e a revisão documental.

Os relatórios de setembro e os resumos locais foram lidos, sem executar scripts remotos. `.local/remote-results.json` registra 10 grupos de cenários de persistência. `.local/kitsu-live-result.json` registra ranking 20, busca 4 sem erros, ficha Cowboy Bebop com capa, 3 relacionados, 1 trailer, críticas vazias e resolução Naruto mantendo identidade legada. [Kitsu](../docs/KITSU.md) também registra navegador e deduplicação reais de 23/09.

## Critério de arquivamento

| Change | Evidência utilizada | Limite |
| --- | --- | --- |
| Modelo de dados | Checklist 37/37; testes Xano de setembro; contratos locais e validação OpenSpec | Não foi feita uma auditoria nova de todos os registros remotos |
| Fundação | Checklist original, relatórios auth/discovery, evidência Kitsu posterior e validação documental atual | Disponibilidade de APIs e regressões visuais não foram revalidadas hoje |
| Administração | Código, testes simulados, contratos e demo histórica | Continua ativa; publicação, testes diretos de autorização e smoke completo faltam |

Arquivar o escopo original não apaga as pendências posteriores de senha, imagem, armazenamento e ambiente: elas estão em [PENDENCIAS.md](PENDENCIAS.md).

## Verificações documentais

Comandos de encerramento:

```powershell
openspec validate --all --strict --no-interactive
openspec validate --archived --strict --no-interactive
openspec list --json
git diff --check -- openspec
```

A rodada de encerramento verificou contratos ativos/consolidados, checkboxes dos arquivos, ausência de marcadores malformados, links Markdown locais, equivalência entre deltas arquivados e specs principais e integridade das saídas históricas.

| Verificação executada | Resultado |
| --- | --- |
| `openspec validate --all --strict --no-interactive` | 17 itens passaram: 16 specs consolidadas e uma change ativa |
| `openspec validate --archived --strict --no-interactive` | Duas changes arquivadas passaram, sem tarefas abertas |
| `openspec list --json` | Somente gerenciamento-website ativa, 17/34 |
| Contagem e IDs comparados com o Git anterior | Modelo 37/37, fundação 87/87, administração 17/34; IDs numéricos originais preservados |
| Links Markdown locais | 38 referências verificadas em 56 arquivos Markdown; nenhuma quebrada |
| Equivalência de delta/spec principal | 16 capacidades correspondem integralmente; sem cabeçalhos de operação delta nas specs principais |
| Hash SHA-256 de resultados/scripts históricos | 11 arquivos não Markdown preservados byte a byte após o arquivamento |
| `git diff --check -- openspec` | Passou |

Saída estruturada: [documentation-checks-2026-10-13.json](documentation-checks-2026-10-13.json). Relatórios Markdown históricos receberam apenas uma nota de contexto atual; seus resultados de setembro foram preservados.

## Arquivamento e sincronização

As sete capacidades de dados e nove capacidades funcionais foram sincronizadas manualmente no formato de spec principal (`Purpose` e `Requirements`), preservando requisitos e cenários. O contrato de home foi reconciliado com as fileiras atuais antes da sincronização. A validação estrita e a comparação de todos os deltas passaram antes de mover as changes.

Em seguida, o CLI executou `openspec archive <change> --yes --skip-specs --json`: `--skip-specs` evitou reaplicar os deltas já sincronizados e conferidos. O campo `specsUpdated: false` na saída do comando descreve apenas essa fase do CLI; os contratos já estavam consolidados. Nenhuma validação foi desativada.

Diretórios finais:

- `changes/archive/2026-10-13-criar-modelo-dados-xano/`
- `changes/archive/2026-10-13-definir-fundacao-codeboxd/`

Os metadados `.openspec.yaml`, propostas, designs, tarefas, deltas e evidências existentes foram mantidos nos diretórios arquivados.

## Efeitos e limites

Esta alteração é documental e de organização OpenSpec. Não houve commit, publicação Xano, alteração de papel de usuário, criação de conta de teste nem inicialização de servidor. Os arquivos gerados `.states` já estavam modificados na retomada e foram limpos pela compilação da reanálise; não pertencem ao diff documental.
