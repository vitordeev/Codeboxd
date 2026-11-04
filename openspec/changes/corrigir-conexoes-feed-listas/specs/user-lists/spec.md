## ADDED Requirements

### Requirement: Exclusive default media lists
O sistema SHALL manter cada obra em Assistido, Quero assistir ou nenhuma das
duas listas padrão. Listas personalizadas SHALL preservar seu comportamento.
Os controles superiores e a lista SHALL refletir o mesmo estado confirmado.

#### Scenario: Switch between defaults
- **WHEN** uma obra em Quero assistir é marcada Assistido, ou vice-versa
- **THEN** ela SHALL sair da anterior e aparecer apenas na nova lista

#### Scenario: Click the active state
- **WHEN** o usuário clica no estado já ativo
- **THEN** a obra SHALL sair das duas listas padrão sem apagar avaliações

#### Scenario: Error or late response
- **WHEN** a gravação falha ou a obra/conta muda durante o envio
- **THEN** a interface SHALL exibir a falha aplicável e não confirmar estado especulativo ou de outra obra

#### Scenario: Legacy conflict
- **WHEN** uma obra aparece nas duas listas durante a migração
- **THEN** a limpeza SHALL preservar Assistido e remover o conflito
