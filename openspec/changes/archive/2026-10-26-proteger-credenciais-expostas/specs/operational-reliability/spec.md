## ADDED Requirements

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
