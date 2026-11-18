## Purpose

Define safe, reviewable acceptance of integrations against the existing shared Xano workspace without requiring a separate environment.

## Requirements

### Requirement: Validação sem workspace adicional
A estratégia de aceite MUST permitir testes locais e verificações controladas no workspace existente sem provisionar sandbox, workspace, fonte de dados ou plano adicional. O destino compartilhado MUST ser identificado explicitamente.

#### Scenario: Ambiente adicional indisponível
- **WHEN** o usuário informa que não consegue criar outro ambiente
- **THEN** o planejamento MUST usar testes locais, leitura/prévia e lotes limitados no destino existente, mantendo os critérios reais de aceite

### Requirement: Lote mutável limitado a fixtures comprovadas
Um plano de alteração de dados MUST vincular origem HTTPS canônica, workspace, branch, fonte, grupo e execução a um baseline completo, recibos de criação, identidades e snapshots de fixtures e ações exatas. Registros anteriores ao lote ou com identidade/snapshot divergentes MUST ser recusados. Nome com prefixo de teste sozinho MUST NOT comprovar propriedade.

#### Scenario: Registro preexistente tem marcador de teste
- **WHEN** um ID já aparece no baseline anterior ao provisionamento
- **THEN** o plano MUST rejeitar sua alteração ou limpeza mesmo que tenha marcador da execução

#### Scenario: Destino ou fixture mudou
- **WHEN** o destino, identidade, snapshot, payload ou conjunto de ações diverge da prévia aprovada
- **THEN** a validação MUST recusar o lote antes de qualquer execução

### Requirement: Aprovação do lote não é aprovação de estratégia
O planejamento MUST distinguir decisão de usar o destino atual da aprovação de um lote mutável concreto. A prévia MUST ter hash, prazo e limite de operações. A ferramenta de planejamento MUST produzir somente metadados sanitizados e MUST NOT executar requisições, importar ambiente ou publicar contratos.

#### Scenario: Decisão de reformular o ambiente
- **WHEN** o usuário autoriza a estratégia no workspace atual
- **THEN** a ferramenta MUST continuar exigindo aprovação vinculada ao hash de um futuro lote para considerá-lo revisado, sem tratar a decisão como execução autorizada

### Requirement: Cenários de falha ficam locais e integração preserva critérios
Falhas induzidas, 429, resets, concorrência agressiva, escalonamento de privilégio e ações destrutivas amplas MUST ser exercitados localmente. Aceite de persistência, privacidade, autoria e entrega real MUST continuar exigindo evidência remota controlada quando aplicável.

#### Scenario: Falta evidência de execução real
- **WHEN** apenas testes simulados ou dry-run passaram
- **THEN** o requisito funcional remoto MUST continuar aberto, sem exigir outro ambiente como única forma de executá-lo

### Requirement: Limpeza e operações fora do escopo
Limpeza MUST listar somente IDs criados na execução e revalidar referências/snapshot antes de cada ação. O planejador MUST recusar mudanças de papel, senhas, envio de mensagens, resets, truncamentos e exclusões administrativas amplas. Auditoria MUST permanecer preservada.

#### Scenario: Operação contra conta real ou arquivo legado
- **WHEN** o plano tenta remover uma conta preexistente, alterar privilégio ou destruir asset sem recibo próprio
- **THEN** a validação MUST rejeitar o plano e manter o critério pendente para tratamento específico
