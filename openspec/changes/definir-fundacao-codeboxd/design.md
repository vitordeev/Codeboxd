## Context

O Codeboxd é um novo projeto sem implementação existente. A plataforma será desenvolvida como uma aplicação social para descoberta, organização e compartilhamento de experiências relacionadas a filmes, séries, animes e livros.

A motivação e as capacidades funcionais estão definidas em `proposal.md`. Os requisitos comportamentais serão definidos nas especificações da change.

A solução precisa suportar diferentes fontes externas de dados e apresentar seus resultados de forma consistente para o usuário. Também precisa armazenar dados próprios da plataforma, como usuários, avaliações, reviews, posts, curtidas, comentários, seguidores e listas.

As principais restrições tecnológicas iniciais são:

- Interface desenvolvida com Python e Streamlit.
- Backend e armazenamento de dados utilizando Xano.
- Integração com fontes externas para obtenção de dados sobre mídias.
- O catálogo externo não deverá ser completamente copiado para o banco do Codeboxd.

## Goals / Non-Goals

**Goals:**

- Criar uma arquitetura que separe claramente a interface, os serviços do Codeboxd e as fontes externas de dados.
- Utilizar o Xano como ponto central para as operações relacionadas aos dados do Codeboxd.
- Criar uma representação consistente para filmes, séries, animes e livros.
- Permitir que dados externos sejam associados a interações e conteúdos criados pelos usuários.
- Evitar que o Streamlit dependa diretamente de múltiplas APIs externas.
- Permitir a evolução futura da plataforma sem exigir mudanças significativas na interface para cada nova fonte de dados.

**Non-Goals:**

- Importar todos os filmes, séries, animes e livros disponíveis nas APIs externas.
- Reproduzir integralmente as funcionalidades de plataformas como Instagram, Letterboxd, AniList ou Goodreads.
- Definir detalhes visuais completos da interface neste documento.
- Definir tarefas específicas de implementação ou código.
- Definir uma infraestrutura de alta escala nesta primeira versão.

## Decisions

### Separar frontend, backend e fontes externas

O Streamlit será responsável pela apresentação da interface e pelas interações do usuário.

O Xano será responsável pelos dados e operações do Codeboxd, incluindo autenticação, dados de usuários, atividades sociais e relacionamento entre os registros.

As APIs externas serão utilizadas para fornecer informações sobre mídias.

Fluxo principal:

```text
Usuário
   ↓
Streamlit
   ↓
Xano
   ↓
Fontes externas de dados