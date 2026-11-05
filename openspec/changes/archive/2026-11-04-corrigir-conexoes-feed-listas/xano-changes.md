# Aplicação MANUAL no Xano — contrato proposto, não publicado

Nenhum passo abaixo foi executado no workspace. Arquivos `xano/` são referência
histórica local; não foram alterados nem representam esta implantação. Aplicar
em branch de teste, validar e publicar backend ANTES de usar o Python novo.

## 0. Conferir e preparar

1. No grupo API **Codeboxd**, comparar schemas/stacks publicados com o mapa em
   investigation.md. Registrar status/corpos sanitizados para os alvos que falham
   e para uma conta sem posts. Não enviar tokens/logs privados ao repositório.
2. Exportar backup de `user`, `profile`, `user_follow`, `post`, `user_list`,
   `user_list_item`, `user_media_interaction`, endpoints e funções afetadas.
   Guardar export privado fora do Git. Ensaiar restauração em branch isolada.
3. Suspender temporariamente escritas de follow/listas durante limpeza e corte.
   Não apagar posts, avaliações, listas personalizadas ou seus itens.
4. Conferir se há fan-out/timeline no remoto. O repositório NÃO contém essas
   tabelas. Não inventar nomes nem fazer migração às cegas. O GET /feed abaixo
   deve passar a usar diretamente post/user_follow, sem depender desse mecanismo.
5. Preservar a chamada `Security/require_current_session` com allow_reset=false
   e validação de ator ativo em todas as rotas protegidas. Nunca aceitar user_id
   ator do cliente. Privacidade das listas públicas/privadas deve permanecer.

## 1. Follow: limpeza e índices

Tabela existente **user_follow**: id inteiro PK, created_at timestamp,
follower_id inteiro referência user.id, followed_id inteiro referência user.id,
identity_key texto. Conferir tipos reais e referências antes de limpar.

1. Query All Records sem paginação truncada, agrupar por (follower_id,followed_id).
   Separar referências órfãs e auto-seguimentos para revisão; não criar user fictício.
2. Em cada par válido duplicado, manter menor id, remover apenas duplicados desse
   par. Normalizar identity_key para `<follower_id>:<followed_id>` em todos os
   sobreviventes; antes, verificar se alguma chave aponta para par diferente e
   reconciliar o par real (não usar chave residual para trocar autoria).
3. Criar índice **B-tree UNIQUE composto (follower_id ASC, followed_id ASC)**.
   Manter PK, índices individuais e UNIQUE identity_key existente. Conferir zero
   pares duplicados/chaves inconsistentes antes de ativar escritas.

## 2. Stacks follow, na ordem

**PUT /follows/{user_id}**, auth user, input user_id integer positivo:

1. Validar sessão e ator ativo. Get Record user por input.user_id; 404 se ausente;
   400 se igual a auth.id. Usar IDs inteiros, não username/profile.id.
2. Em Database Transaction: Get Record `user`, field_name=id,
   field_value=auth.id, **Settings → Lock habilitado**, retorno actor_lock.
   PUT e DELETE devem adquirir esse mesmo lock primeiro. Depois Query All Records user_follow com
   follower_id=auth.id AND followed_id=input.user_id, return single.
3. Se existe: não Add Record; se identity_key diverge, Edit Record para a chave
   canônica após revisão/limpeza. Se não existe: Add Record com follower_id,
   followed_id e identity_key canônica.
4. Se duas requisições criarem juntas, UNIQUE impede duplicação. Na captura de
   violação de unicidade, **fora da transação abortada**, Query All pelo par:
   se existe, tratar como sucesso; se não existe, propagar erro (não esconder
   conflito de chave associado a outro par). Nunca transformar todo erro em 200.
5. Retornar HTTP 200 JSON `{ "follower_id": <auth.id>, "followed_id": <target>,
   "following": true }` tanto para criado quanto já existente.

**DELETE /follows/{user_id}**, mesma auth/input:

