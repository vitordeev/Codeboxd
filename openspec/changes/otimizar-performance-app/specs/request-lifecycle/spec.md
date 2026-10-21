# Request lifecycle

## Purpose

Definir o uso eficiente de requisições e dados temporários durante a navegação,
preservando isolamento, consistência e recuperação dos limites dos serviços.

## ADDED Requirements

### Requirement: Reuse equivalent safe reads
O sistema SHALL reutilizar leituras equivalentes ainda válidas dentro do escopo de cache definido, sem compartilhar dados privados entre sessões ou credenciais.

#### Scenario: Repeated navigation
- **WHEN** uma navegação repete a mesma leitura dentro de sua validade
- **THEN** o sistema SHALL reutilizar o resultado sem nova chamada desnecessária
- **AND** consultas e páginas distintas SHALL manter resultados independentes

#### Scenario: Account change
- **WHEN** o usuário sai ou troca de conta
- **THEN** o sistema SHALL impedir acesso aos dados privados em cache da conta anterior

#### Scenario: Short navigation identity reuse
- **WHEN** um membro navega em modo de leitura até 15 segundos após verificar sua identidade com o mesmo token e sessão
- **THEN** o sistema SHALL reutilizar essa identidade sem repetir a consulta de validação
- **AND** mudanças externas da conta SHALL ser verificadas novamente ao expirar esse prazo

### Requirement: Invalidate stale reads after mutations
O sistema SHALL invalidar leituras afetadas por gravações e SHALL NOT armazenar erros como respostas bem-sucedidas.

#### Scenario: Saved change
- **WHEN** uma alteração é confirmada e sua informação é consultada novamente
- **THEN** o sistema SHALL apresentar a informação confirmada sem restaurar a versão anterior do cache

#### Scenario: Failed read
- **WHEN** uma consulta falha temporariamente
- **THEN** uma nova tentativa permitida SHALL consultar o serviço em vez de reutilizar a falha como dado válido

### Requirement: Respect service rate limits
O sistema SHALL respeitar Retry-After em HTTP 429 e limitar tentativas ao escopo do limite aplicável, preservando dados e rascunhos durante a espera.

#### Scenario: Active cooldown
- **WHEN** o serviço informa um prazo de nova tentativa
- **THEN** o sistema SHALL informar a espera e impedir repetição da operação limitada antes desse prazo
- **AND** o sistema SHALL permitir recuperação após o prazo sem exigir logout

### Requirement: Prevent duplicate side effects
O sistema SHALL NOT repetir automaticamente operações com efeitos colaterais e SHALL impedir envios duplicados enquanto a mesma operação estiver em andamento.

#### Scenario: Slow submission
- **WHEN** o usuário repete um envio enquanto sua confirmação está pendente
- **THEN** o sistema SHALL manter apenas uma operação em andamento e indicar seu estado

### Requirement: Preserve server authorization
O sistema SHALL manter autorização de ações protegidas no servidor e SHALL NOT usar otimizações para conceder acesso de conta expirada, desativada ou sem permissão.

#### Scenario: Rejected authorization
- **WHEN** o servidor rejeita a sessão ou o acesso com 401 ou 403
- **THEN** o sistema SHALL impedir a ação protegida e invalidar o estado de acesso correspondente

#### Scenario: Navigation cache is not authorization
- **WHEN** uma ação protegida ou acesso administrativo é solicitado durante a validade da identidade de navegação
- **THEN** o sistema SHALL solicitar validação fresca, respeitando cooldown, e SHALL manter autorização no endpoint de destino

### Requirement: Bound collection loading
O sistema SHALL carregar coleções em parcelas adequadas à tela, preservando acesso aos demais resultados e exatidão de totais exigidos pelo domínio.

#### Scenario: Large collection
- **WHEN** os resultados excedem a parcela inicial da tela
- **THEN** o sistema SHALL disponibilizar continuação sem duplicar ou omitir identidades
- **AND** o sistema SHALL NOT apresentar uma parcela como total completo
