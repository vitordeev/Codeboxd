> Estado reconciliado em 26/10/2026: 21/34 tarefas concluídas, 13 abertas. Tabela report e endpoints publicados em 13–19/10; interface com fixtures em 22/10. Leituras admin reais de 23/10 constam na change de performance. Faltam critérios completos de autorização, mutações, auditoria e browser real; não arquivar. As seções e rodadas anteriores abaixo preservam o planejamento e sua evolução; o checklist e a evidência datada prevalecem sobre resumos antigos.

## Why

O Codeboxd precisa de uma área administrativa para acompanhar a atividade do site e permitir que pessoas autorizadas gerenciem usuários, catálogo e denúncias em um só lugar. Esta proposta nasceu antes da implementação do fluxo. Na revisão de 13/10/2026, telas, estados e contratos locais já existiam; naquele momento, faltavam autorização e persistência remotas, testes integrados e validação visual. O escopo de aceite atualizado em 12/11 está registrado abaixo. Ver `tasks.md` e `validation/revisao-2026-10-13.md`.

## Escopo de aceite — atualização de 12/11/2026

Esta change encerra a entrega da interface administrativa e seu aceite integrado
de leitura comprovado: áreas administrativas, buscas vazias, falha parcial
controlada e larguras desktop/celular, conforme a evidência de 11/11/2026.
Esse encerramento não afirma aceite integrado de mutações, persistência de
alterações ou auditoria real. Suspensão/reativação, criação/edição de catálogo
e decisões de reports integradas deverão ser verificadas em uma change futura,
com ambiente Xano isolado e autorização específica antes de qualquer escrita.

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
- Xano: contratos locais de autorização, indicadores, usuários, catálogo e reports/auditoria; implantação remota e verificações reais ainda precisam de evidência.
- Catálogo existente: integração com os registros e fontes já usados para filmes, séries, livros e animes, sem criar duplicatas.
- Autenticação: reutilizar a identidade e os papéis existentes, confirmando autorização em cada operação administrativa.
- O projeto não criará um sistema de mensagens privadas nesta mudança. Os reports poderão apontar para mensagens se esse conteúdo já existir ou vier a ser integrado; os tipos de alvo efetivamente disponíveis devem ser confirmados no levantamento.