1. Validar sessão/ator; rejeitar auto-seguimento e ID inválido.
2. Em Database Transaction adquirir o mesmo Get Record user com Lock da rota PUT,
   depois Query All Records pelo par e Delete Record de TODOS os resultados
   (defesa para residual legado), nenhum resultado também é sucesso.
3. Retornar 200 `{ "follower_id": <auth.id>, "followed_id": <target>,
   "following": false }`. DELETE de alvo ausente pode retornar o mesmo estado.
4. Manter GET /profiles/{user_id} com following do ator, inclusive array vazio;
   para conta válida sem profile, criar/reparar profile no fluxo administrativo
   após verificar ownership, em vez de mascarar 404 com conexão inventada.

## 3. Feed direto

**GET /feed**, auth user; page int default 1 min 1, per_page int default 20
min 1 max 100. Stack:

1. Validar sessão/ator ativo.
2. Query All Records em **post**, join **user_follow**:
   `post.user_id = user_follow.followed_id`; filtro
   `user_follow.follower_id = auth.id`. NÃO juntar post do próprio leitor,
   user_media_interaction ou timeline como requisito para produzir resultado.
3. Ordenar **post.id DESC** (estável), paginar page/per_page. Retornar lista de
   posts, ou objeto `{items:[...],...}`. Sem posts → HTTP 200 `[]`; nunca 404.
   Índice único do par evita multiplicar posts pelo join. Índices B-tree:
   user_follow(follower_id,followed_id) coberto pelo UNIQUE composto;
   **post(user_id ASC,id DESC)** para consulta dos seguidos. Manter PK post.id.
4. Campos dos posts: id,user_id,media_id nullable,body,created_at timestamp
   em milissegundos,image (objeto com url ou URL),spoiler; likes_count e
   comments_count opcionais. Add-ons, se usados, devem ser opcionais e não
   excluir posts com media_id nulo, zero likes/comentários ou leitor sem posts.
5. Não é necessário backfill ao seguir nem limpeza de timeline ao deixar de
   seguir nessa consulta direta: todos os posts existentes passam a ser elegíveis
   pelo par atual. Desativar dependência de fan-out para este endpoint; conservar
   dados antigos até confirmar que nenhum consumidor externo precisa deles.
6. GET /posts?user_id=auth.id deve devolver 200 [] se leitor nunca publicou;
   validar filtro/ordenação/paginação. GET /media e /profiles sem resultados
   também devolvem listas vazias. Erros reais precisam retornar HTTP de erro.

## 4. Status único de lista: schema e migração

Criar tabela **user_media_list_status**, auth=false, campos:

| Campo | Tipo/regra |
| --- | --- |
| id | integer, PK gerada |
| created_at | timestamp, default now |
| updated_at | timestamp, default now |
| user_id | integer obrigatório, referência user.id |
| media_id | integer obrigatório, referência media.id |
| status | enum obrigatório: watched, want_to_watch |

Índices: PK(id); **B-tree UNIQUE (user_id ASC,media_id ASC)**;
**B-tree (user_id ASC,status ASC,id ASC)** para projeção das listas. Ausência de
registro representa nenhum; não usar status vazio no banco. Usar media.id interno,
equivalente ao movie_id pedido, abrangendo as mídias já suportadas.

Migração com escritas suspensas:

1. Query All user_list, user_list_item e nova tabela (todas as páginas).
   Somente default_key exatamente `<owner>:planned` ou `<owner>:completed`
   identifica padrão. Conferir user_list.user_id=owner; conflito interrompe corte.
   Não inferir tipo pelo título. Legados sem chave: revisar e atribuir a chave
   manualmente se confirmados como padrão, antes de migrar seus itens.
2. Agrupar itens padrão por (user_list.user_id,user_list_item.media_id), validando
   user/media existentes. Para cada grupo: se houver completed, status=watched;
   senão planned→want_to_watch. Duplicatas da mesma lista também viram um registro.
   Gerar relatório privado com contagens antes/depois e conflitos resolvidos.
3. Add/Edit na tabela nova pelo par. Para repetição antes do corte, aplicar sempre
   a mesma regra, incluindo watched se a tabela nova já tiver watched. Conferir
   para cada par migrado o resultado esperado e exclusividade.
