## MODIFIED Requirements

### Requirement: Paginacao ampliada nas abas de filmes, series e animes
As abas administrativas de filmes, series, livros e animes MUST apresentar ate 35 resultados por pagina, preservando busca, identidade e paginacao dos registros cadastrados. Quando series, animes ou livros tiverem menos de 35 registros cadastrados, a primeira pagina MUST complementar a exibicao com resultados reais de TMDB, Kitsu ou Open Library, respectivamente, sem gravar esses resultados. Resultados externos MUST NOT receber uma etiqueta de "nao cadastrado" nem acao de edicao de registro salvo. A administracao MUST NOT oferecer uma acao de importacao/completamento em lote.

#### Scenario: Existem ao menos 35 obras na categoria
- **WHEN** uma administradora abre a primeira pagina de qualquer categoria com pelo menos 35 registros correspondentes
- **THEN** a secao apresenta 35 registros reais e mantem a paginacao para os demais

#### Scenario: Existem menos de 35 obras na categoria
- **WHEN** a categoria ou o resultado da busca contem menos de 35 registros
- **THEN** series, animes e livros completam a exibicao com resultados externos ate 35, enquanto filmes apresentam apenas os registros existentes

#### Scenario: Resultado externo e somente para consulta
- **WHEN** uma obra vem do provedor externo
- **THEN** a interface apresenta a obra sem etiqueta de cadastro, nao permite edita-la como registro persistido e nao a grava no catalogo

#### Scenario: Aba aberta sem acao de importacao
- **WHEN** a administradora abre series, animes ou livros
- **THEN** o sistema consulta candidatos externos para exibicao sem criar registros ou oferecer importacao em lote

#### Scenario: Categoria nao incluida no aumento
- **WHEN** a administradora abre a aba de filmes
- **THEN** a pagina mantem ate 35 registros cadastrados e nao consulta resultados externos

#### Scenario: Navegacao por categoria sem abas duplicadas
- **WHEN** a administradora abre uma categoria do catalogo
- **THEN** as categorias sao acessadas pela navegacao lateral, sem uma segunda fileira de abas no topo

## REMOVED Requirements

### Requirement: Completar series e animes com obras reais
**Reason**: O usuario pediu para retirar os controles de importar/completar listas do painel administrativo.
**Migration**: Series, animes e livros continuam mostrando resultados externos somente para consulta; nenhuma obra externa e persistida por essa acao.

#### Scenario: Administradora completa uma aba com sucesso
- **WHEN** uma administradora abre uma aba de series, animes ou livros
- **THEN** o painel nao oferece importacao em lote nem grava obras automaticamente

#### Scenario: Provedor ou persistencia falha durante a importacao
- **WHEN** uma aba administrativa e aberta
- **THEN** nenhum candidato externo e gravado no catalogo

#### Scenario: Identidades externas ja existem
- **WHEN** uma administradora navega pelo catalogo externo
- **THEN** identidades ja cadastradas nao aparecem duplicadas e os resultados externos nao sao persistidos
