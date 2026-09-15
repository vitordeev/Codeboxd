<p align="center">
  <img src="docs/images/codeboxd-banner.png" alt="Banner do CodeBoxd" width="100%">
</p>

<h1 align="center">CodeBoxd</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python 3.14">
  <img src="https://img.shields.io/badge/Reflex-Aplicacao_Web-111111" alt="Reflex">
  <img src="https://img.shields.io/badge/Xano-Backend-6138F5" alt="Xano">
  <img src="https://img.shields.io/badge/OpenSpec-Especificacao-F5C518" alt="OpenSpec">
  <img src="https://img.shields.io/badge/Status-Em_desenvolvimento-F5C518" alt="Status: em desenvolvimento">
</p>

<p align="center">
  Descubra, avalie, organize e compartilhe filmes, séries, animes e livros.
</p>

Plataforma social de cultura e entretenimento para descobrir, avaliar, organizar e compartilhar filmes, séries, animes e livros.

O CodeBoxd combina catálogo de mídias, avaliações, listas personalizadas e recursos sociais em uma experiência inspirada em plataformas como Letterboxd. A interface é desenvolvida em Python com Reflex, enquanto o Xano concentra o banco de dados, a autenticação, as APIs e as regras de negócio.

Projeto acadêmico em desenvolvimento por uma equipe de três integrantes.

Objetivo

Criar uma comunidade na qual cada usuário possa:

criar uma conta e editar o próprio perfil;

pesquisar filmes, séries, animes e livros;

consultar informações detalhadas de cada obra;

atribuir notas e publicar avaliações;

marcar o andamento de consumo de uma mídia;

criar e organizar listas personalizadas;

seguir outros usuários;

acompanhar atividades da comunidade em um feed;

descobrir obras populares, bem avaliadas ou adicionadas recentemente.

Identidade visual

A interface segue a prototipação do projeto:

tema escuro com preto e tons de cinza;

amarelo como cor principal de destaque;

cartões e componentes com cantos arredondados;

alto contraste e navegação simples;

menu principal com Início, Feed, Listas e Perfil;

categorias Todos, Filmes, Séries, Animes e Livros.

Paleta principal

Cor

Hexadecimal

Uso

Preto

#0B0B0B

Fundo principal

Cinza-escuro

#1A1A1A

Cards, menus e superfícies

Amarelo

#F5C518

Botões, destaques e estados ativos

Branco

#FFFFFF

Textos principais

Cinza-claro

#B3B3B3

Textos secundários

Tecnologias

Camada

Tecnologia

Responsabilidade

Aplicação web

Python + Reflex

Interface, páginas, componentes e integração com as APIs

Backend

Xano

APIs REST, regras de negócio e validações

Banco de dados

Xano Database

Persistência e relacionamentos

Autenticação

Xano Auth

Cadastro, login, sessão e autorização

Dependências Python

uv

Ambiente virtual e gerenciamento de pacotes

Especificação

OpenSpec

Propostas, requisitos, design e tarefas

Desenvolvimento assistido

Codex

Apoio ao planejamento, implementação e revisão

Versionamento

Git

Histórico de alterações e colaboração da equipe

O Codex é somente uma ferramenta de desenvolvimento e não faz parte das funcionalidades oferecidas pelo CodeBoxd ao usuário final.

Arquitetura

flowchart TD
    U[Usuário] --> R[Aplicação Reflex]
    R --> X[APIs REST do Xano]
    X --> D[(Banco de dados Xano)]
    X --> A[Autenticação Xano]
    E[APIs externas] --> X

Os dados de catálogo podem ser importados das seguintes fontes:

TMDB: filmes e séries;

AniList: animes;

Google Books: livros.

Sempre que possível, os dados externos devem ser importados e armazenados no Xano. A aplicação não deve depender de uma chamada externa a cada carregamento de página.

Funcionalidades do MVP

Conta e perfil

cadastro, login e logout;

exibição e edição do perfil;

avatar, biografia e nome de usuário;

controle de acesso para usuário, moderador e administrador.

Catálogo e descoberta

página inicial com destaques;

busca por título;

filtros por tipo de mídia e gênero;

página de detalhes da obra;

elenco, direção, autoria, sinopse, classificação e trailer quando disponíveis;

