## Context

O Codeboxd é uma plataforma social para descoberta, registro e compartilhamento de experiências relacionadas a filmes, séries, animes e livros.

A aplicação utilizará o Xano como backend e camada de persistência, enquanto o frontend será desenvolvido utilizando Streamlit. Informações detalhadas sobre mídias poderão ser obtidas através de APIs externas, enquanto os dados específicos da plataforma deverão ser persistidos no Xano.

Esta arquitetura precisa suportar relacionamentos entre usuários, mídias, interações pessoais, listas e funcionalidades sociais sem duplicar informações ou comprometer a integridade dos dados.

Veja `proposal.md` para a motivação da change e as specs desta change para os comportamentos esperados.

## Goals / Non-Goals

**Goals:**

- Criar um modelo de dados organizado para persistir as informações do Codeboxd.
- Permitir a identificação única de usuários.
- Separar dados de autenticação dos dados públicos de perfil.
- Criar uma representação unificada para filmes, séries, animes e livros.
- Permitir relacionamentos entre usuários e mídias.
- Suportar avaliações, status e reviews.
- Suportar relações sociais entre usuários.
- Suportar posts, curtidas e comentários.
- Suportar listas personalizadas.
- Evitar duplicação de mídias provenientes de APIs externas.
- Criar uma estrutura preparada para crescimento futuro da aplicação.

**Non-Goals:**

- Armazenar permanentemente todas as informações fornecidas pelas APIs externas.
- Definir o layout ou comportamento visual do frontend.
- Implementar algoritmos de recomendação.
- Implementar notificações nesta etapa.
- Implementar moderação ou denúncias de conteúdo nesta etapa.
- Definir todos os endpoints da API nesta change.

## Decisions

### 1. Utilizar uma tabela unificada para mídias

O sistema utilizará uma única entidade `media` para representar:

- filmes;
- séries;
- animes;
- livros.

Cada registro possuirá um campo que identifica seu tipo.

Exemplo:

```text
media_type

movie
series
anime
book