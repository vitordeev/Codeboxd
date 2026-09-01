## Why

O Codeboxd será uma plataforma social para descoberta, organização e compartilhamento de experiências relacionadas a filmes, séries, animes e livros. A mudança é necessária para estabelecer as capacidades fundamentais do produto antes do início do desenvolvimento, garantindo que as funcionalidades tenham comportamentos bem definidos e possam evoluir de forma organizada.

## What Changes

* Criar uma plataforma unificada para filmes, séries, animes e livros.
* Permitir a descoberta e pesquisa de mídias de diferentes tipos em uma única interface.
* Permitir que usuários criem contas e mantenham perfis pessoais.
* Permitir que usuários visualizem detalhes de mídias e interajam com elas.
* Permitir que usuários registrem o consumo de mídias e atribuam avaliações e reviews.
* Criar um sistema de biblioteca pessoal para organizar mídias de acordo com o status de consumo.
* Criar um sistema de listas personalizadas que permita agrupar diferentes tipos de mídia.
* Criar um sistema social baseado em publicações e atividades relacionadas às mídias consumidas.
* Permitir que usuários sigam outros usuários e acompanhem suas atividades.
* Criar um feed que apresente publicações e atividades de usuários seguidos.
* Integrar o sistema com fontes externas de dados para obter informações sobre filmes, séries, animes e livros.

## Capabilities

### New Capabilities

* `media-catalog`: Define o catálogo unificado de filmes, séries, animes e livros e os comportamentos relacionados à identificação e visualização dessas mídias.
* `media-discovery`: Define a descoberta, pesquisa e filtragem de mídias disponíveis na plataforma.
* `user-authentication`: Define o cadastro, autenticação e gerenciamento de sessões dos usuários.
* `user-profile`: Define os perfis públicos dos usuários e a visualização de suas atividades e informações.
* `media-interactions`: Define como usuários registram o consumo de mídias, atribuem avaliações e escrevem reviews.
* `social-feed`: Define a criação e exibição de publicações e atividades relacionadas às interações dos usuários com mídias.
* `social-connections`: Define o relacionamento entre usuários por meio das funcionalidades de seguir e deixar de seguir.
* `user-lists`: Define a criação e gerenciamento de listas personalizadas contendo mídias.
* `media-data-integration`: Define a obtenção e utilização de dados de fontes externas para filmes, séries, animes e livros.

### Modified Capabilities

Nenhuma, pois esta é a criação inicial das capacidades do projeto.

## Impact

Esta mudança estabelece a fundação funcional do Codeboxd e servirá como base para as futuras implementações do projeto.

Os sistemas afetados incluem a interface do usuário, os serviços de backend, o armazenamento de dados dos usuários e as integrações com fontes externas de informações sobre mídias.

O projeto utilizará o Streamlit com Python para a interface do usuário e o Xano para os serviços de backend e armazenamento de dados. O sistema também dependerá de APIs externas para obter dados de filmes, séries, animes e livros.
