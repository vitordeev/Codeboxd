# admin-catalog-management Specification

## Purpose

Organiza a consulta e a manutenção administrativa do catálogo do Codeboxd por tipo de obra, preservando a identidade dos registros e as integrações existentes.

## Requirements

### Requirement: Seções de catálogo por tipo
O sistema MUST oferecer seções administrativas distintas para filmes, séries, livros e animes, usando os registros existentes no catálogo.

#### Scenario: Administradora abre uma seção
- **WHEN** uma administradora seleciona um tipo de obra
- **THEN** o sistema apresenta registros daquele tipo e permite pesquisar e filtrar os resultados

#### Scenario: Seção sem resultados
- **WHEN** nenhum registro corresponde à busca ou aos filtros
- **THEN** o sistema informa que não há resultados e permite alterar os critérios

### Requirement: Acesso autorizado ao catálogo administrativo
O sistema MUST verificar no backend o papel administrativo antes de consultar ou modificar dados do catálogo por meio da área de gerenciamento.

#### Scenario: Pessoa sem autorização solicita uma operação
- **WHEN** uma pessoa sem papel administrativo tenta acessar uma operação do catálogo administrativo
- **THEN** o sistema rejeita a solicitação e não altera nem revela dados restritos

### Requirement: Corrigir registros existentes
O sistema MUST permitir que uma administradora autorizada consulte e corrija campos administrativos suportados de um registro existente sem alterar sua identidade ou suas referências externas. O sistema MUST validar os dados antes de salvar.

#### Scenario: Correção válida
- **WHEN** uma administradora salva alterações válidas em uma obra existente
- **THEN** o sistema atualiza o registro e informa o resultado

#### Scenario: Dados inválidos
- **WHEN** os dados enviados não passam pela validação
- **THEN** o sistema informa os campos inválidos e preserva o registro anterior

### Requirement: Evitar duplicatas no catálogo
O sistema MUST verificar a identidade externa e o tipo da obra antes de cadastrar qualquer registro novo pela área administrativa, reutilizando o registro correspondente quando ele já existir.

#### Scenario: Obra já cadastrada
- **WHEN** a administradora tenta adicionar uma obra com identidade externa já registrada para aquele tipo
- **THEN** o sistema evita a duplicação e direciona para o registro existente

#### Scenario: Obra ainda não cadastrada
- **WHEN** a identidade externa e o tipo não correspondem a um registro existente
- **THEN** o sistema permite criar o registro somente após validar os campos exigidos


### Requirement: Paginacao ampliada nas abas de filmes, series e animes
As abas administrativas de filmes, series e animes MUST solicitar ate 35 registros existentes por pagina, preservando busca, ordenacao, identidade dos registros e paginacao. O sistema MUST apresentar apenas os registros disponiveis; nao deve criar, importar ou simular obras para completar a pagina. A aba de livros mantem o tamanho de pagina atual.

#### Scenario: Existem ao menos 35 obras na categoria
- **WHEN** uma administradora abre a primeira pagina de filmes, series ou animes com pelo menos 35 registros correspondentes
- **THEN** a secao apresenta 35 registros reais e mantem a paginacao para os demais

#### Scenario: Existem menos de 35 obras na categoria
- **WHEN** a categoria ou o resultado da busca contem menos de 35 registros
- **THEN** a secao apresenta somente os registros existentes e informa corretamente o estado vazio ou a quantidade disponivel

#### Scenario: Categoria nao incluida no aumento
- **WHEN** a administradora abre a aba de livros
- **THEN** a paginacao conserva o tamanho de pagina vigente para livros
