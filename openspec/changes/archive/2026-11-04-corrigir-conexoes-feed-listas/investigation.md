# Investigação anterior à implementação — 29/10/2026

Sem acesso ao workspace Xano, sem chamadas autenticadas nem reprodução remota.
Leitura de Python, testes, schemas/stacks Xano locais, specs e changes ativas.
`project.md` não existe. A auditoria documental CB-MT-004/005/006 é coerente
com os achados abaixo, mas não prova as causas dos incidentes remotos.

## Bug 1

Confirmado: `follow` decide por `following_ids`, compara uid sem normalização,
ignora resposta da mutação e altera a lista após qualquer HTTP 2xx, sem trava.
HTTPs de erro já viram APIError e notice; não é correto afirmar que todo erro
HTTP era ignorado. Corpo 2xx inválido/sem confirmação era aceito. Conversão de ID
inválido pode lançar ValueError sem mensagem. Cargas de perfil em voo podem
reaplicar conexões anteriores à mutação.
Xano local: upsert user_follow por identity_key e unicidade apenas nessa chave;
DELETE busca/remove só um registro. Isso não cobre pares legados com chave errada.
Conferir remotamente pares duplicados, chaves residuais, user/profile órfãos,
tipo de IDs, resposta/status por alvo e versão dos stacks publicados.

## Bug 2

Confirmado: `_refresh_posts` busca /feed, depois /posts próprios e /likes;
qualquer falha não-404 nessas leituras impede aplicar todos os posts. A tela
exibe o mesmo vazio após falha e após lista vazia. Criação de post invalida cache
e recarrega; isso pode explicar a recuperação observada, mas não está comprovado.
O stack feed local já faz join post.user_id=user_follow.followed_id, filtrando
follower_id=$auth.id; não usa primeiro post, timeline ou fan-out. Não inventar
uma tabela ausente. Conferir stack remoto, paginação, follows reais e logs de
/feed, /posts, /media, /profiles e /likes para conta sem posts.

## Bug 3

Confirmado: `quick_add` faz PUT /interactions e POST /lists/id/items separados,
nunca remove a lista oposta, ignora as respostas e não tem bloqueio. Os dois
botões em pages/social.py usam classe fixa, sem estado ativo. selected_status
é do editor de avaliação (começa planned mesmo sem relação), inadequado para
mostrar participação em listas. user_list_item permite a mesma mídia em listas
diferentes, correto para personalizadas e incorreto para as duas padrão.
Não há duas tabelas de filmes: há user_list + user_list_item, além de
user_media_interaction com avaliações. Migrar somente itens das duas listas
padrão para nova relação única; não eliminar reviews para representar nenhum.

## Mapa Python → Xano

Todas as rotas abaixo usam grupo social (XANO_SOCIAL_URL), Authorization Bearer
do servidor e JSON. Sem valores de configuração/credenciais neste documento.
`services/api.request`: timeout total 10s/conexão 3s, httpx.RequestError→APIError,
HTTP 400/401/403/404/409/422/429→mensagem PT, outros→indisponível; 204→None,
JSON inválido→APIError. GET/HEAD repetem 429 até três tentativas curtas;
mutações não são repetidas. `_call` invalida cache antes/depois de escrita,
verifica token antes/depois, pagina coleções de 100 e cacheia leituras por 15s.
`_require_user` valida sessão por GET /auth/me (grupo auth) antes de escrita;
401 limpa sessão, falha transitória mantém identidade/rascunho.

| Fluxo / função | Método e endpoint | Entrada | Resposta e erro |
| --- | --- | --- | --- |
| load_community, _profile_updates | GET /profiles | páginas | perfis por user_id; rows valida lista/items |
| conexões próprias e de perfil | GET /profiles/{user_id} | páginas | profile, followers, following, interactions; following_ids normalizados |
| follow | PUT /follows/{target} | ID no path, sem payload | antes ignorava registro; agora confirma par/estado |
| follow | DELETE /follows/{target} | ID no path | antes aceitava success; agora estado ou confirmação por perfil |
| load_feed / _refresh_posts | GET /feed | per_page=20 | posts dos seguidos; falha essencial→feed_error |
| _refresh_posts | GET /posts | user_id=ator, per_page=20 | próprios, unidos/deduplicados/ordenados; agora falha parcial visível |
| _refresh_posts | GET /likes | sem filtro | post_id curtidos; 404 legado tolerado, demais falhas não autorizativas agora aviso |
| _load_reference | GET /media, GET /profiles | paginação | catálogo/autores para cartões/editor; erro não autorizativo agora não impede posts |
| save_post / remove_post | POST /posts, PUT/DELETE /posts/{id} | body, media_id, spoiler; imagem multipart quando aplicável | invalida cache e chama _refresh_posts; mantido |
| _persist_selected / _load_external_interaction | GET /media?identity_key, GET /media/{id}, POST /media | external_source, external_id, media_type, title, description, cover_url, year, details | valida identidade antes de usar ID interno; mantido |
| _load_personal_interaction / save_interaction | GET/PUT /interactions | PUT: media_id,status,rating,review,spoiler | avaliação/biblioteca preservadas; quick_add deixa de sobrescrever avaliação |
| _ensure_default_lists | GET /lists; PUT /lists/{id}; POST /lists | reparo legado ou title,description,is_public,default_kind | prepara IDs/default_key; mantido, usado pela descoberta/listas |
| load_lists / open_list | GET /lists, /lists/public; GET /lists/{id}/items, /lists/public/{id}/items | paginação, list ID | metadados e itens; Xano deve projetar status nas padrão |
| add_list_result / add_current_media_to_list | POST /lists/{id}/items | media_id | personalizado mantido; padrão deve delegar ao status único no Xano |
| remove_list_item | DELETE /lists/{id}/items/{media_id} | IDs no path | personalizado mantido; padrão remove apenas se status atual corresponder |
| delete list | DELETE /lists/{id} | list ID | backend deve limpar status correspondente em padrão |
| **novo** _load_selected_list_status / quick_add | GET/PUT /media-list-status/{media_id} | PUT: status=watched, want_to_watch ou null | {user_id,media_id,status}; valida os IDs e enum antes de aplicar; falha visível sem escrita legada |

Mapeamento do novo status: completed→watched, planned→want_to_watch. A lista
inferior é carregada pelos endpoints existentes e passa a usar a mesma fonte
no Xano. O picker da ficha recarrega status confirmado após adicionar a padrão.

## O que só o usuário pode verificar no Xano

Schemas/índices e stacks publicados versus arquivos locais; duplicatas reais,
dados de perfil dos alvos, joins e filtros efetivos, limites de paginação,
addons, sessão, caches e eventuais tabelas de fan-out não presentes no repo.
Não declarar os incidentes remotos resolvidos antes dos ensaios de xano-changes.md.
