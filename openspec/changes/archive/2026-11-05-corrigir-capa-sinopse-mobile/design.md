## Context

Ver proposal.md. A regra móvel preserva a capa absoluta da composição desktop;
texto com largura de 80% intersecta uma imagem de até 42% no lado direito.

## Goals / Non-Goals

**Goals:** manter a capa proporcional e o texto integral em celulares.
**Non-Goals:** redesenhar desktop, trocar provedores ou alterar metadados.

## Decisions

Até 640px, usar fluxo vertical: capa relativa centralizada seguida do texto.
Retirar limites de 80% do título/sinopse. Preservar seletores e componentes.
Reduzir somente a opacidade deixaria a interseção e prejudicaria a capa;
reservar duas colunas estreitas prejudicaria textos longos.

## Risks / Trade-offs

Cartão móvel fica mais alto → altura acompanha a sinopse, sem truncar conteúdo.
Verificar 320/390/640px, placeholder e quatro tipos com CSS real no navegador.

## Migration Plan

Aplicar CSS, validar geometria e screenshots locais, compilar e reiniciar
a aplicação depois do ensaio funcional em andamento. Rollback: restaurar
somente a regra móvel anterior; nenhum dado ou endpoint envolvido.
