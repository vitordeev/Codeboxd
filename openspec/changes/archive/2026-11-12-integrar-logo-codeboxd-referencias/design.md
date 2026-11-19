## Context

As nove imagens em `Imagens/` foram visualizadas. `HomePage.png` e `MoviePage.png` mostram melhor a marca; `image 3.png` é o mascote já usado pelo app. Nenhum arquivo independente da logo foi encontrado. O helper `_logo_icon` é compartilhado por login, conta, páginas sociais e administração, incluindo a demonstração administrativa via seu import existente. Reflex 0.9.11.post1 e `.venv` estão disponíveis. TMDB, Kitsu, Open Library e compatibilidade Jikan não são afetados.

## Goals / Non-Goals

**Goals:** reproduzir o símbolo observado e aplicá-lo de forma consistente, nítida e com dimensões estáveis.

**Non-Goals:** redesign, alteração de mascotes, tipografia, rotas, provedores, dados ou publicação. A change de redesign anterior continua cancelada.

## Decisions

- Reconstituir o cubo em SVG transparente, com sinais `<>` e triângulo de reprodução. Não recortar screenshots com fundo preto: isso reduziria nitidez e carregaria pixels do layout.
- Usar `assets/codeboxd-logo.svg`, `viewBox` fixo e amarelo da paleta atual. É reprodução manual baseada nas referências, não o vetor-fonte original. A origem é material local fornecido no projeto, sem nova fonte de terceiros.
- Retornar `rx.el.img` no helper existente, com dimensões explícitas, `alt=""` e `aria-hidden` porque o nome Codeboxd já está adjacente. Manter texto e destinos dos links existentes.
- Adaptar somente seletores de tamanho que pressupõem SVG inline para também aceitar `.brand-icon`; manter layouts e demais seletores. Usar o mesmo asset em `rel=icon` SVG; preservar `favicon.ico` legado como fallback.
- Verificar SVG/XML e todos os importadores do helper, compilar e renderizar o asset com o CSS real em tamanhos móveis/desktop. Evidências do navegador usam markup de verificação local, não demonstram jornadas integradas ou publicação.

## Risks / Trade-offs

- Reprodução imprecisa por referência raster → preservar geometria principal e registrar fonte/limite; apresentar prévia ampliada e pequena.
- Seletores antigos não dimensionarem imagens → adaptar seletores específicos e conferir proporção/ausência de overflow.
- Cache do navegador → referência de asset hash quando disponível e favicon SVG explícito.

## Migration Plan

Adicionar asset, conectar helper e head, ajustar seletores, compilar e verificar navegador. Reverter somente esses arquivos/linhas se necessário. Sem migração de dados, Docker ou reinício da instância normal.
