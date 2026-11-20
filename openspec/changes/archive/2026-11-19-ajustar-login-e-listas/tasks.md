## 1. Navegação do login e listas

- [x] 1.1 Tornar o logo e nome Codeboxd da tela de login um link acessível para `/`; verificar rota e nome acessível.
- [x] 1.2 Remover somente o botão “Explorar listas públicas”; verificar que “Minhas listas” e a renderização pública para visitantes continuam presentes.
## 2. Validar e registrar

- [x] 2.1 Conferir no código que a marca aponta para `/`, que o controle de listas públicas foi removido e que visitantes continuam vendo listas públicas; executar `reflex compile --dry`, `git diff --check` e `openspec validate ajustar-login-e-listas --type change`.

## Evidências locais (2026-11-18)

- A marca na tela de login é um link acessível para `/`.
- O botão “Explorar listas públicas” foi removido; “Minhas listas” permanece e o ramo de exibição de listas públicas para visitantes foi preservado.
- Reflex compilou com sucesso; change OpenSpec válida; `git diff --check` passou com avisos apenas de normalização LF/CRLF.
- Não foram executados testes automatizados nesta alteração.

## Complemento visual (2026-11-19)

- [x] 1.3 Agrupar “Minhas listas” e “Criar lista” na mesma linha responsiva e manter “Criar lista” restrito à coleção pessoal.
- [x] 2.2 Conferir a composição no código, executar `reflex compile --dry`, `git diff --check` e `openspec validate ajustar-login-e-listas --type change`.
