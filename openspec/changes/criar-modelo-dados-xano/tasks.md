## 1. Preparação do modelo de dados

- [ ] 1.1 Revisar as specs de persistência e verificar que todas as capabilities possuem requisitos definidos
- [ ] 1.2 Confirmar a estrutura das entidades e relacionamentos definidos no design.md
- [ ] 1.3 Preparar o workspace do Xano e verificar que o banco de dados está disponível para criação das tabelas

## 2. Usuários e perfis

- [ ] 2.1 Criar a tabela de usuários e verificar que cada registro possui uma identidade única
- [ ] 2.2 Configurar os campos únicos necessários para identificação do usuário e verificar que registros duplicados são rejeitados
- [ ] 2.3 Criar a tabela de perfis e verificar que um perfil pode ser associado a um usuário
- [ ] 2.4 Configurar a relação entre usuário e perfil e verificar que os dados permanecem associados corretamente

## 3. Catálogo de mídias

- [ ] 3.1 Criar a tabela media e verificar que ela suporta filmes, séries, animes e livros
- [ ] 3.2 Adicionar os campos de identificação e verificar que cada mídia possui uma identidade interna
- [ ] 3.3 Adicionar o tipo da mídia e verificar que o registro identifica corretamente sua categoria
- [ ] 3.4 Adicionar os identificadores external_source e external_id e verificar que mídias externas podem ser identificadas
- [ ] 3.5 Configurar a prevenção de duplicação por fonte e identificador externo e verificar que registros duplicados não são criados

## 4. Interações entre usuários e mídias

- [ ] 4.1 Criar a tabela user_media_interaction e verificar que uma interação pode ser associada a um usuário e uma mídia
- [ ] 4.2 Adicionar o campo de status e verificar que o estado da interação pode ser persistido
- [ ] 4.3 Adicionar o campo de avaliação e verificar que uma avaliação válida pode ser armazenada
- [ ] 4.4 Adicionar o campo de review e verificar que uma avaliação textual pode ser associada à interação
- [ ] 4.5 Validar que diferentes usuários podem possuir interações independentes com a mesma mídia

## 5. Relações sociais

- [ ] 5.1 Criar a tabela user_follow e verificar que um usuário pode seguir outro usuário
- [ ] 5.2 Configurar a direção da relação entre follower_user e followed_user e verificar que os papéis permanecem distintos
- [ ] 5.3 Configurar a prevenção de relações de seguimento duplicadas e verificar que a mesma relação não pode ser persistida duas vezes

## 6. Conteúdo social

- [ ] 6.1 Criar a tabela post e verificar que um post pode ser associado ao seu autor
- [ ] 6.2 Configurar a associação opcional entre post e media e verificar que posts podem ou não referenciar uma mídia
- [ ] 6.3 Criar a tabela post_like e verificar que uma curtida pode ser associada a um usuário e a um post
- [ ] 6.4 Configurar a prevenção de múltiplas curtidas ativas do mesmo usuário no mesmo post e verificar que duplicações são rejeitadas
- [ ] 6.5 Criar a tabela comment e verificar que comentários podem ser associados ao autor e ao post correspondente

## 7. Listas personalizadas

- [ ] 7.1 Criar a tabela user_list e verificar que cada lista possui um usuário proprietário
- [ ] 7.2 Criar a tabela user_list_item e verificar que itens podem ser associados a listas e mídias
- [ ] 7.3 Configurar a prevenção de mídias duplicadas na mesma lista e verificar que uma mídia não pode aparecer duas vezes na mesma lista
- [ ] 7.4 Validar que a mesma mídia pode ser adicionada a listas diferentes sem conflito

## 8. Integridade e relacionamentos

- [ ] 8.1 Verificar que todas as relações de usuário apontam para registros válidos
- [ ] 8.2 Verificar que todas as relações de mídia apontam para registros válidos
- [ ] 8.3 Configurar os campos necessários para consultas frequentes e verificar que as relações podem ser recuperadas corretamente
- [ ] 8.4 Criar dados de teste representando usuários, mídias, interações, posts e listas
- [ ] 8.5 Validar os principais relacionamentos realizando operações de criação e consulta

## 9. Validação final

- [ ] 9.1 Executar `openspec validate criar-modelo-dados-xano` e verificar que a change está válida
- [ ] 9.2 Revisar todas as tabelas criadas no Xano e verificar que correspondem ao design.md
- [ ] 9.3 Confirmar que todas as relações previstas nas specs podem ser persistidas e recuperadas