seções de tendências, mais bem avaliados e adicionados recentemente.

Avaliações e acompanhamento

nota de 0,5 a 5 estrelas;

criação, edição e remoção lógica de avaliação;

texto de avaliação e aviso de spoiler;

estados: planejado, em andamento, concluído ou abandonado;

registro de gostei ou não gostei.

Listas

criação e edição de listas personalizadas;

listas públicas ou privadas;

inclusão, remoção e ordenação de mídias.

Comunidade

seguir e deixar de seguir usuários;

feed de atividades;

visualização de avaliações e listas públicas.

Comentários, curtidas, favoritos, notificações, denúncias e recomendações avançadas ficam previstos para uma etapa posterior ao MVP.

Banco de dados no Xano

Tabelas existentes que devem ser preservadas

user;

event_log;

grupos de API authentication e event_logs.

Não crie outra tabela de usuários e não armazene senhas manualmente. A autenticação deve continuar sob responsabilidade do Xano Auth.

Tabelas do catálogo

Tabela

Finalidade

media

Registro central de filmes, séries, animes e livros

movie_metadata

Dados específicos de filmes

series_metadata

Temporadas, episódios e estado de séries

anime_metadata

Dados específicos de animes

book_metadata

ISBN, editora, páginas e edição de livros

genre

Gêneros disponíveis

media_genre

Relação muitos-para-muitos entre mídia e gênero

person

Pessoas relacionadas às obras

media_credit

Elenco, direção, roteiro e autoria

O campo media.type aceita somente:

MOVIE;

SERIES;

ANIME;

BOOK.

Identificadores externos, como TMDB, AniList, MyAnimeList, Google Books e ISBN, devem ser únicos quando informados, mas nunca devem substituir o identificador interno da tabela.

Tabelas de interação

Tabela

Finalidade

user_media_state

Progresso, estado de consumo e sentimento do usuário

review

Nota, avaliação escrita, spoiler e estado da publicação

media_list

Listas criadas pelos usuários

list_item

Mídias e suas posições dentro de uma lista

follow

Relação entre seguidor e usuário seguido

activity

Eventos exibidos no feed social

Regras essenciais

um usuário pode ter apenas um estado por mídia;

um usuário pode ter somente uma avaliação ativa por mídia;

uma mídia não pode aparecer duas vezes na mesma lista;

um usuário não pode seguir a si mesmo;

a combinação de seguidor e seguido deve ser única;

avaliações removidas devem usar exclusão lógica;

a média e a quantidade de avaliações de uma mídia devem permanecer consistentes;

endpoints de escrita devem validar o usuário autenticado no Xano.

Ordem recomendada de criação

preservar e revisar user e event_log;

criar media;

criar as tabelas de metadados;

criar genre e media_genre;

criar person e media_credit;

criar user_media_state;

criar review;

criar media_list e list_item;

criar follow;

criar activity.

Divisão da equipe

Responsável

Módulo

Telas e funcionalidades

Tabelas principais

Branch sugerida

Pessoa 1

Catálogo e descoberta

Início, busca, filtros, cards e detalhes

media, metadados, genre, media_genre, person, media_credit

feature/catalogo-descoberta

Pessoa 2

Usuários e social

Autenticação, perfil, seguidores e feed

user, follow, activity

feature/usuarios-social

Pessoa 3

Avaliações e listas

Notas, reviews, andamento e listas

user_media_state, review, media_list, list_item

feature/avaliacoes-listas

Cada módulo deve ter uma mudança própria no OpenSpec:

catalogo-e-descoberta;

usuarios-e-social;

avaliacoes-e-listas.

Pré-requisitos

Windows 10 ou 11;

Python 3.14 instalado;

Git;

uv;

conta e workspace configurados no Xano;

extensão do Xano autenticada no VS Code;

OpenSpec instalado;

extensão oficial do Codex no VS Code.

Instalação

Abra o PowerShell integrado do VS Code na raiz do projeto.

git clone <URL_DO_REPOSITORIO>
cd Codeboxd

Instale as dependências registradas no projeto:

uv sync

Se o comando uv não estiver disponível no PATH, use o executável pelo caminho completo:

& "$env:USERPROFILE\.local\bin\uv.exe" sync

