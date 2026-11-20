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


### Requirement: Excluir logicamente obra removida por moderacao
Uma obra removida por decisao administrativa MUST deixar de aparecer no catalogo publico e MUST deixar de aceitar novas interacoes/listas. A remocao MUST preservar o registro, as referencias historicas de usuarios, o report e sua auditoria; a area administrativa MUST identificar a obra como removida.

#### Scenario: Obra reportada e removida
- **WHEN** uma administradora confirma a remocao da obra vinculada a um report
- **THEN** a obra desaparece de buscas e selecoes publicas, referencias historicas permanecem consistentes e o report continua consultavel

#### Scenario: Usuario tenta criar nova referencia a obra removida
- **WHEN** uma pessoa tenta avaliar, listar ou vincular uma obra removida
- **THEN** o backend rejeita a nova referencia sem apagar dados historicos existentes

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
