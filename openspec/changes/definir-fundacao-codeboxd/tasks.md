## 1. Project Setup

- [x] 1.1 Create the initial Reflex project structure and verify the application starts successfully with the Reflex run command
- [x] 1.2 Define the frontend page and component structure and verify all main application sections can be accessed
- [x] 1.3 Configure the Xano backend workspace and verify authenticated requests can reach the backend
- [x] 1.4 Define environment configuration for external services and verify sensitive configuration is not hardcoded in the application

## 2. User Authentication

- [x] 2.1 Create the user data structure required for registration and verify a new user account can be stored
- [x] 2.2 Implement user registration and verify valid users can create accounts
- [x] 2.3 Validate required registration information and verify incomplete registrations are rejected
- [x] 2.4 Enforce unique usernames and verify duplicate usernames cannot be registered
- [x] 2.5 Enforce unique email addresses and verify duplicate email addresses cannot be registered
- [x] 2.6 Implement user login and verify valid credentials create an authenticated session
- [x] 2.7 Handle invalid authentication attempts and verify invalid credentials do not create a session
- [x] 2.8 Implement logout functionality and verify authenticated sessions are ended
- [x] 2.9 Protect authenticated functionality and verify unauthenticated users cannot modify personal or social data

## 3. User Profiles

- [x] 3.1 Create the user profile data structure and verify each registered user has an associated profile
- [x] 3.2 Implement public profile viewing and verify users can access public profile information
- [x] 3.3 Implement profile editing and verify users can update their own profile information
- [x] 3.4 Protect profile ownership and verify users cannot modify another user's profile
- [x] 3.5 Implement profile activity display and verify available user activities are displayed
- [x] 3.6 Implement profile statistics and verify summary information is calculated from Codeboxd data

## 4. Unified Media Catalog

- [x] 4.1 Create the unified media representation and verify it supports movies, series, anime and books
- [x] 4.2 Store media type information and verify every registered media item is associated with a supported type
- [x] 4.3 Store external media identity information and verify source and external identifiers are preserved
- [x] 4.4 Implement media detail display and verify available identifying information is shown
- [x] 4.5 Implement media-type-specific information handling and verify different media types can display their available specific data
- [x] 4.6 Adapt the media detail page to the MoviePage reference across movies, series, anime and books, displaying available provider metadata and related works

## 5. External Media Data Integration

- [x] 5.1 Select and configure supported external data sources and verify each supported media category can retrieve external information
- [ ] 5.2 Implement external media search integration and verify matching media data can be retrieved
- [x] 5.3 Implement external media detail retrieval and verify available information can be retrieved for a selected media item
- [x] 5.4 Normalize externally obtained media information and verify supported media sources can produce the unified media representation
- [x] 5.5 Prevent duplicate internally stored media references and verify the same source and external identifier are not stored twice
- [x] 5.6 Implement external source failure handling and verify unavailable sources do not corrupt existing Codeboxd data

## 6. Media Discovery

- [x] 6.1 Implement text-based media search and verify matching media results are displayed
- [x] 6.2 Implement mixed media search results and verify movies, series, anime and books can appear in results
- [x] 6.3 Display media type identification in search results and verify users can distinguish media categories
- [x] 6.4 Implement media type filters and verify filtering limits results to the selected category
- [x] 6.5 Implement media detail navigation from discovery results and verify selecting a result opens the correct media details
- [x] 6.6 Handle searches with no results and verify users receive a no-results response
- [x] 6.7 Handle unavailable external search data and verify users receive an appropriate failure message

## 7. Media Interactions

- [x] 7.1 Create the user-media interaction data structure and verify interactions are associated with both a user and a media item
- [x] 7.2 Implement Planned consumption status and verify users can add media to their planned list
- [x] 7.3 Implement In Progress consumption status and verify users can mark media as currently being consumed
- [x] 7.4 Implement Completed consumption status and verify users can mark media as completed
- [x] 7.5 Implement Dropped consumption status and verify users can mark media as dropped
- [x] 7.6 Implement consumption status updates and verify users can change their own media status
- [x] 7.7 Implement media ratings and verify a user can maintain only one active rating per media item
- [x] 7.8 Implement rating updates and verify updated ratings replace previous ratings
- [x] 7.9 Implement media reviews and verify users can create reviews associated with media
- [x] 7.10 Implement review editing and verify users can edit only their own reviews
- [x] 7.11 Protect interaction ownership and verify one user's interactions cannot modify another user's interactions
- [x] 7.12 Implement personal interaction display and verify users can view their recorded status, rating and review

## 8. Social Connections

- [x] 8.1 Create the user connection data structure and verify follower and followed user relationships can be stored
- [x] 8.2 Implement following users and verify authenticated users can follow another user
- [x] 8.3 Prevent duplicate follows and verify the same relationship cannot be created twice
- [x] 8.4 Prevent self-following and verify users cannot follow their own profile
- [x] 8.5 Implement unfollowing and verify existing follow relationships can be removed
- [x] 8.6 Implement followers display and verify profile followers can be viewed
- [x] 8.7 Implement following display and verify the users followed by a profile can be viewed

## 9. Social Feed

