# operational-reliability Specification

## Purpose

Garantir operação reproduzível do Codeboxd, preservar imagens enviadas e evitar o compartilhamento acidental de arquivos privados e dados gerados.

## Requirements

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

### Requirement: Safe credential exposure inventory

O projeto MUST manter inventário da exposição identificada com categoria, localização, consumidor, prioridade e situação, sem publicar valores secretos ou dados pessoais. Limitações de acesso ao histórico e aos provedores MUST ser explícitas.

#### Scenario: Secret is found in available history

- **WHEN** uma credencial é identificada no histórico disponível
- **THEN** o inventário registra a ocorrência e os consumidores sem reproduzir o valor
- **AND** distingue exposição confirmada de itens ainda não verificados

### Requirement: Verifiable credential revocation

Credenciais expostas MUST ter substituição e revogação verificadas no serviço responsável antes de serem consideradas resolvidas. Senhas e sessões de contas afetadas MUST ser tratadas conforme os mecanismos de invalidação disponíveis.

#### Scenario: Replacement is activated

- **WHEN** uma credencial exposta é substituída
- **THEN** o consumidor autorizado funciona com a nova configuração e há evidência da revogação da anterior
- **AND** testes não executados permanecem pendentes

#### Scenario: Account password was exposed

- **WHEN** uma conta de teste tem senha exposta
- **THEN** a senha é substituída e a validade das sessões anteriores é verificada e tratada
- **AND** qualquer limitação de invalidação permanece registrada como pendência

### Requirement: Prevent credential reintroduction

O projeto MUST oferecer verificação reproduzível dos arquivos destinados ao versionamento para detectar segredos e arquivos privados conhecidos, sem imprimir seus valores. Exemplos de configuração MUST usar placeholders sem credenciais utilizáveis.

#### Scenario: Staged content contains a known secret pattern

- **WHEN** a verificação encontra um segredo sintético em conteúdo destinado ao versionamento
- **THEN** informa a localização sem o valor e retorna falha

#### Scenario: Configuration contains only public settings and placeholders

- **WHEN** a verificação examina configuração pública e placeholders aprovados
- **THEN** não os classifica automaticamente como credenciais expostas
