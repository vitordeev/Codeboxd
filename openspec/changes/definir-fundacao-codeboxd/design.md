## Context

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