- [x] 9.1 Create the social post data structure and verify posts can be associated with users and media items
- [x] 9.2 Implement media-related post creation and verify authenticated users can publish valid posts
- [x] 9.3 Implement followed user activity retrieval and verify the feed displays available activity from followed users
- [x] 9.4 Implement post information display and verify authors and associated media are displayed
- [x] 9.5 Implement post likes and verify a user can have only one active like per post
- [x] 9.6 Implement like removal and verify users can remove their own likes
- [x] 9.7 Implement post comments and verify authenticated users can create comments
- [x] 9.8 Implement social content ownership checks and verify users cannot modify or remove content created by others
- [x] 9.9 Implement editing and removal of owned social content and verify users can manage their own posts and comments

## 10. User Lists

- [x] 10.1 Create the custom list data structure and verify each list is associated with its owner
- [x] 10.2 Implement custom list creation and verify a valid list requires a title
- [x] 10.3 Implement adding media to lists and verify supported media types can be added
- [x] 10.4 Prevent duplicate media entries and verify the same media cannot appear twice in one list
- [x] 10.5 Implement removing media from lists and verify existing entries can be removed
- [x] 10.6 Implement list editing and verify users can update their own list title and description
- [x] 10.7 Implement list deletion and verify a deleted list no longer contains accessible entries
- [x] 10.8 Protect list ownership and verify users cannot modify or delete lists created by other users

## 11. Integration and Validation

- [x] 11.1 Verify authentication and profile functionality work together through the complete registration, login and profile flow
- [x] 11.2 Verify media discovery and external data integration work together from search to media detail display
- [x] 11.3 Verify media interactions persist correctly across user sessions
- [x] 11.4 Verify social connections affect the content displayed in the social feed
- [x] 11.5 Verify posts can reference supported media types and associated media information remains accessible
- [x] 11.6 Verify user lists support media from all supported categories
- [ ] 11.7 Validate the completed OpenSpec change and verify all proposal artifacts remain valid

Evidence update 19/09/2026: task 11.6 passed against the published Xano API with movie, series, anime and book records in one temporary list; the list was removed after the check. A real Jikan anime record remains in the shared catalog. The UI now searches this cached catalog when an external provider fails, with a visible provider warning. Jikan's live anime search still returns HTTP 504, so task 5.2 and final task 11.7 remain open until the external search can be verified.

## Evidência e retomada

Estado em 19/09/2026. A aplicação Reflex tem páginas sociais ligadas ao Xano publicado no workspace 147717. Navegação autenticada, cadastro, sessão, logout e contas independentes foram verificadas em navegador e chamadas reais; os resultados de backend anteriores ficam em `.local/remote-results.json` e as contas de teste em `.local/` (ignorado pelo Git).

TMDB está configurado no `.env` local e busca, detalhes, populares e capas foram confirmados na API e no navegador. Jikan e Open Library são provedores públicos, sem chave adicional. Open Library respondeu antes; a consulta ao Jikan nesta retomada falhou temporariamente, então a validação completa de todos os provedores ainda está aberta. O workspace Xano retorna 404 em `/likes`; a carga do feed não faz consultas por publicação e busca o estado de curtida sob demanda ao abrir uma discussão ou alternar a curtida.

Referências visuais atualizadas orientam descoberta, feed, perfil e listas; o pop-up de login foi explicitamente desconsiderado. Continue a implementação local. Configuração de domínio e hospedagem fica fora da etapa atual. Não arquive a change enquanto houver tarefas abertas. Histórico e instruções operacionais: `docs/RETOMADA.md`.

## 12. Acesso público e visitantes
- [x] 12.1 Permitir descoberta, busca e detalhes de obras sem autenticação
- [x] 12.2 Mostrar trailers disponíveis sem exigir conta
- [x] 12.3 Permitir nota pessoal local a visitantes, mantendo crítica escrita, posts, follows e biblioteca sob conta

Evidência 19/09/2026: visitante usa armazenamento local por identidade da obra; trailers aceitam apenas chaves YouTube de vídeos TMDB classificados como trailer/teaser. O smoke público e autenticado foi confirmado no navegador; ver a evidência da tarefa 12.4.
- [x] 12.4 Confirm public navigation, guest rating, trailers and authenticated-only mutations in the running browser
- [x] 12.5 Reduzir latência da descoberta e das fichas, limitar carga inicial, paralelizar leituras independentes e manter compatibilidade de curtidas sob demanda
Evidência 19/09/2026: 48 testes unitários passaram. Smoke no Edge da instância atualizada confirmou home responsiva, busca/detalhe públicos, login, biblioteca, feed, comunidade, listas, logout e bloqueio da biblioteca após sair, sem erros JavaScript. Quando `/likes` retorna 404, a carga do feed não consulta discussões por publicação. A sequência de sondagens consecutivas atingiu HTTP 429 no Xano; a aplicação mostrou aviso recuperável e preservou a sessão.
Estado da change após debug: 85/87 tarefas. Permanecem busca Jikan ao vivo e validação final.
- [x] 12.6 Manter o conteúdo visível e navegável enquanto as ações assíncronas estão carregando
