<p align="center">
  Uma comunidade para descobrir, avaliar, organizar e compartilhar experiências culturais.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Reflex-Aplicacao_Web-111111" alt="Reflex">
  <img src="https://img.shields.io/badge/Xano-Backend-6138F5" alt="Xano">
</p>

Sobre o projeto

O CodeBoxd é uma plataforma social de cultura e entretenimento que reúne filmes, séries, animes e livros em um único lugar.

A proposta é permitir que pessoas com diferentes interesses encontrem novas obras, registrem suas experiências e compartilhem opiniões com a comunidade. Cada usuário pode criar avaliações, acompanhar o que está consumindo, organizar listas e descobrir conteúdos por meio das atividades de outras pessoas.

Tipos de conteúdo

Filmes

Séries

Animes

Livros

Descubra produções e registre o que assistiu

Acompanhe temporadas e episódios

Explore títulos e estúdios

Organize leituras e avaliações

Principais funcionalidades

Descoberta

pesquisa por título;

filtros por tipo de mídia e gênero;

conteúdos populares, recentes e mais bem avaliados;

recomendações relacionadas;

página completa de cada obra.

Avaliações

notas de 0,5 a 5 estrelas;

avaliações escritas;

identificação de conteúdo com spoiler;

edição e gerenciamento das próprias avaliações;

visualização das opiniões da comunidade.

Acompanhamento

obras planejadas;

conteúdos em andamento;

obras concluídas ou abandonadas;

registro de gostei ou não gostei;

acompanhamento do progresso do usuário.

Listas personalizadas

criação de coleções próprias;

listas públicas ou privadas;

organização de filmes, séries, animes e livros;

reordenação dos itens de uma lista.

Comunidade

perfis personalizados;

sistema de seguidores;

feed de atividades;

compartilhamento de listas e avaliações;

descoberta de novos conteúdos através de outros usuários.

Experiência do usuário

flowchart LR
    A[Descobrir] --> B[Consultar]
    B --> C[Avaliar]
    C --> D[Organizar]
    D --> E[Compartilhar]

O usuário começa explorando o catálogo, consulta os detalhes de uma obra, registra sua experiência, adiciona o conteúdo a uma lista e compartilha sua opinião com a comunidade.

Principais páginas

Início: destaques, tendências e recomendações;

Busca: pesquisa e filtros por categoria;

Detalhes: sinopse, informações técnicas, elenco, trailer e avaliações;

Feed: atividades dos usuários seguidos;

Listas: coleções criadas pelo usuário;

Perfil: histórico, avaliações, listas e informações pessoais.

Identidade visual

O CodeBoxd utiliza uma interface escura com elementos em amarelo para destacar as principais ações. O visual foi pensado para oferecer alto contraste, leitura confortável e uma experiência moderna.

Cor

Hexadecimal

Aplicação

Preto

#0B0B0B

Fundo principal

Cinza-escuro

#1A1A1A

Cards e superfícies

Amarelo

#F5C518

Botões e destaques

Branco

#FFFFFF

Textos principais

Cinza-claro

#B3B3B3

Textos secundários

Tecnologias

Tecnologia

Utilização

Python

Linguagem principal do projeto

Reflex

Construção da aplicação web e da interface

Xano

Banco de dados, autenticação, APIs e regras de negócio

Git e GitHub

Versionamento e colaboração

Arquitetura

flowchart TD
    U[Usuário] --> R[Aplicação Reflex]
    R --> X[APIs do Xano]
    X --> D[(Banco de dados)]
    X --> A[Autenticação]

A aplicação Reflex apresenta a interface e consome as APIs do Xano. O Xano é responsável pela autenticação, persistência dos dados e regras de negócio da plataforma.

Fontes de dados

O catálogo pode ser enriquecido por serviços especializados:

TMDB: filmes e séries;

AniList: animes;

Google Books: livros.

Diferenciais

diferentes formatos culturais reunidos em uma única plataforma;

recursos de catálogo, organização e comunidade integrados;

experiência visual consistente para filmes, séries, animes e livros;

perfis que representam os interesses culturais de cada usuário;

descoberta de conteúdo baseada também nas interações da comunidade.

Equipe

Projeto acadêmico desenvolvido por uma equipe de três integrantes do curso de Análise e Desenvolvimento de Sistemas.

Os nomes e perfis dos integrantes podem ser adicionados nesta seção.

Licença

Projeto criado para fins acadêmicos e de portfólio.