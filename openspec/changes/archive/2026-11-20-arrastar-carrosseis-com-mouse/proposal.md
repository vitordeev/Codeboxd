# Proposal

## Why

As prateleiras horizontais do catálogo não oferecem arrasto com mouse na `develop`, então a navegação no desktop depende das setas ou da barra de rolagem. Adicionar arrasto direto torna a exploração das coleções de filmes mais natural sem alterar carregamento ou dados.

## What Changes

- Permitir arrastar horizontalmente as prateleiras de catálogo com o botão primário do mouse.
- Preservar cliques nos cards quando o ponteiro não ultrapassar o limiar de arrasto e suprimir somente o clique originado por um arrasto concluído.
- Manter foco e navegação por teclado, rolagem nativa por toque/trackpad, paginação e carregamento de mais resultados.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `media-discovery`: ampliar a interação das prateleiras horizontais para permitir navegação por arrasto com mouse.

## Impact

- Interface das prateleiras horizontais do catálogo, atualmente composta em `Codeboxd_main/pages/social.py` e estilizada em `assets/codeboxd.css`.
- Pode requerer um pequeno script de interação no cliente e testes locais de gestos, cliques e acessibilidade.
- Sem alterações em APIs, estado do servidor, provedores, dependências ou persistência.
