## Purpose

Permite revisar reports de mensagens e outros conteúdos do Codeboxd em uma fila rastreável, preservando o conteúdo reportado e registrando as decisões da moderação.

## ADDED Requirements

### Requirement: Registrar reports de conteúdo
O sistema MUST permitir registrar um report com o tipo e identificador do conteúdo alvo, a categoria do motivo, a descrição opcional, a pessoa denunciante e uma cópia contextual suficiente para análise. O fluxo MUST aceitar mensagens como tipo de conteúdo reportável sem exigir que esta mudança crie um sistema de mensagens.

#### Scenario: Report válido recebido
- **WHEN** um report válido é enviado sobre uma mensagem, publicação, comentário, perfil ou outro tipo de conteúdo suportado
- **THEN** o sistema registra o report como pendente e preserva os dados necessários para revisá-lo

#### Scenario: Report sem alvo ou motivo válido
- **WHEN** um report não contém um alvo identificável ou um motivo aceito
- **THEN** o sistema rejeita o registro e informa o que precisa ser corrigido

### Requirement: Fila de moderação protegida
O sistema MUST permitir que somente administradores consultem reports e o conteúdo contextual associado. A fila MUST oferecer filtro por status, tipo e motivo.

#### Scenario: Administradora consulta a fila
- **WHEN** uma administradora abre os reports e aplica filtros
- **THEN** o sistema apresenta reports correspondentes, seu status e contexto autorizado

#### Scenario: Membro tenta acessar reports
- **WHEN** uma pessoa sem papel administrativo solicita a fila ou detalhes de um report
- **THEN** o backend rejeita a solicitação sem revelar reports ou conteúdo reportado

### Requirement: Atualizar o estado de um report
O sistema MUST suportar os estados pendente, em análise, resolvido e rejeitado. Somente uma administradora autorizada pode alterar o estado.

#### Scenario: Report colocado em análise
- **WHEN** uma administradora inicia a análise de um report pendente
- **THEN** o sistema altera seu estado para em análise

#### Scenario: Report resolvido ou rejeitado
- **WHEN** uma administradora conclui a revisão e registra uma decisão
- **THEN** o sistema atualiza o estado para resolvido ou rejeitado e registra a decisão

### Requirement: Auditar decisões de moderação
O sistema MUST preservar o status anterior e o novo, a decisão, a pessoa responsável e o horário para cada mudança de estado de um report.

#### Scenario: Estado do report alterado
- **WHEN** uma administradora atualiza o estado ou decisão de um report
- **THEN** o sistema mantém um histórico auditável da alteração

### Requirement: Denúncia não remove conteúdo automaticamente
O sistema MUST manter o conteúdo reportado intacto até que uma ação autorizada de moderação seja executada separadamente.

#### Scenario: Novo report recebido
- **WHEN** um report é criado
- **THEN** o sistema registra a denúncia sem excluir, ocultar ou editar automaticamente o conteúdo alvo
