# Retorno às rotas existentes — 18/11/2026

## Decisão aplicada

Após o usuário apontar que a Home já possui busca de obras, foram removidas as
rotas novas `/buscar` e `/lista` e o item Buscar da navegação principal. A Home
(`/`) conserva seu campo de busca existente. A rota `/listas` conserva a seleção,
visualização e gerenciamento de listas no mesmo local.

## Evidências locais

- `reflex compile --dry`: sucesso.
- Compilação da tabela Reflex: lista `/`, `/listas`, `/feed`, `/biblioteca` e as
  demais rotas anteriores; não registra `/buscar` nem `/lista`.
- Testes direcionados de componentes, busca existente e listas: **33 passaram**.
- Fixture browser local com backend fictício: **10/10 cenários** em 1440px e
  390px, sem erros JavaScript; navegação por teclado, foco na viewport, abertura
  de lista e operações de lista permaneceram na rota antiga.
- A fixture não alterou o servidor normal nem dados remotos. Não houve publicação
  Xano nem teste em ambiente remoto.

## Limites

Esta reversão restaura os pontos de entrada de navegação; não conclui o restante
da change UI/UX. As capacidades de busca paginada em perfis/listas e detalhes
endereçáveis deixam de ter uma página própria no produto. Seus contratos e
testes locais ainda existentes não são uma rota ativa nem evidência de aceite
remoto.
