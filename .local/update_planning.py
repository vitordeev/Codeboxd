from pathlib import Path

root = Path('openspec/changes')
designs = {
'definir-fundacao-codeboxd': '''## Context

Veja proposal.md e specs para o escopo. Existe um login em Reflex 0.9.11.post1 e um backend Xano com usuários, logs e catálogo administrativo legado (titulos). O produto é uma rede social cultural para filmes, séries, animes e livros.

## Goals / Non-Goals

**Goals:** implementar os fluxos especificados, preservar dados existentes e aplicar autorização no backend.

**Non-Goals:** recomendações por aprendizado de máquina, chat, notificações e infraestrutura de grande escala.

## Decisions

- Reflex implementa páginas, estado e serviços Python. O navegador nunca recebe credenciais dos provedores. Xano é responsável por autenticação, persistência e autorização.
- Páginas: descoberta, detalhes, cadastro/login, biblioteca, feed, comunidade, perfil e listas. Admin exige papel verificado por /auth/me; token presente não equivale a sessão válida.
- Adaptadores no servidor Python consultam TMDB (filmes/séries), Jikan (animes) e Open Library (livros). A camada isola normalização e falhas. Somente mídias utilizadas são persistidas no Xano. Esta decisão substitui o esboço que colocava todos os adaptadores no Xano.
- O grupo Codeboxd oferece endpoints tipados. Mutações exigem autenticação e autoria derivada de $auth.id. Perfis públicos nunca retornam e-mail ou senha.
- Sessões lembradas duram até 24 horas, igual ao token; sessões não lembradas usam SessionStorage. Revalidar perfil antes de ações protegidas; 401 encerra sessão, indisponibilidade recebe mensagem própria.
- Notas em passos de 0,5 entre 0,5 e 5; zero significa sem nota. Reviews e posts com spoilers são recolhidos por padrão.
- Feed contém posts de usuários seguidos; comunidade permite encontrar perfis. Interações aparecem na biblioteca e no perfil e podem ser compartilhadas como posts.
- Listas públicas são legíveis por todos; privadas somente pelo proprietário. Exclusões removem dependências em transação.
- Preservar titulos como catálogo legado, protegendo mutações por papel admin. media mantém a identidade externa do catálogo social.

## Risks / Trade-offs

- Falhas externas → avisos por fonte e acesso contínuo aos dados persistidos.
- Token no navegador → evitar HTML não confiável, limitar validade e validar no Xano.
- Alterações remotas da equipe → comparar exportação antes de publicar, sem apagar dados existentes.
- Testes locais não comprovam publicação → registrar separadamente a validação remota.

## Migration Plan

Exportar esquema remoto sem registros/segredos; adicionar tabelas e endpoints; corrigir logs e autorização; testar contratos e compilar Reflex; revisar dry-run antes de publicar; configurar XANO_SOCIAL_URL e TMDB_READ_TOKEN. Rollback restaura endpoints sem excluir dados criados.
''',
'criar-modelo-dados-xano': '''## Context

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
'''}
for change, body in designs.items():
    (root/change/'design.md').write_text(body, encoding='utf-8')
