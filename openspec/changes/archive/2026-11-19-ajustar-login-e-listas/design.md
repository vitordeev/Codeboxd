## Context

O logo da página de login hoje é renderizado como conteúdo estático, enquanto a home pública está registrada em `/`. Na página de listas, um botão alterna usuários autenticados da coleção pessoal para descoberta pública; visitantes já carregam o modo público sem esse botão.

## Goals / Non-Goals

**Goals:** criar um link acessível entre a marca e a home e retirar apenas o controle de exploração pública da página autenticada de listas.

**Non-Goals:** mudar rotas, dados, API, exibição das listas pessoais ou a descoberta pública para visitantes.

## Decisions

- Envolver o conjunto ícone e nome da marca em um único link para `/`, com nome acessível explícito.
- Remover somente o botão “Explorar listas públicas”; manter “Minhas listas” e a renderização pública usada por visitantes.

## Risks / Trade-offs

- Usuários autenticados deixam de alternar para descoberta pública por esse botão; a página continua focada na coleção pessoal, conforme solicitado.

## Migration Plan

Sem migração de dados. Rollback: restaurar o botão de descoberta e retirar o link da marca.

## Ajuste visual complementar

Agrupar os controles “Minhas listas” e “Criar lista” na mesma linha flexível. A ação de criar permanece visível somente para a coleção pessoal autenticada; visitantes e o modo público não recebem esse controle.
