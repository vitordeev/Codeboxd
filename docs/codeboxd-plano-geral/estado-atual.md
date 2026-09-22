# Estado atual

## Repositório

O repositório contém:

- `README.md` com a visão conceitual e a identidade do CodeBoxd.
- `openspec/config.yaml`.
- A change `definir-fundacao-codeboxd`, com proposta, design, especificações e tarefas.
- A change `criar-modelo-dados-xano`, com a proposta do modelo persistente, design, especificações e tarefas.
- Arquivos `.xs` exportados do Xano.
- Configurações auxiliares para OpenSpec em `.github`, `.claude`, `.gemini`, `.opencode` e `.agents`.

Não há, atualmente, código de frontend em Python, Streamlit ou Reflex. Também não há integração implementada com APIs externas de mídia.

## Xano conectado

Workspace verificado:

| Item | Valor |
|---|---|
| Workspace | `Victor's Workspace` |
| Workspace ID | `151345` |
| Instância | `x8ki-letl-twmt` |
| Perfil CLI | perfil padrão associado ao workspace `151345` |

O workspace respondeu corretamente à consulta de identidade e à listagem de workspaces.

## Documentos Xano existentes

O workspace possui 19 documentos, todos relacionados ao Quick Start:

### Tabelas

- `user`
- `event_log`

### Endpoints de autenticação

- `auth/signup`
- `auth/login`
- `auth/me`
- `reset/request-reset-link`
- `reset/magic-link-login`
- `reset/update_password`
- `message/send_welcome_email`

### Outros recursos

- Consulta de eventos do usuário.
- Função de geração de magic link.
- Função de registro de eventos.
- Função de validação de papel.
- Addon de usuário.
- Agente e ferramenta de exemplo para documentação Xano.

## Dados existentes

### Tabela `user`

Campos atuais:

- `id`
- `created_at`
- `name`
- `email`
- `password`
- `role`
- `password_reset.token`
- `password_reset.expiration`
- `password_reset.used`

Existe índice único para `email`.

### Tabela `event_log`

Campos atuais:

- `id`
- `created_at`
- `user_id`
- `action`
- `metadata`

## Validação do OpenSpec

As duas changes atuais passaram na validação do OpenSpec sem findings:

- `definir-fundacao-codeboxd`
- `criar-modelo-dados-xano`

Isso valida a estrutura dos artefatos, mas não significa que as funcionalidades estejam implementadas no Xano.
