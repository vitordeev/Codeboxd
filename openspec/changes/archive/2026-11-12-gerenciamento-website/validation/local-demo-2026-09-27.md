# Validação da demonstração local

## Escopo

A rota `/admin/demo` apresenta uma massa de dados sintética e somente de leitura
para revisar os formatos esperados do painel sem alterar o workspace Xano.

## Massa exibida

- 25 usuários na primeira página, com papéis `admin`, `moderator` e `member`, estados `active` e `disabled` e campos seguros.
- 25 obras na primeira página, distribuídas entre `movie`, `series`, `book` e `anime`, preservando `identity_key` e a identidade externa.
- 8 reports com os estados `pending`, `reviewing`, `resolved` e `rejected`, tipos de alvo variados e snapshots contextuais, incluindo mensagens.
- Envelopes JSON demonstrativos para `dashboard`, `users`, `catalog` e `reports`, com `total`, `page`, `next_page` e `per_page`.

## Verificação

- URL local: `http://localhost:3002/admin/demo`
- Resposta observada: HTTP 200
- A rota não possui eventos de escrita nem chamadas ao Xano.
- `reflex compile --dry`: sucesso.
- `openspec validate gerenciamento-website`: sucesso.

Esta prévia não substitui a validação do painel com dados reais depois da publicação
dos endpoints no workspace Xano.
