## 1. Preparação do modelo de dados

- [x] 1.1 Revisar as specs de persistência e verificar que todas as capabilities possuem requisitos definidos
- [x] 1.2 Confirmar a estrutura das entidades e relacionamentos definidos no design.md
- [x] 1.3 Preparar o workspace do Xano e verificar que o banco de dados está disponível para criação das tabelas

## 2. Usuários e perfis

- [x] 2.1 Criar a tabela de usuários e verificar que cada registro possui uma identidade única
- [x] 2.2 Configurar os campos únicos necessários para identificação do usuário e verificar que registros duplicados são rejeitados
- [x] 2.3 Criar a tabela de perfis e verificar que um perfil pode ser associado a um usuário
- [x] 2.4 Configurar a relação entre usuário e perfil e verificar que os dados permanecem associados corretamente

## 3. Catálogo de mídias

- [x] 3.1 Criar a tabela media e verificar que ela suporta filmes, séries, animes e livros
- [x] 3.2 Adicionar os campos de identificação e verificar que cada mídia possui uma identidade interna
- [x] 3.3 Adicionar o tipo da mídia e verificar que o registro identifica corretamente sua categoria
- [x] 3.4 Adicionar os identificadores external_source e external_id e verificar que mídias externas podem ser identificadas
- [x] 3.5 Configurar a prevenção de duplicação por fonte e identificador externo e verificar que registros duplicados não são criados

## 4. Interações entre usuários e mídias

- [x] 4.1 Criar a tabela user_media_interaction e verificar que uma interação pode ser associada a um usuário e uma mídia
- [x] 4.2 Adicionar o campo de status e verificar que o estado da interação pode ser persistido
- [x] 4.3 Adicionar o campo de avaliação e verificar que uma avaliação válida pode ser armazenada
- [x] 4.4 Adicionar o campo de review e verificar que uma avaliação textual pode ser associada à interação
- [x] 4.5 Validar que diferentes usuários podem possuir interações independentes com a mesma mídia

## 5. Relações sociais

- [x] 5.1 Criar a tabela user_follow e verificar que um usuário pode seguir outro usuário
- [x] 5.2 Configurar a direção da relação entre follower_user e followed_user e verificar que os papéis permanecem distintos
- [x] 5.3 Configurar a prevenção de relações de seguimento duplicadas e verificar que a mesma relação não pode ser persistida duas vezes

## 6. Conteúdo social

- [x] 6.1 Criar a tabela post e verificar que um post pode ser associado ao seu autor
- [x] 6.2 Configurar a associação opcional entre post e media e verificar que posts podem ou não referenciar uma mídia
- [x] 6.3 Criar a tabela post_like e verificar que uma curtida pode ser associada a um usuário e a um post
- [x] 6.4 Configurar a prevenção de múltiplas curtidas ativas do mesmo usuário no mesmo post e verificar que duplicações são rejeitadas
- [x] 6.5 Criar a tabela comment e verificar que comentários podem ser associados ao autor e ao post correspondente

## 7. Listas personalizadas

- [x] 7.1 Criar a tabela user_list e verificar que cada lista possui um usuário proprietário
- [x] 7.2 Criar a tabela user_list_item e verificar que itens podem ser associados a listas e mídias
- [x] 7.3 Configurar a prevenção de mídias duplicadas na mesma lista e verificar que uma mídia não pode aparecer duas vezes na mesma lista
- [x] 7.4 Validar que a mesma mídia pode ser adicionada a listas diferentes sem conflito

## 8. Integridade e relacionamentos

- [x] 8.1 Verificar que todas as relações de usuário apontam para registros válidos
- [x] 8.2 Verificar que todas as relações de mídia apontam para registros válidos
- [x] 8.3 Configurar os campos necessários para consultas frequentes e verificar que as relações podem ser recuperadas corretamente
- [x] 8.4 Criar dados de teste representando usuários, mídias, interações, posts e listas
- [x] 8.5 Validar os principais relacionamentos realizando operações de criação e consulta

## 9. Validação final

- [x] 9.1 Executar `openspec validate criar-modelo-dados-xano` e verificar que a change está válida
- [x] 9.2 Revisar todas as tabelas criadas no Xano e verificar que correspondem ao design.md
- [x] 9.3 Confirmar que todas as relações previstas nas specs podem ser persistidas e recuperadas

## Evidência e retomada

Estado em 18/09/2026. A migração inicial do workspace Xano 147717 foi publicada: tabelas sociais, grupo Codeboxd, endpoints e atualizações aos endpoints existentes. Testes reais com duas contas confirmaram cadastro/login, perfil e privacidade, mídia e deduplicação, interações independentes, seguidores, feed, autoria de posts, curtidas, comentários, listas públicas/privadas, ownership e exclusões. Evidência reproduzível está em `.local/remote-results.json`; segredos e contas permanecem em `.local/`, ignorado pelo Git.

Validação remota adicional em 18/09/2026 confirmou posts com e sem mídia opcional e a mesma mídia em duas listas distintas. Os objetos temporários foram excluídos após o teste; nenhuma mídia ou interação persistente foi criada. Com isso, todas as 37 tarefas desta change foram verificadas. A rota remota `/likes` ainda responde 404, embora exista XanoScript local; o estado atual do feed contorna isso pela rota de discussão. Não arquivar enquanto a validação da change de fundação permanecer aberta.
