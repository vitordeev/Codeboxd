## Why

A marca da tela de login deve levar de volta à página inicial, e a página de listas deve manter uma interface mais direta sem o botão para explorar listas públicas.

## What Changes

- Tornar clicável o conjunto do ícone e nome Codeboxd na tela de login, apontando para a página inicial `/`.
- Remover da página `/listas` o botão “Explorar listas públicas”, preservando o acesso às listas pessoais e a exibição pública para visitantes.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `user-authentication`: navegação da marca na tela de login para a página inicial.
- `user-lists`: remover o controle de descoberta pública da página de listas para usuários autenticados.

## Impact

Afeta os componentes Reflex das páginas de login e listas, testes de contrato de navegação e as specs principais de autenticação e listas. Não altera APIs, persistência ou autorização.

## Ajuste visual complementar

- Alinhar os controles “Minhas listas” e “Criar lista” lado a lado na coleção pessoal autenticada, usando uma linha flexível que possa quebrar em telas estreitas. “Criar lista” continua restrito ao escopo pessoal.
