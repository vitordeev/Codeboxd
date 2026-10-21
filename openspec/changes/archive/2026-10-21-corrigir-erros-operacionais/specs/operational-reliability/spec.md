## Purpose

Garantir operação reproduzível do Codeboxd, preservar imagens enviadas e evitar o compartilhamento acidental de arquivos privados e dados gerados.

## ADDED Requirements

### Requirement: Protect local private and generated files

O projeto MUST excluir arquivos privados e gerados do conjunto versionado, preservando suas cópias locais durante a correção de rastreamento. Credenciais MUST NOT ser copiadas para relatórios.

#### Scenario: Remove local artifacts from version control

- **WHEN** a proteção de arquivos é aplicada
- **THEN** arquivos privados e gerados deixam de ser rastreados sem apagar suas cópias locais

### Requirement: Reproducible development environment

O projeto MUST fornecer um ambiente de desenvolvimento documentado com dependências diretas fixadas e comandos verificáveis de teste e compilação.

#### Scenario: Validate configured environment

- **WHEN** o ambiente documentado tem suas dependências instaladas
- **THEN** os testes locais e a compilação da aplicação podem ser executados com esse ambiente

### Requirement: Readable upload failures

O sistema MUST apresentar mensagens legíveis em português para falhas de envio de imagem, sem escapes Unicode literais nem respostas internas do provedor.

#### Scenario: Upload is rejected or unavailable

- **WHEN** o envio falha por conexão, autorização ou rejeição dos dados
- **THEN** a pessoa recebe uma mensagem legível e a falha mantém sua classificação HTTP quando aplicável

### Requirement: Usable persisted banner URL

O sistema MUST persistir uma URL concreta utilizável para o banner de perfil e remover o arquivo recém-criado quando a atualização do perfil for rejeitada.

#### Scenario: Banner update succeeds

- **WHEN** uma imagem válida é enviada pelo proprietário e o perfil é atualizado
- **THEN** o banner permanece disponível no armazenamento e o perfil recebe uma URL concreta

#### Scenario: Profile update rejects banner

- **WHEN** a atualização do perfil falha após gravar o novo arquivo
- **THEN** o arquivo recém-criado é removido sem apagar imagens anteriores

