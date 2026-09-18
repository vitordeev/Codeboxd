## Context

Veja proposal.md e specs. Reflex é a aplicação Python e Xano é a fonte de verdade. O workspace já contém user, event_log e titulos, que devem ser preservados.

## Goals / Non-Goals

**Goals:** persistência relacional, identidade externa estável, autorização e unicidade sob concorrência.

**Non-Goals:** copiar todo o catálogo externo ou migrar destrutivamente tabelas existentes.

## Decisions

| Tabela | Relações e restrições |
|---|---|
| user | Autenticação existente, email único, username normalizado para novos cadastros; preservar campos/papéis existentes. |
| profile | user_id e username únicos; display_name, bio, avatar_url públicos. |
| media | identity_key único (fonte + categoria + ID externo), title, media_type, description, cover_url, year, details. |
| user_media_interaction | user_id + media_id únicos; status planned/in_progress/completed/dropped, rating, review, spoiler. |
| user_follow | follower_id + followed_id únicos; sem auto-seguimento. |
| post | user_id, media_id opcional, body, spoiler e datas. |
| post_like | user_id + post_id únicos. |
| comment | user_id, post_id, body e datas. |
| user_list | user_id, title, description, is_public. |
| user_list_item | list_id + media_id únicos. |

Chaves compostas determinísticas permitem operações idempotentes e índices únicos. Autoria vem de $auth.id. Endpoints verificam existência das referências e propriedade antes de modificar dados. Índices adicionais cobrem usuário, mídia, post, lista e seguidores.

Cadastro cria usuário e perfil em transação. Contas antigas podem completar perfil após login. Alterar username atualiza user e profile em transação, verificando colisões. A exclusão de posts e listas remove dependências em transação. Não há exclusão pública de mídias referenciadas.

Listas privadas são filtradas no backend; seus itens herdam a mesma visibilidade. Logs recebem apenas metadados permitidos, nunca objetos completos de usuário.

## Risks / Trade-offs

- Usernames legados duplicados → preservar esquema legado; unicidade de novos nomes via profile e validação de user.
- Categorias legadas incluem games → preservar titulos sem conversões implícitas.
- Corridas de inserção → índices únicos, além das verificações da API.
- Relações Xano não substituem validação → verificar existência explicitamente.

## Migration Plan

Exportar o workspace, adicionar estruturas sem truncar tabelas, validar dry-run, publicar em transação e testar com dois usuários. Tarefas remotas só são concluídas após execução comprovada. Rollback restaura endpoints sem remover dados.