Variáveis de ambiente

Crie um arquivo .env na raiz do projeto. Os nomes finais devem acompanhar a implementação, mas a configuração inicial pode seguir este formato:

XANO_API_BASE_URL=https://SEU-WORKSPACE.xano.io/api:SEU_GRUPO
XANO_AUTH_API_BASE_URL=https://SEU-WORKSPACE.xano.io/api:SEU_GRUPO_AUTH

Nunca envie tokens, senhas ou chaves reais para o Git. Inclua .env no .gitignore e mantenha apenas um .env.example sem dados secretos.

Executando o projeto

Com o terminal aberto na raiz:

uv run reflex run

Caso o uv ainda não esteja no PATH:

& "$env:USERPROFILE\.local\bin\uv.exe" run reflex run

Depois, acesse:

aplicação: http://localhost:3000;

servidor local do Reflex: http://localhost:8000.

Mantenha esse terminal em execução enquanto estiver usando a aplicação. Para encerrar, pressione Ctrl + C.

OpenSpec e Codex

Verifique a configuração do OpenSpec no terminal:

openspec doctor

Comandos iniciados por /, como /opsx:propose, devem ser enviados no chat da extensão Codex, e não no PowerShell. Texto descritivo e prompts também devem ser enviados no chat; o terminal aceita somente comandos de linha de comando instalados.

Antes de implementar uma mudança:

crie a proposta no OpenSpec;

revise requisitos, design e tarefas;

confirme quais tabelas, campos e endpoints do Xano serão alterados;

obtenha aprovação da equipe;

implemente em uma branch própria;

revise o git diff e execute os testes.

O agente de IA pode gerar os arquivos locais do Xano, mas não deve publicar, excluir tabelas ou modificar dados de produção automaticamente. Toda alteração precisa de revisão humana e, quando disponível, execução em modo de simulação antes do envio.

Estrutura esperada

Codeboxd/
├── Codeboxd/              # Código Python e páginas Reflex
├── assets/                # Imagens, fontes e arquivos estáticos
├── docs/
│   └── images/            # Banner e capturas usadas no README
├── openspec/              # Propostas, especificações e tarefas
├── xano/                  # Definições locais do workspace Xano
│   ├── api/
│   ├── function/
│   ├── table/
│   └── workspace/
├── .env.example           # Exemplo de configuração sem segredos
├── .gitignore
├── pyproject.toml
├── rxconfig.py
└── README.md

A estrutura real poderá evoluir conforme os módulos forem implementados.

Fluxo de trabalho com Git

Atualize a branch principal antes de iniciar uma tarefa:

git switch main
git pull
git switch -c feature/nome-da-funcionalidade

Depois de implementar e testar:

git status
git add .
git commit -m "feat: descreva a funcionalidade"
git push -u origin feature/nome-da-funcionalidade

Abra um Pull Request e solicite a revisão de pelo menos uma pessoa da equipe. Evite que duas pessoas alterem simultaneamente a mesma tabela do Xano ou o mesmo componente central.

Critérios de qualidade

interface responsiva e coerente com a prototipação;

componentes reutilizáveis;

estados de carregamento, vazio e erro nas páginas;

validação de entrada no Reflex e no Xano;

autorização conferida no backend;

segredos fora do repositório;

nomes de tabelas e campos em snake_case;

código organizado por domínio;

commits pequenos e objetivos;

testes dos principais fluxos antes de cada Pull Request.

Roadmap

Configurar Python, uv e Reflex

Inicializar o projeto Reflex

Configurar OpenSpec

Conectar e autenticar a extensão do Xano

Aprovar as especificações dos três módulos

Criar e revisar as tabelas do MVP no Xano

Implementar autenticação e perfil

Implementar catálogo, busca e detalhes

Implementar avaliações e acompanhamento

Implementar listas personalizadas

Implementar seguidores e feed

Integrar fontes externas de catálogo

Executar testes integrados

Preparar implantação

Licença

Este projeto foi criado para fins acadêmicos. A equipe deve definir uma licença antes de distribuí-lo publicamente.

Equipe

Projeto desenvolvido por uma equipe de três integrantes. Adicione aqui os nomes, contatos e responsabilidades finais de cada participante.