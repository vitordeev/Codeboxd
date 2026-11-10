> **REVERTIDA a pedido do usuário. Bonecos e carregamento anteriores restaurados; logo preservada. Não retomar sem novo pedido.**

## Context

Os robôs do login são SVG inline; cadastro e descoberta usam `assets/mascot.png`. A logo tem asset próprio e não muda. Há flags existentes para operações gerais, home, ficha, biblioteca, perfil, discussão, feed e administração. A primeira entrega se divide em carregamento independente e prancha de ilustrações; cenas só após aprovação explícita da prancha. Os resultados das changes anteriores não comprovam esta entrega.

## Goals / Non-Goals

**Goals:** feedback de espera consistente e contextual, e uma proposta de evolução dos robôs com linguagem única.

**Non-Goals:** redesign completo, retomar a proposta Dobra rejeitada/cancelada, mudar autenticação, provedores, API, limites, tempos, caches ou dados. Sem Docker, publicação ou carregador global que bloqueie a página.

## Decisions

1. Criar componente `loading_status` com texto específico, indicador decorativo e variante inline/cards/rows. Usar `role=status`, anúncio educado e atômico; esconder placeholders da acessibilidade. Esqueletos sem controle interativo ou percentual fictício. Respeitar movimento reduzido.
2. Substituir indicadores textuais nos mesmos ramos condicionais das flags existentes: home/coleções, operações sociais, busca inicial, biblioteca inicial, detalhes da obra, perfil, comentários, feed e feedback administrativo. Acrescentar indicador nos botões de autenticação enquanto aguardam. Usar esqueletos somente quando falta conteúdo; preservar a política funcional existente e as ações de erro/repetição. Atualizações com conteúdo já disponível recebem apenas status inline.
3. Manter componentes estáticos limitados a poucos placeholders; não adicionar polling, duração mínima, timeouts artificiais ou novos eventos de estado. Não afirmar melhoria no tempo real de API.
4. Prancha inédita para evolução dos robôs: cinco papéis de cor `--illu-*`, 2px, cabeça ~1/3, olhos em pontos, boca em arco e detalhe de assinatura de carretel lateral. Três poses, três expressões e seis objetos. Apresentar SVG e prévia clara/escura a 360px/1440px. Não reutilizar Dobra como se aprovado.
5. Somente após aprovação: oito cenas (onboarding, vazio, 404, 500, sucesso, carregando, offline, sem resultados), SVG inline via componente `Illustration(name,size)`, grupos nomeados e IDs únicos, acessibilidade contextual, SVGO e <30 KB por cena. Remover assets antigos apenas depois da substituição validada. Preservar capas reais, uploads, avatares e logo.

## Risks / Trade-offs

- Flags sobrepostas anunciarem status duplicado → evitar status global quando existe status de seção para o mesmo carregamento; manter texto específico.
- Skeleton substituir dados úteis → mostrar somente com coleção vazia/sem dados iniciais; não alterar a lógica de busca ou mutações.
- Nova direção visual não agradar → aprovar a prancha antes de criar ou integrar cenas.
- CSS interferir no design existente → classes prefixadas `cb-loading`/`cb-skeleton`, sem alterações globais de paleta ou layout.

## Migration Plan

Adicionar componente/estilos, integrar nos ramos existentes e verificar compile, regressões e navegador local com fixtures. Publicar apenas proposta de ilustração na change até aprovação. Reverter somente essas integrações se necessário. Xano, TMDB, Kitsu, Open Library e resolução legada Jikan permanecem iguais.
