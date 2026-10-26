> Reconciliação documental em 26/10/2026: marcadores de merge removidos; IDs e evidências históricas preservados. Estado desta entrega: arquivada, 87 tarefas únicas concluídas. Textos datados abaixo descrevem suas respectivas rodadas.

## Context

O projeto tem páginas Reflex e estados sociais ligados ao grupo Xano Codeboxd. As imagens em `Imagens/` orientam descoberta, feed, perfil e listas; o pop-up de login foi desconsiderado. Revisão documental em 13/10/2026: provedores e layout refletem o código atual; evidências remotas são de setembro. Configuração é carregada do `.env`, mas a revisão encontrou o arquivo rastreado e `.gitignore` vazio. Segredos não devem chegar ao navegador nem aos artefatos.

## Goals / Non-Goals

### MoviePage visual reference

A referência `Imagens/Captura de tela 2026-09-18 154800.png` orienta hero, sinopse, metadados, status, nota/review, listas, críticas e relacionados. A estrutura responsiva é compartilhada pelos quatro tipos, mostrando somente campos disponíveis. TMDB, Kitsu e Open Library fornecem metadados e relacionados conforme suporte. Críticas podem estar vazias, especialmente em livros/animes; falhas opcionais não impedem a ficha principal. Streaming TMDB considera o Brasil quando disponível.


**Goals:** implementar os fluxos especificados, preservar dados existentes e aplicar autorização no backend.

**Non-Goals:** recomendações por aprendizado de máquina, chat, notificações e infraestrutura de grande escala.

## Decisions

- Quando a busca de um provedor falha, o Codeboxd preserva o aviso e pesquisa o catálogo já persistido no Xano por título e categoria. Isso mantém obras conhecidas acessíveis durante indisponibilidade externa sem apresentar registros locais como resultados recém-consultados no provedor.

- Reflex implementa páginas, estado e serviços Python. O navegador nunca recebe credenciais dos provedores. Xano é responsável por autenticação, persistência e autorização.
- Páginas: descoberta, detalhes, cadastro/login, biblioteca, feed, comunidade, perfil e listas. Admin exige papel verificado por /auth/me; token presente não equivale a sessão válida.
- Adaptadores no servidor Python consultam TMDB (filmes/séries), Kitsu (animes) e Open Library (livros). A camada isola normalização e falhas; somente mídias utilizadas são persistidas no Xano. Essa decisão substitui o esboço de adaptadores no Xano.
- TMDB usa token de leitura no servidor; Kitsu e Open Library são públicas. Kitsu substituiu consultas Jikan em 23/09/2026, com evidência de busca, ficha e navegador em `docs/KITSU.md`. IDs Jikan/MyAnimeList são resolvidos por mapeamento Kitsu, mantendo registros usados por listas/avaliações; nunca assumir igualdade numérica entre fontes.
- A home atual empilha coleções por tipo, com fileiras horizontais e controles próprios. A grade vertical de populares registrada em 22/09 foi substituída. Busca e navegação por categoria seguem independentes e paginadas, preservando consulta, identidades e falhas parciais.

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
- Credenciais e arquivos gerados rastreados → corrigir Git em trabalho próprio; não afirmar proteção existente apenas porque a documentação antiga a menciona.
- O endpoint remoto `/likes` retorna 404 neste workspace. A carga do feed não faz uma consulta de discussão por publicação; a compatibilidade usa `/posts/{id}/discussion` sob demanda para abrir ou alternar uma curtida. A publicação remota do endpoint local de likes segue pendente.

## Migration Plan

Exportar esquema remoto sem registros/segredos; adicionar tabelas e endpoints; corrigir logs e autorização; testar contratos e compilar Reflex; revisar dry-run antes de publicar; configurar XANO_SOCIAL_URL e TMDB_READ_TOKEN. Rollback restaura endpoints sem excluir dados criados.

- Regra de acesso: descoberta, busca, detalhes e trailers do catálogo são públicos. Visitantes guardam nota pessoal em LocalStorage, sem perfil nem envio ao Xano; publicar críticas/posts, seguir e salvar biblioteca/listas exige conta.

## Estado de encerramento

Escopo original concluído: 87 tarefas, contratos sincronizados antes de arquivar. Recuperação de senha, imagem de post, validação administrativa, persistência de uploads e hospedagem têm contexto/pendências próprios em `openspec/HISTORICO.md` e `openspec/PENDENCIAS.md`. A conclusão não equivale a nova execução de todos os fluxos remotos ou visuais.
