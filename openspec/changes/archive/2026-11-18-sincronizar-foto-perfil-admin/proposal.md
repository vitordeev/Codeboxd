## Why

A foto de perfil salva no site pode nao aparecer no cabecalho administrativo porque a identidade fica em cache durante a sessao. Ao reabrir o menu, o painel deve buscar a foto atual do mesmo perfil.

## What Changes

- Atualizar os dados do administrador sempre que o menu de identidade for aberto, mantendo validacao da sessao e fallback de avatar.
- Preservar a imagem mais recente do perfil entre o site e o painel administrativo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `admin-dashboard`: atualizar os dados da identidade ao abrir o menu do administrador.

## Impact

Afeta o estado Reflex do painel e o requisito existente de identidade administrativa. Nenhuma mudanca de contrato ou publicacao Xano e necessaria; o endpoint `/admin/me` ja retorna `avatar_url` do perfil atual.
