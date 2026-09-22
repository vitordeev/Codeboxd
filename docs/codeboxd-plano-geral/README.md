# CodeBoxd — Plano Geral

Este diretório consolida o entendimento atual do projeto, o estado do workspace Xano, o modelo de produto definido no OpenSpec e os próximos passos de implementação.

## Documentos

- [Estado atual](estado-atual.md): o que existe hoje no repositório e no Xano.
- [Arquitetura alvo](arquitetura-alvo.md): responsabilidades do frontend, backend e fontes externas.
- [Modelo de dados](modelo-dados.md): entidades, campos principais e regras de integridade.
- [Inconsistências e decisões](decisoes-e-inconsistencias.md): pontos que precisam ser resolvidos antes da implementação.
- [Roadmap](roadmap.md): sequência recomendada de execução.

## Visão do produto

O CodeBoxd será uma plataforma social para descoberta, registro, organização e compartilhamento de experiências culturais relacionadas a:

- Filmes
- Séries
- Animes
- Livros

O usuário deverá poder pesquisar uma obra, visualizar seus detalhes, registrar status de consumo, atribuir nota, escrever uma review, organizar mídias em listas, publicar atividades e acompanhar outros usuários.

## Estado resumido

O projeto está na fase de fundação e especificação. O OpenSpec já descreve as principais capacidades, mas a implementação do domínio ainda não foi criada.

O workspace Xano autenticado é `Victor's Workspace` (`151345`). Ele contém a estrutura inicial do Quick Start do Xano, com autenticação, recuperação de senha e logs de eventos. As tabelas próprias do CodeBoxd ainda precisam ser criadas.

## Regra de segurança

Tokens, senhas, credenciais e variáveis secretas não devem ser armazenados nesta documentação nem versionados no Git.
