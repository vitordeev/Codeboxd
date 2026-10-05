# Operações administrativas

Este mapa descreve os modelos e contratos para a mudança `gerenciamento-website`.
Os endpoints administrativos ficam no grupo Xano `Codeboxd`, exigem `auth = "user"`
e validam em cada chamada que o usuário obtido por `$auth.id` está ativo e possui
papel `admin`.

## Modelos existentes

| Domínio | Fonte | Campos usados pela administração | Observações |
| --- | --- | --- | --- |
| Contas | `user` | `id`, `name`, `username`, `role`, `account_status`, `created_at` | `role`: `admin`, `moderator`, `member`; estado: `active`, `disabled`. Senha e reset token nunca fazem parte das respostas. |
| Perfil | `profile` | `user_id`, `username`, `display_name`, `bio`, `avatar_url`, `banner_url` | Relação única por usuário; edição de perfil continua no fluxo próprio. |
| Catálogo atual | `media` | `id`, `identity_key`, `external_source`, `external_id`, `media_type`, `title`, `description`, `cover_url`, `year`, `details` | Tipos persistidos: `movie`, `series`, `anime`, `book`. A identidade externa é imutável nas correções. |
| Catálogo legado | `titulos` | `id`, `nome`, `categoria`, `sinopse`, `ano`, `genero`, `status`, `capa` | É usado por telas legadas e inclui `game`; não deve ser misturado ao catálogo social `media`. |
| Publicações | `post` | `id`, `user_id`, `created_at` | O dashboard exibe atividade mínima; não carrega corpo nem imagem para essa lista. |
| Auditoria disponível | `event_log` | `user_id`, `action`, `metadata`, `created_at` | `user_id` guarda o ator autenticado; `metadata` contém somente IDs, transição, decisão e motivo necessário. |
| Denúncias | `report` | alvo, motivo, snapshot, denunciante, estado, revisor e decisão | Nova tabela local; mensagens podem ser analisadas pelo snapshot sem tabela de mensagens. |

## Operações e payloads

| Operação | Endpoint planejado | Entrada | Resposta mínima |
| --- | --- | --- | --- |
| Indicadores e atividade | `GET /admin/dashboard` | `page`/limite fixos no servidor | `users_total`, `posts_total`, `media_total`, `reports_pending`, `recent_posts[]` |
| Pesquisa de contas | `GET /admin/users` | `search`, `user_id?`, `account_status?`, `role?`, `page`, `per_page` | `{items: [{id, username, name, role, account_status, created_at}], total, page, next_page, per_page}` |
| Suspender/reativar | `PUT /admin/users/{id}/status` | `account_status`, `reason?` | `{success, user_id, previous_status, account_status}`; o ator vem da sessão, não do payload |
| Catálogo | `GET /admin/catalog` | tipo, consulta, filtros, `page`, `per_page` | `{items, total, page, next_page, per_page}` com campos permitidos da tabela `media` |
| Corrigir obra | `PUT /admin/catalog/{id}` | `title`, `description?`, `cover_url?`, `year?` | Registro atualizado sem alterar `id`, `identity_key`, fonte ou ID externo |
| Cadastrar obra | `POST /admin/catalog` | identidade externa, tipo, título e metadados opcionais | `{success, created, item}`; identidade existente devolve o registro atual em vez de duplicar |
| Fila de denúncias | `GET /admin/reports` | estado, tipo, motivo, `page`, `per_page` | Lista mínima com snapshot e dados da decisão; nunca inclui credenciais |
| Decisão de denúncia | `PUT /admin/reports/{id}` | estado final e decisão | estado anterior/novo e revisor autenticado registrados na auditoria |

Listas administrativas usam páginas com até 100 itens; a UI usa 25 por página.
Respostas de lista têm estado vazio explícito. Consultas de contagem são executadas
no servidor e não são calculadas a partir de páginas da UI.

## Acesso e privacidade

- Cada endpoint administrativo rejeita visitante, conta desativada e papel diferente de `admin` antes de consultar dados restritos.
- IDs de ator são sempre lidos de `$auth.id`. IDs de alvo podem vir da rota; identidade administrativa nunca vem do cliente.
- Listas de usuários não retornam e-mail, senha, hash, token de autenticação nem dados de recuperação.
- Snapshots guardam apenas o trecho do alvo necessário à decisão, sem tokens, dados de autenticação ou conteúdo não relacionado.
- Texto de snapshot, motivo e decisão é exibido como texto escapado; abrir uma denúncia não altera seu conteúdo alvo.
- Suspensão/reativação e decisões registram ator, horário, ação e estado anterior/novo; motivo é opcional e limitado.
- Campos de correção do catálogo são os metadados estáveis locais (`title`, `description`, `cover_url`, `year`). Referências externas e detalhes brutos do provedor permanecem intactos.

## Estado da integração

Os contratos e arquivos Xano locais ficam em `xano/`. Em 26/09/2026, o dry-run do
workspace `147717` reconheceu a tabela `report` e os endpoints do dashboard, usuários,
catálogo e moderação. O dry-run não publica alterações: as rotas administrativas só
ficam funcionais quando esses arquivos forem publicados no workspace conectado.

## Publicação, concessão de acesso e rollback

1. Revise o diff dos arquivos `xano/` e rode `xano workspace push -d xano -w 147717 --dry-run`.
2. Publique somente após revisão do delta no workspace Xano. Em seguida, rode a suíte
   `python -m unittest discover -s tests -q` e `reflex compile --dry`.
3. Conceda o papel `admin` manualmente no registro `user` aprovado, atualizando `role`
   para `admin` por meio do console seguro do Xano. Nunca exponha credenciais no cliente.
4. Para rollback, restaure no Xano os arquivos da revisão anterior para os endpoints e
   tabela afetados usando o histórico/revisões do workspace; rode o dry-run para revisar
   o delta inverso antes de publicar. Reverta também os arquivos locais correspondentes
   para manter o próximo dry-run alinhado ao estado remoto. A reversão do código do site
   não remove registros `report` já criados; preserve-os para auditoria.

Até que a publicação manual ocorra, alterações locais e resultados de dry-run não
representam validação de chamadas reais ao Xano.
