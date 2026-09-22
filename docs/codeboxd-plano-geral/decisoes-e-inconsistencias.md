# Decisões e inconsistências

## Inconsistências encontradas

### Streamlit versus Reflex

O OpenSpec define Streamlit com Python, mas o README menciona Reflex. A decisão deve ser registrada e aplicada aos documentos e à estrutura do projeto.

### `name` versus `username`

O requisito funcional exige username único, porém o Xano atual possui apenas `name` e índice único para `email`.

Decisão necessária:

- Adicionar `username` e manter `name` temporariamente; ou
- Migrar `name` para `username`; ou
- Definir `name` como nome de exibição e criar `username` separado.

Recomendação: criar `username` separado e reservar `name` ou `display_name` para apresentação.

### Perfil misturado com autenticação

O design recomenda separar credenciais de dados públicos, mas não existe tabela `profile`.

Recomendação: criar `profile` com relação um-para-um com `user`.

### Campos opcionais no usuário

O schema atual declara `email` e `password` como opcionais, embora sejam necessários para cadastro e login.

É necessário alinhar:

- validação do schema;
- validação dos endpoints;
- mensagens de erro;
- migração de dados existentes.

### Workspace local versus workspace conectado

O repositório contém `xano/workspace/pedros_workspace.xs`, enquanto o perfil ativo está associado a `Victor's Workspace`.

O arquivo de workspace é apenas metadado de exportação e não deve ser usado para presumir que os dois workspaces são o mesmo. Antes de qualquer push, deve-se confirmar explicitamente o workspace alvo.

### Quick Start versus domínio do produto

Os arquivos Xano atuais estão marcados como `xano:quick-start` e representam uma base genérica. Eles não constituem ainda o backend funcional do CodeBoxd.

## Decisões recomendadas

1. Escolher oficialmente Streamlit ou Reflex.
2. Adotar nomes em inglês para entidades e campos do Xano, mantendo a documentação funcional em português.
3. Criar `username` único e `profile` separado.
4. Usar uma tabela unificada `media`.
5. Aplicar restrições únicas no banco, além de validações nos endpoints.
6. Fazer o Xano atuar como camada única entre frontend e APIs externas.
7. Não enviar tokens ou credenciais ao Git.
8. Usar `--dry-run` antes de qualquer `xano workspace push`.

## Pendências de produto

- Definir escala da avaliação: por exemplo, 0,5 a 5 estrelas.
- Definir limite e formato de reviews e comentários.
- Definir visibilidade padrão de listas e perfis.
- Definir comportamento de exclusão de mídia referenciada por interações.
- Definir paginação do feed, busca e listas.
- Definir quais atividades aparecem no feed.
- Definir APIs externas para cada categoria.
- Definir política de cache e atualização de dados externos.
- Definir tratamento de indisponibilidade de uma fonte externa.
- Definir endpoint e estratégia de logout/invalidação de token.
