## Why

O card da obra associada aparece atualmente separado do cabeçalho do post. O
usuário pediu que ele fique ao lado da identificação do autor para deixar a
publicação mais coesa e fácil de reconhecer.

## What Changes

- Posicionar o card compacto da obra na mesma faixa visual do avatar e do nome do autor.
- Manter a foto pessoal como conteúdo principal abaixo do cabeçalho.
- Preservar link, título, miniatura e fallback do card, com quebra responsiva em telas estreitas.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `social-feed`: quando houver obra associada, exibir seu card compacto junto à identificação do autor no cabeçalho do post.

## Impact

Afeta somente a composição do post em `Codeboxd_main/pages/social.py` e este
planejamento OpenSpec. Não altera dados, APIs, autenticação ou upload de imagens.
