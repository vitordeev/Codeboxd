# Modelo de dados pretendido

## Entidades principais

```text
user
  └── profile

user ──< user_media_interaction >── media
user ──< user_follow >── user
user ──< post >── media
user ──< post_like >── post
user ──< comment >── post
user ──< user_list ──< user_list_item >── media
```

## `user`

Responsável pela identidade e autenticação.

Campos esperados:

- `id`
- `username` obrigatório e único
- `email` obrigatório e único
- `password`
- `role`
- `created_at`

O campo `name` existente deverá ser analisado antes de ser substituído ou migrado.

## `profile`

Responsável pelas informações públicas:

- `id`
- `user_id`
- `display_name`
- `biography`
- `profile_image`
- `created_at`
- `updated_at`

Cada usuário deverá ter no máximo um perfil.

## `media`

Representação unificada para filmes, séries, animes e livros.

Campos esperados:

- `id`
- `media_type`: `movie`, `series`, `anime` ou `book`
- `title`
- `description`
- `cover_image` ou `poster_image`
- `external_source`
- `external_id`
- `created_at`
- `updated_at`

Regra de integridade:

```text
UNIQUE(external_source, external_id)
```

Informações específicas de cada tipo devem ser armazenadas apenas quando necessário, sem quebrar a representação comum.

## `user_media_interaction`

Relaciona um usuário a uma mídia.

Campos esperados:

- `id`
- `user_id`
- `media_id`
- `status`: `planned`, `in_progress`, `completed` ou `dropped`
- `rating`
- `review`
- `created_at`
- `updated_at`

Regra de integridade:

```text
UNIQUE(user_id, media_id)
```

Cada usuário deverá ter uma interação ativa por mídia, atualizando o registro existente quando alterar status, nota ou review.

## `user_follow`

Representa uma relação direcionada entre usuários.

Campos esperados:

- `id`
- `follower_user_id`
- `followed_user_id`
- `created_at`

Regras:

```text
UNIQUE(follower_user_id, followed_user_id)
follower_user_id != followed_user_id
```

## `post`

Publicação social.

Campos esperados:

- `id`
- `author_user_id`
- `media_id` opcional
- `content`
- `created_at`
- `updated_at`

O post poderá referenciar uma mídia, mas essa associação deverá ser opcional.

## `post_like`

Campos esperados:

- `id`
- `user_id`
- `post_id`
- `created_at`

Regra:

```text
UNIQUE(user_id, post_id)
```

## `comment`

Campos esperados:

- `id`
- `user_id`
- `post_id`
- `content`
- `created_at`
- `updated_at`

## `user_list`

Lista criada por um usuário.

Campos esperados:

- `id`
- `owner_user_id`
- `title`
- `description`
- `is_public`
- `created_at`
- `updated_at`

## `user_list_item`

Relaciona uma lista a uma mídia.

Campos esperados:

- `id`
- `list_id`
- `media_id`
- `position` opcional
- `created_at`

Regra:

```text
UNIQUE(list_id, media_id)
```

## Integridade e autorização

- Toda relação deverá apontar para registros válidos.
- Dados criados por usuários deverão preservar seu proprietário.
- Usuários só poderão alterar seus próprios perfis, interações, listas e conteúdo social.
- Exclusões deverão considerar registros dependentes.
- Endpoints autenticados deverão usar o usuário do token, não um `user_id` livremente informado pelo cliente.
