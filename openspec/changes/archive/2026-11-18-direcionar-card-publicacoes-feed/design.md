## Context

O dashboard renderiza quatro cards em uma grade responsiva. A rota do feed principal existente e `/feed`; o card de publicacoes atualmente nao tem destino.

## Goals / Non-Goals

**Goals:** manter os tres destinos administrativos atuais, ligar publicacoes ao feed principal e renderizar esse card por ultimo.

**Non-Goals:** criar uma area de moderacao de publicacoes ou mudar a grade responsiva.

## Decisions

- Reutilizar `href="/feed"` no card existente, pois essa e a rota principal de feed ja registrada na aplicacao.
- Mover somente a chamada do card de publicacoes para o fim dos quatro cards, sem reordenar os outros indicadores.

## Risks / Trade-offs

- Se a rota principal mudar no futuro, o destino do card precisa acompanhar o registro da rota.

## Migration Plan

Sem migracao. Rollback: remover o destino `/feed` e restaurar a posicao anterior do card.
