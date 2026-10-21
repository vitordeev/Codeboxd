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
| Indicadores e atividade | `GET /admin/dashboard` | `page`, `per_page` (padrão 6, máximo 100) para atividade; pendências limitadas a 5 | `users_total`, `posts_total`, `media_total`, `reports_pending`, `recent_posts[]` |
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

Os contratos e arquivos Xano locais ficam em `xano/`. Em 19/10/2026, uma exportação
de esquema confirmou que a tabela `report` e os oito endpoints administrativos já
existem no workspace `147717` (Pedro's Workspace). O perfil do projeto se chama
literalmente `default`; selecione `-p default -w 147717` explicitamente, pois o perfil
padrão global pode apontar para outro workspace.

As leituras reais rejeitaram visitante (401) e membro (403). Isso não comprova os
fluxos autorizados: as duas contas de teste disponíveis são membros. O esquema
remoto já exige `account_status == "active"` para administradores, regra agora
preservada nos arquivos locais. Evidências e limites estão em
`openspec/changes/gerenciamento-website/validation/backend-review-2026-10-19.md`.

Uma prévia restrita a `GET /admin/dashboard` e `GET /admin/users` foi aprovada sem
operações destrutivas. Ela prepara paginação independente de atividade/reports no
dashboard e parâmetros opcionais explícitos na pesquisa de usuários. Não foi
publicada. A prévia do diretório inteiro inclui outras alterações e remoção de
campos da tabela `user`; não use esse delta amplo para publicar a administração.

## Publicação, concessão de acesso e rollback

1. Revise o diff dos arquivos `xano/` e o esquema remoto. Para as duas correções revisadas em 19/10/2026, use `xano workspace push -p default -d xano -w 147717 --dry-run --include 'api/codeboxd/admin_dashboard_GET.xs' --include 'api/codeboxd/admin_users_GET.xs'`.
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
