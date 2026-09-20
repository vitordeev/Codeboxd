## Context

O projeto já tem as páginas Reflex e os estados sociais ligados ao grupo Xano Codeboxd. As imagens atualizadas em `Imagens/` orientam descoberta, feed, perfil e listas; o pop-up de login das referências foi desconsiderado. O ambiente local tem as URLs Xano e o token TMDB no `.env` ignorado; segredos nunca devem chegar ao navegador.

## Goals / Non-Goals

### MoviePage visual reference

The reference `Imagens/Captura de tela 2026-09-18 154800.png` defines the media detail layout: hero, synopsis, provider metadata, library status, rating/review, list shortcuts, public reviews, and recommendations. Use the same responsive structure for movies, series, anime, and books, showing only fields provided by each source. Recommendations use TMDB, Jikan, or Open Library subject search when available. Public reviews come from TMDB for movies/series and Jikan for anime; books show an empty state because Open Library does not provide textual user reviews. Optional review/recommendation failures must not prevent the main media details from loading.

**Goals:** implementar os fluxos especificados, preservar dados existentes e aplicar autorização no backend.

**Non-Goals:** recomendações por aprendizado de máquina, chat, notificações e infraestrutura de grande escala.

## Decisions

- Quando a busca de um provedor falha, o Codeboxd preserva o aviso e pesquisa o catálogo já persistido no Xano por título e categoria. Isso mantém obras conhecidas acessíveis durante indisponibilidade externa sem apresentar registros locais como resultados recém-consultados no provedor.

- Reflex implementa páginas, estado e serviços Python. O navegador nunca recebe credenciais dos provedores. Xano é responsável por autenticação, persistência e autorização.
- Páginas: descoberta, detalhes, cadastro/login, biblioteca, feed, comunidade, perfil e listas. Admin exige papel verificado por /auth/me; token presente não equivale a sessão válida.
- Adaptadores no servidor Python consultam TMDB (filmes/séries), Jikan (animes) e Open Library (livros). A camada isola normalização e falhas. Somente mídias utilizadas são persistidas no Xano. Esta decisão substitui o esboço que colocava todos os adaptadores no Xano.
- TMDB usa o token de leitura no servidor. Jikan e Open Library são serviços públicos e não requerem chave. Busca e detalhe real foram confirmados para TMDB; a chamada mais recente ao Jikan falhou temporariamente, sem indicar falta de credencial.
- O grupo Codeboxd oferece endpoints tipados. Mutações exigem autenticação e autoria derivada de $auth.id. Perfis públicos nunca retornam e-mail ou senha.
- Sessões lembradas duram até 24 horas, igual ao token; sessões não lembradas usam SessionStorage. Revalidar perfil antes de ações protegidas; 401 encerra sessão, indisponibilidade recebe mensagem própria.
- Notas em passos de 0,5 entre 0,5 e 5; zero significa sem nota. Reviews e posts com spoilers são recolhidos por padrão.
- Feed contém posts de usuários seguidos; comunidade permite encontrar perfis. Interações aparecem na biblioteca e no perfil e podem ser compartilhadas como posts.
- Listas públicas são legíveis por todos; privadas somente pelo proprietário. Exclusões removem dependências em transação.
- Preservar titulos como catálogo legado, protegendo mutações por papel admin. media mantém a identidade externa do catálogo social.
- Esta etapa continua o desenvolvimento e a validação local. Hospedagem e domínio ficam fora do escopo atual; nenhuma publicação está autorizada ou implícita.

## Risks / Trade-offs

- Falhas externas → avisos por fonte e acesso contínuo aos dados persistidos.
- Token no navegador → evitar HTML não confiável, limitar validade e validar no Xano.
- Alterações remotas da equipe → comparar exportação antes de publicar, sem apagar dados existentes.
- Testes locais não comprovam publicação → registrar separadamente a validação remota.
- O endpoint remoto `/likes` retorna 404 neste workspace. A carga do feed não faz uma consulta de discussão por publicação; a compatibilidade usa `/posts/{id}/discussion` sob demanda para abrir ou alternar uma curtida. A publicação remota do endpoint local de likes segue pendente.

## Migration Plan

Exportar esquema remoto sem registros/segredos; adicionar tabelas e endpoints; corrigir logs e autorização; testar contratos e compilar Reflex; revisar dry-run antes de publicar; configurar XANO_SOCIAL_URL e TMDB_READ_TOKEN. Rollback restaura endpoints sem excluir dados criados.

- Regra de acesso: descoberta, busca, detalhes e trailers do catálogo são públicos. Visitantes guardam nota pessoal em LocalStorage, sem perfil nem envio ao Xano; publicar críticas/posts, seguir e salvar biblioteca/listas exige conta.
