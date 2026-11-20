## Why

O trilho de filmes populares da página inicial depende de setas e de um botão separado para trazer a próxima página, enquanto a barra de rolagem ocupa espaço abaixo dos cards. A navegação deve ficar contínua: a pessoa percorre os cards e novos filmes são acrescentados ao chegar ao fim.

## What Changes

- Remover as setas, botões manuais e barras de rolagem visíveis de todas as prateleiras horizontais da página inicial.
- Buscar e acrescentar automaticamente a próxima página da coleção correspondente quando a pessoa se aproximar do fim de uma prateleira.
- Preservar a categoria, ordem e identidade de cada prateleira, evitando duplicatas e chamadas simultâneas.
- Encerrar novas consultas quando o provedor não tiver mais itens, sem alterar a navegação das buscas e páginas de descoberta.

## Capabilities

### New Capabilities

### Modified Capabilities
- `media-discovery`: todas as prateleiras horizontais da home carregam mais resultados ao alcançar o fim, sem setas, botões manuais ou scrollbar visível.

## Impact

Afeta prateleiras da página inicial em `Codeboxd_main/pages/social.py`, paginação no estado social e nos adaptadores de catálogo em `Codeboxd_main/state/social.py` e `Codeboxd_main/services/catalog.py`, estilos em `assets/codeboxd.css` e a especificação `media-discovery`. Não altera APIs, rotas nem a paginação da busca.