4. Depois de validar backup/migração e preparar TODAS as rotas abaixo, Delete
   Record dos itens **somente das listas padrão migradas** em user_list_item.
   Conservar user_list (título, descrição, is_public e default_key) e todas as
   personalizadas. A migração não altera user_media_interaction, incluindo nota/review.
5. Publicar roteamento novo e liberar escritas junto com o corte. Nunca deixar
   versões antigas gravarem user_list_item padrão em paralelo à nova fonte.

## 5. Função de escrita única e endpoints de status

Criar função **Lists/set_media_list_status**, parâmetros server-only:
user_id int, media_id int, status enum nullable, expected_status enum nullable
opcional e conditional_delete bool default false. Não expor user_id como input API.

Stack em ordem:

1. Get Record user/media, validar existência/ator ativo. Validar status null ou
   enum. Nunca receber rating/review/spoiler neste contrato de organização.
2. Adicionar **Database Transaction**; dentro dela, primeiro **Get Record** da
   tabela `user`, field_name=`id`, field_value=parâmetro `user_id`, output `id`,
   Return As `actor_lock`. Na aba **Settings**, habilitar **Lock**. Só então
   executar os passos 3–5 dentro da mesma transação. Todos os escritores das
   listas padrão, inclusive DELETE de lista, devem adquirir esse mesmo lock
   antes de consultar status. Não bloquear apenas a relação, pois ela pode não
   existir. Não chamar a função em background nem soltar o lock antes das escritas.
   Essa configuração é documentada em Get Record; se não estiver disponível
   no editor do workspace, interromper o corte e conferir a versão/permissões.
3. Query All user_media_list_status pelo par, single. Se conditional_delete=true
   e registro ausente ou status diferente de expected_status: não remover.
4. Se status=null: Delete Record existente; ausência é sucesso.
   Se status não nulo e existe: Edit Record status e updated_at (não alternar).
   Se não existe: Add Record com par/status e timestamps. Índice único cobre
   qualquer escritor que tente bypass; tratar conflito só após rollback/reconsulta.
5. Ainda na mesma transação, quando status não nulo e a operação não foi um
   conditional_delete ignorado: Query All `user_media_interaction` WHERE
   user_id=ator AND media_id=mídia, single. Se existe, **Edit Record somente
   status e updated_at**, com watched→completed, want_to_watch→planned;
   preservar rating, review, spoiler e identidade. Se não existe: Add Record
   user_id,media_id,identity_key=`<user_id>:<media_id>`, status mapeado, rating=0,
   review="",spoiler=false e timestamps now. Isso preserva o efeito de organização
   da biblioteca do atalho antigo sem sobrescrever avaliações. Status null não
   remove nem altera a interação. Qualquer erro de banco aborta ambas as mudanças.
6. Retornar `{user_id,media_id,status}` do registro persistido, ou status null
   quando ausente. Não responder sucesso antes do commit.

**GET /media-list-status/{media_id}** (novo), auth user, media_id inteiro positivo:
sessão/ator → Get media (404 se inexistente) → Query All pelo par auth.id/media_id
single → 200 `{user_id:<auth.id>,media_id:<input>,status:<enum ou null>}`.

**PUT /media-list-status/{media_id}** (novo), mesma auth/path, JSON
`{"status":"watched"}` / `{"status":"want_to_watch"}` / `{"status":null}`.
Exigir campo status presente (ausência não significa apagar), invalid enum→400.
Sessão/ator → função com auth.id/media_id/status → devolver objeto confirmado.
Repetir PUT idêntico mantém estado. O toggle é decisão do cliente após GET.
Nenhuma avaliação é apagada. Nenhum add-on é obrigatório nesses endpoints.

## 6. TODAS as entradas das listas padrão

Preservar autorizações originais antes de executar os desvios abaixo. Identificar
tipo por default_key correspondente ao owner, nunca por título. planned mapeia
want_to_watch, completed mapeia watched. Chave não nula inválida → erro/revisão.

