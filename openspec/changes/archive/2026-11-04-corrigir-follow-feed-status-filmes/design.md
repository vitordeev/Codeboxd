## Context

Ver proposal.md. Inventario atual confirma somente `.openspec.yaml` antes
desta rodada; o historico Git possui um commit para esse diretorio. Nao ha
contrato proprio a implementar ou migrar. A entrega funcional relacionada
esta arquivada em `2026-11-04-corrigir-conexoes-feed-listas`.

## Goals / Non-Goals

Preservar rastreabilidade de um scaffold supersedido, sem duplicar entrega.
Nao criar funcionalidade nova ou marcar trabalho de outra change como proprio.

## Decisions

Definir escopo documental explicito e validar antes do arquivo. O marcador
skip_specs decorre da ausencia de novos requisitos neste encerramento, nao
de uma excecao para esconder implementacao pendente. O resultado deve se chamar
supersedido, nunca nova correcao funcional entregue.

## Risks / Trade-offs

Confusao de contagens: as tarefas desta change sao apenas de reconciliacao;
os dez criterios funcionais pertencem exclusivamente a entrega vinculada.

## Migration Plan

Nenhuma migracao, dependencia ou provedor alterado. Sem Docker. Rollback
documental pode restaurar a pasta ativa e seus links, preservando a entrega
funcional arquivada e as specs consolidadas.
