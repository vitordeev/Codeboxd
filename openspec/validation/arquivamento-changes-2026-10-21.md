# Revisão e arquivamento — 21/10/2026

Pedido: identificar changes finalizadas e movê-las para archive. Conferidos
`openspec list`, status dos artefatos, tarefas e evidências das entregas.
Nenhuma execução de produto, teste remoto ou nova migração nesta revisão.

## Arquivadas

| Change | Tarefas | Contrato consolidado | Destino |
| --- | --- | --- | --- |
| avaliar-meias-estrelas | 5/5 | media-interactions: escala, decimais e cenários adicionais; cenários anteriores preservados | [Archive](../changes/archive/2026-10-21-avaliar-meias-estrelas/tasks.md) |
| corrigir-erros-operacionais | 7/7 | operational-reliability: quatro requisitos de arquivos, ambiente, uploads e banner | [Archive](../changes/archive/2026-10-21-corrigir-erros-operacionais/tasks.md) |
| padronizar-listas-iniciais | 7/7 | data-user-lists: dois requisitos de cadastro/reset único e preservação de personalizadas futuras | [Archive](../changes/archive/2026-10-21-padronizar-listas-iniciais/tasks.md) |

Todos os artefatos estavam completos. As evidências de meias estrelas incluem
navegador/Xano; correções operacionais têm verificação local histórica, sem Docker;
listas têm migração real e contrato publicado, com personalizadas testadas localmente.
Arquivar não amplia a camada de validação registrada nem encerra pendências de
outras changes, como build, e-mail, administração ou rotação de credenciais.

Specs mescladas antes do movimento, usando as regras atuais de cada artefato.
`openspec validate --specs --strict`: 17 specs aprovadas. As três changes também
passaram na validação estrita. Arquivamento por CLI com `--skip-specs --yes --json`
após a mesclagem manual: `specsUpdated: false` no retorno indica que o comando
não repetiu a sincronização já executada, e não ausência de contratos consolidados.
Pastas e `.openspec.yaml` preservados. Links locais afetados pelo movimento corrigidos.

## Permanecem abertas

| Change | Progresso | Motivo |
| --- | --- | --- |
| otimizar-performance-app | 11/37 | Implementação restante, build, metas, medições e integração |
| gerenciamento-website | 17/34 | Critérios administrativos reais e interface |
| exigir-texto-denuncias-avaliacoes | 3/5 | Rejeição autenticada e navegador |
| recuperar-senha-codigo-6-digitos | 7/8 | E-mail e troca completa em caixa controlada |
| traduzir-descricoes-deepl | 5/6 | Verificação visual da integração |
| exigir-openspec-para-implementacoes | 0/4 | Critérios de processo ainda abertos; não encerrar apenas por existir orientação parcial |
| regularizar-merge-e-commits | Sem tarefas | Scaffold sem artefatos completos; commits de merge históricos não comprovam todos os critérios de uma change sem planejamento |

Não marcar tarefas pendentes como concluídas apenas para permitir arquivamento.
As duas changes arquivadas em 13/10 permanecem intactas.

Atualização posterior no mesmo dia: por novo pedido do usuário,
`exigir-openspec-para-implementacoes` e `regularizar-merge-e-commits` foram
implementadas/revisadas, validadas e arquivadas em 4/4 cada. A tabela acima e o
resultado 23/24 abaixo preservam o estado da primeira revisão.
[Encerramento posterior](encerramento-processo-git-2026-10-21.md).

## Conferência final

- Correspondência conferida para os sete requisitos dos três deltas e seus
  cenários; requisitos e cenários preexistentes preservados nas specs principais.
- Nove documentos afetados/referenciados conferidos sem links locais quebrados.
- `git diff --check` aprovado (somente avisos de conversão LF/CRLF).
- `openspec list --json` confirma sete changes restantes e ausência das três
  arquivadas na lista ativa.
- `openspec validate --all --strict`: 23 itens aprovados e um reprovado, o
  scaffold preexistente `regularizar-merge-e-commits`, sem artefatos completos.
  Não declarar validação global integral nem modificar seu escopo para arquivá-lo.
- Nenhum novo teste de aplicação executado: esta rodada altera documentação,
  consolida specs e move pastas; a validação usa OpenSpec e conferência de links.
