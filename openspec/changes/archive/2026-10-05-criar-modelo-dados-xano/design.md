## Context

Revisão de encerramento: 13/10/2026. O modelo inicial está concluído (37/37); a descrição de publicação abaixo se refere às evidências de setembro. Campos e APIs administrativos posteriores pertencem a `gerenciamento-website`, não à migração inicial.

Reflex é a aplicação Python e Xano é a fonte de verdade. A migração inicial foi publicada no workspace 147717 e validada com duas contas de teste. As tabelas existentes `user`, `event_log` e `titulos` foram preservadas. No workspace remoto, `/likes` retorna HTTP 404 apesar do endpoint existir localmente; o feed usa a rota de discussão como compatibilidade.

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

Exportar o workspace, adicionar estruturas sem truncar tabelas, validar dry-run e testar com dois usuários. A migração inicial e a paginação foram publicadas; os principais relacionamentos foram exercitados com operações reais. Resultados e credenciais de teste ficam em `.local/`. Rollback restaura endpoints sem remover dados.

## Compatibilidade e continuidade

`identity_key` considera fonte, categoria e identificador externo, evitando colisão de IDs TMDB entre filmes e séries. Desde 23/09, Kitsu é a fonte atual de anime; o mapeamento MyAnimeList/Kitsu reaproveita registros Jikan existentes e suas relações. O catálogo legado `titulos` permanece separado.

Banner de perfil e imagem de post são complementos posteriores descritos no histórico central. `report` e auditoria administrativa são tratados pela change ativa. Não inferir publicação administrativa a partir da migração social concluída.

A revisão encontrou `.gitignore` vazio e arquivos privados/gerados rastreados. A localização `.local/` não garante proteção Git; essa correção operacional está em `openspec/PENDENCIAS.md`.
