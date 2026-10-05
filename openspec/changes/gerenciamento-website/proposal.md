## Why

O Codeboxd precisa de uma área administrativa para acompanhar a atividade do site e permitir que pessoas autorizadas gerenciem usuários, catálogo e denúncias em um só lugar. Hoje não há um fluxo administrativo especificado que conecte esses dados e ações com permissões verificadas no servidor.

## What Changes

- Criar um painel administrativo com indicadores reais, atividade recente e itens pendentes.
- Permitir pesquisar usuários, consultar informações administrativas e suspender ou reativar contas conforme as permissões existentes.
- Organizar o gerenciamento do catálogo em seções para filmes, séries, livros e animes, com busca, filtros e correção de registros existentes.
- Criar uma fila de reports para mensagens e outros conteúdos, com estados de análise e registro da decisão e do responsável.
- Proteger páginas e operações administrativas no backend, apresentar estados de carregamento, erro e vazio e adaptar a interface para desktop e celular.

- Criar uma rota de login administrativo separada em `/admin/login`, reutilizando a autenticação existente e autorizando o painel somente para contas com papel `admin`.

## Capabilities

### New Capabilities

- `admin-dashboard`: Visão administrativa de indicadores, atividade recente e pendências reais do sistema.
- `admin-user-management`: Pesquisa, consulta e ações autorizadas sobre contas de usuários.
- `admin-catalog-management`: Consulta e manutenção administrativa do catálogo separado por tipo de obra.
- `content-moderation`: Registro, análise e resolução de denúncias sobre mensagens e outros conteúdos.

### Modified Capabilities

Nenhuma. As capacidades administrativas ainda não estão descritas nas especificações existentes.

## Impact

- Interface Reflex: navegação protegida e novas páginas, estados e componentes administrativos.
- Xano: verificação de papel e autorização no servidor; possíveis endpoints e estruturas para relatórios, estados de moderação e auditoria.
- Catálogo existente: integração com os registros e fontes já usados para filmes, séries, livros e animes, sem criar duplicatas.
- Autenticação: reutilizar a identidade e os papéis existentes, confirmando autorização em cada operação administrativa.
- O projeto não criará um sistema de mensagens privadas nesta mudança. Os reports poderão apontar para mensagens se esse conteúdo já existir ou vier a ser integrado; os tipos de alvo efetivamente disponíveis devem ser confirmados no levantamento.
