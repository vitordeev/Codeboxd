## Purpose

Permitir descoberta intencional de obras, pessoas e listas públicas em um ponto
de busca consistente, com escopos identificados, paginação e proteção de privacidade.

## ADDED Requirements

### Requirement: Escopos de busca independentes
A busca SHALL distinguir Obras, Pessoas e Listas públicas e consultar apenas o escopo ativo submetido. Obras SHALL preservar busca textual nos quatro tipos, relevância e categorias separadas já existentes.

#### Scenario: Buscar obra após navegar em categoria
- **WHEN** o usuário envia consulta de Obras após explorar Filmes
- **THEN** a busca SHALL continuar pesquisando filmes, séries, animes e livros, sem reaproveitar a categoria como filtro textual oculto

#### Scenario: Trocar de domínio
- **WHEN** o usuário alterna para Pessoas ou Listas públicas
- **THEN** a interface SHALL identificar o domínio, não apresentar resultados do domínio anterior como atuais e consultar somente o domínio escolhido

#### Scenario: Digitar sem submeter
- **WHEN** o usuário edita o texto de busca
- **THEN** essa edição SHALL NOT disparar consultas de todos os domínios ou alterar silenciosamente a consulta usada na paginação atual

### Requirement: Busca de listas por critérios do domínio
O sistema SHALL permitir encontrar listas públicas por título, com filtros explícitos de criador e opção de incluir descrição. Resultados SHALL ter ordenação estável, identificação do criador e acesso ao detalhe, sem depender de atividade no feed.

#### Scenario: Encontrar coleção pelo título
- **WHEN** uma consulta corresponde a títulos de listas públicas
- **THEN** os resultados SHALL apresentar essas listas com criador identificável, link ao perfil e detalhe, inclusive quando títulos iguais pertencem a pessoas distintas

#### Scenario: Refinar por criador ou descrição
- **WHEN** o usuário aplica um criador ou escolhe incluir a descrição
- **THEN** os resultados SHALL respeitar os critérios visíveis e informar como limpar o filtro, sem inventar tags ou metadados inexistentes

### Requirement: Busca de pessoas com projeção pública
A busca de Pessoas SHALL pesquisar username e nome de exibição com paginação no servidor e abrir o perfil selecionado. Somente dados públicos necessários SHALL ser apresentados, sem expor e-mail, credenciais ou informações administrativas.

#### Scenario: Encontrar perfil
- **WHEN** o usuário envia username ou parte do nome de exibição
- **THEN** os perfis correspondentes SHALL ser identificados por nome/@ e link para seu perfil, com fallback quando avatar está ausente

### Requirement: Privacidade antes da resposta pública
Filtragem de privacidade SHALL ocorrer no servidor antes da paginação, contagem e geração de resumo. Listas privadas SHALL NOT aparecer em resultados públicos, totais, previews, HTML ou caches compartilhados, mesmo quando pertencem ao usuário autenticado que faz a busca pública.

#### Scenario: Título coincide com lista privada
- **WHEN** uma lista privada é a única correspondência da consulta pública
- **THEN** a busca SHALL responder sem expor existência, título, criador, itens ou contagem dessa lista

#### Scenario: Lista deixa de ser pública
- **WHEN** uma lista previamente encontrada muda para privada e é consultada novamente
- **THEN** resultados e detalhe público SHALL revalidar acesso e não restaurar o conteúdo por cache, URL direta ou estado de outra conta

#### Scenario: Busca das próprias listas
- **WHEN** o usuário quer localizar ou gerenciar suas listas privadas
- **THEN** ele SHALL utilizar o contexto pessoal autenticado, sem incorporá-las ao resultado de Listas públicas

### Requirement: Paginação e contexto reproduzíveis
Cada escopo SHALL manter sua consulta submetida, filtros, página e estado na navegação. Recarregar ou voltar SHALL recuperar contexto válido; mudança de conta/consulta/escopo SHALL impedir resposta atrasada de preencher o contexto novo.

#### Scenario: Abrir detalhe e voltar
- **WHEN** o usuário abre um resultado e retorna à busca
- **THEN** escopo, consulta e página SHALL ser recuperados sem confundir texto ainda não submetido com a consulta anterior

#### Scenario: Página com mais resultados
- **WHEN** o usuário solicita continuação
- **THEN** ela SHALL trazer itens da mesma consulta visível, sem omissões ou duplicação por troca de escopo, e só indicar continuação/totais confirmados

#### Scenario: Resposta obsoleta
- **WHEN** uma consulta anterior termina após troca de domínio ou conta
- **THEN** seus dados SHALL NOT substituir os resultados ativos nem reapresentar dados privados de outra sessão

### Requirement: Vazio, erro e limites distinguíveis
A busca SHALL distinguir ausência de correspondências, carregamento, falha de serviço e limitação de requisições. Resultados utilizáveis SHALL permanecer acessíveis em falhas parciais aplicáveis, com recuperação explícita e sem repetição cega de consultas.

#### Scenario: Domínio indisponível
- **WHEN** o serviço de listas ou pessoas falha
- **THEN** a interface SHALL informar a falha naquele escopo, sem afirmar que não existem resultados ou consultar dados privados como fallback

#### Scenario: Limite de requisições
- **WHEN** o backend retorna limitação temporária
- **THEN** a busca SHALL respeitar a espera e manter a consulta, sem tempestade de requisições ou bloqueio dos demais conteúdos disponíveis