- **GET /lists/{id}/items** e **GET /lists/public/{id}/items**: Get user_list,
  validar propriedade/privacidade como hoje. Padrão → Query All
  user_media_list_status WHERE user_id=list.user_id AND status=tipo; sort id ASC,
  paginação original; mapear para `{id:<status.id>,list_id:<list.id>,media_id,
  created_at}`. Personalizada → user_list_item como hoje. Não alterar lista privada
  para pública nem autorizar o GET público de lista privada.
- **POST /lists/{id}/items**, input media_id: validar sessão, owner e media;
  padrão → função set_media_list_status(auth.id,media_id,tipo), retornar objeto
  de item compatível `{id,list_id,media_id,created_at}` após commit. Adição ao
  mesmo tipo mantém estado, não é toggle. Personalizada → lógica atual.
- **DELETE /lists/{id}/items/{media_id}**: validar owner; padrão → função com
  status=null, conditional_delete=true, expected_status=tipo. Não apagar watched
  porque chegou tarde DELETE de want_to_watch. Retornar `{success:true}`.
  Personalizada → lógica atual.
- **DELETE /lists/{id}**: validar owner, transação/bloqueio de user como acima,
  remover statuses do owner que correspondem ao tipo da lista; apagar metadado
  da lista. Nunca remover o outro tipo ou avaliações. Personalizadas mantêm a
  limpeza original de seus user_list_item. Preparação padrão poderá recriar
  metadado vazio, como já acontece.
- **POST /lists** e função existente de preparação padrão: manter default_key
  único por owner/tipo e metadados existentes. Não copiar itens legados após corte.
- **PUT /lists/{id}**: manter default_key imutável; personalização de título/
  descrição/visibilidade não muda tipo nem ownership nem remove status.
- Revisar qualquer função/add-on/endpoint de perfil/admin que enumere itens
  padrão diretamente: delegar à mesma projeção, sem misturar personalizadas.
  Não mudar contratos /interactions GET/PUT nem filtros de biblioteca nesta entrega;
  somente a função de organização atualiza o status de consumo preservando avaliação.

## 7. Verificação manual obrigatória e rollback

1. Follow: alvo válido com/sem follow legado, PUT repetido/paralelo, DELETE
   repetido, seguir novamente; um só par. Inválido/self/visitante rejeitados.
2. Conta nova sem posts: seguir autor com posts históricos → GET /feed inclui
   posts sem publicar nada. Parar de seguir remove conteúdo desse autor. Vazio
   legítimo 200 []; erro 5xx não vira []. Conferir primeira/segunda página.
3. Listas: GET status ausente; PUT want_to_watch; PUT watched; repetir watched;
   PUT null. Em cada passo confirmar dois GETs de itens, controles e recarga.
   Testar também busca dentro da lista, picker da ficha, exclusão de item/lista,
   renomear padrão, lista privada e personalizada homônima, duas contas.
4. Disparar PUTs opostos e DELETE condicional concorrentes; deve sobrar no máximo
   um status e projeções coerentes. Testar >100 itens, falha/timeout pós-commit,
   avaliações preservadas e ausência de novos itens padrão em user_list_item.
5. Registrar evidência sanitizada e só então concluir task 3.2. Não foi executada
   pelo agente. Se falhar, manter escritas bloqueadas e restaurar backup/stacks
   junto com reversão do Python; não executar limpeza irreversível sem backup.

Dependências: idempotência/deduplicação e feed remoto dependem de 1–3;
switch Python e todas as listas padrão dependem de 4–6 completos. O novo Python
exibe falha explícita se o endpoint novo não estiver disponível. Não há alegação
de migração, índice, stack, add-on ou publicação realizados.

## Referências oficiais consultadas

- [Get Record e configuração Lock](https://docs.xano.com/the-function-stack/functions/database-requests/get-record)
  documenta bloqueio dentro de Database Transaction.
- [Database Transaction](https://docs.xano.com/the-function-stack/functions/database-requests/database-transaction)
  documenta agrupamento de operações de banco e que falhas de passos que não
  são de banco não garantem rollback. Validar entradas/precondições antes de
  iniciar gravações; não engolir erros de banco dentro da transação.
