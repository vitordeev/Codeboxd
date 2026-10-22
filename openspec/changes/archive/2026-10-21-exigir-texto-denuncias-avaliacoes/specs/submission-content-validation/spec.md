## Purpose

Exigir conte?do escrito em den?ncias e avalia??es, com rejei??o consistente de texto vazio na interface e na API, preservando a organiza??o da biblioteca sem nota.

## ADDED Requirements

### Requirement: Denúncia com texto obrigatório
O sistema SHALL exigir descrição escrita não vazia depois de remover espaços nas extremidades em toda denúncia, na interface e no backend.

#### Scenario: Descrição ausente ou em branco
- **WHEN** uma denúncia é enviada sem descrição ou contendo apenas espaços
- **THEN** o sistema SHALL rejeitar o envio antes de gravar e manter o formulário aberto com mensagem de correção

#### Scenario: Descrição válida
- **WHEN** uma denúncia inclui motivo, alvo válidos e descrição escrita
- **THEN** o sistema SHALL preservar o texto e permitir o envio sujeito à autorização existente

### Requirement: Avaliação escrita obrigatória
O sistema SHALL exigir texto não vazio depois de trim em toda submissão do formulário de avaliação. A API de interações SHALL rejeitar nota positiva sem review.

#### Scenario: Somente nota ou espaços
- **WHEN** o formulário de avaliação não contém crítica escrita, mesmo que haja nota
- **THEN** o sistema SHALL rejeitar o envio antes de persistir a obra ou a avaliação e manter a entrada recuperável

#### Scenario: Avaliação válida
- **WHEN** o formulário contém crítica escrita e nota válida
- **THEN** o sistema SHALL permitir gravação sujeita à identidade, autoria, envio único e autorização existentes

#### Scenario: Organização sem avaliação
- **WHEN** o usuário usa um atalho de status da biblioteca sem atribuir nota
- **THEN** o sistema SHALL permitir organizar a obra sem exigir uma crítica
