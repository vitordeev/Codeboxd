## ADDED Requirements

### Requirement: Confirmed idempotent follow actions
O sistema SHALL normalizar IDs e confirmar o estado real da conexão sem criar
duplicatas. Erros SHALL ser apresentados sem alterar o estado confirmado.

#### Scenario: Repeated follow and refollow
- **WHEN** a pessoa segue, repete seguir, deixa de seguir e segue novamente um perfil válido
- **THEN** cada ação SHALL retornar o estado atual e existir no máximo uma conexão

#### Scenario: Rejected or obsolete action
- **WHEN** uma requisição falha ou a conta muda durante o envio
- **THEN** a interface SHALL preservar o estado confirmado e não aplicar resultado de outra conta
