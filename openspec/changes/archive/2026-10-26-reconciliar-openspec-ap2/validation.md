# Revisão documental para a AP2 — 26/10/2026

## Achados e correções

1. Os centrais apresentavam administração 17/34 ou 19/34, performance 11/37 e
   tradução ainda ativa. Reconciliados para 21/34, 14/37 e DeepL arquivada 6/6.
2. Dois checklists arquivados da fundação repetiam IDs 5.2 e 11.7 por marcadores
   de merge de oito caracteres. Removidas as duplicações: 87 tarefas únicas em
   cada diretório. Designs reconciliados; narrativas originais em `antes/`.
3. Leituras admin reais de 23/10 existiam na change de performance. Os resumos
   agora as reconhecem, sem atribuir conclusão às mutações e ao browser administrativo.
4. Resend já escolhido e publicado em 22/10. Envio aceito, chegada na caixa e
   ciclo real continuam pendentes; não falta escolher provedor.
5. Os 14 diretórios de arquivo anteriores estão concluídos nos seus checklists.
   Cópias da fundação/modelo em datas diferentes são histórico preservado,
   não funcionalidades adicionais nem motivo para apagar uma das versões.

## Decisão de arquivamento

| Change | Decisão e evidência |
| --- | --- |
| gerenciamento-website | Manter ativa: 13 critérios abertos, incluindo autorização, mutações, auditoria e browser real |
| otimizar-performance-app | Manter ativa: 23 critérios abertos, incluindo jornadas completas, comparações e metas restantes |
| recuperar-senha-codigo-6-digitos | Manter ativa: 3.2 e 3.4 abertas, sem envio/entrega/ciclo comprovados |
| reconciliar-openspec-ap2 | Arquivar após validação documental; sem deltas funcionais (`skip_specs: true`) |

## Comandos e resultados

Antes do arquivamento: `openspec validate --all --strict --no-interactive`
aprovou 23 itens; `openspec validate --archived --strict --no-interactive`
aprovou 14. `git diff --check -- openspec` aprovado.
Inventário em [audit.json](audit.json), gerado por [audit.py](audit.py).
Após o arquivamento, validação repetida nos caminhos finais: **22 itens ativos/specs
e 15 changes arquivadas aprovados**, zero falhas. Auditoria final: **221 documentos
Markdown e 323 links locais**, nenhum link quebrado, marcador de merge ou ID
duplicado; todos os checklists têm metadados e todos os arquivados estão sem
tarefas abertas. `git diff --check -- openspec` aprovado.

## Limites e preservação

Somente documentação alterada. Não foi repetida a suíte histórica de 374 testes,
nem executados Reflex, navegador ou serviços remotos. Alteração preexistente em
`reflex.lock/package.json` preservada. Nenhum commit criado.
Snapshots `.txt` em `antes/` mantêm os documentos anteriores literalmente,
inclusive referências relativas e marcadores antigos como evidência de origem;
não são documentos ativos nem entradas do validador Markdown.
Validação documental não comprova funcionamento atual ou equivalência semântica
integral entre código e specs. Não houve uso de Docker.
