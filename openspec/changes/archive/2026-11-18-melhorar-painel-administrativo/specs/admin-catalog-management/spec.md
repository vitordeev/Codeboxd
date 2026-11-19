## ADDED Requirements

### Requirement: Paginação ampliada nas abas de filmes, séries e animes
As abas administrativas de filmes, séries e animes MUST solicitar até 35 registros existentes por página, preservando busca, ordenação, identidade dos registros e paginação. O sistema MUST apresentar apenas os registros disponíveis; não deve criar, importar ou simular obras para completar a página. A aba de livros mantém o tamanho de página atual.

#### Scenario: Existem ao menos 35 obras na categoria
- **WHEN** uma administradora abre a primeira página de filmes, séries ou animes com pelo menos 35 registros correspondentes
- **THEN** a seção apresenta 35 registros reais e mantém a paginação para os demais

#### Scenario: Existem menos de 35 obras na categoria
- **WHEN** a categoria ou o resultado da busca contém menos de 35 registros
- **THEN** a seção apresenta somente os registros existentes e informa corretamente o estado vazio ou a quantidade disponível

#### Scenario: Categoria não incluída no aumento
- **WHEN** a administradora abre a aba de livros
- **THEN** a paginação conserva o tamanho de página vigente para livros
