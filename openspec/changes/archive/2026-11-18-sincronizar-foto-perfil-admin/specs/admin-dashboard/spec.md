## MODIFIED Requirements

### Requirement: Identificacao compacta da pessoa administradora
As paginas administrativas MUST apresentar um controle de avatar circular para a sessao administrativa validada. Ao ativa-lo, o controle MUST mostrar o nome de exibicao, o nome de usuario e o cargo da sessao atual. A identidade e o cargo MUST vir de dados verificados pelo servidor, e a interface MUST oferecer fallback legivel quando nao houver avatar ou perfil completo. Sempre que o menu de identidade for aberto, o painel MUST atualizar esses dados do perfil atual, incluindo a foto, sem reutilizar uma resposta antiga da mesma sessao.

#### Scenario: Administradora abre os dados da propria sessao
- **WHEN** uma administradora autenticada ativa seu avatar no cabecalho
- **THEN** o painel mostra o nome, o nome de usuario e o cargo administrativo associados a sessao atual

#### Scenario: Foto de perfil atualizada no site
- **WHEN** a administradora salva uma nova foto no perfil do site e abre novamente o menu administrativo
- **THEN** o painel busca o perfil atual e mostra a nova foto sem exigir novo login

#### Scenario: Perfil sem foto ou dados complementares
- **WHEN** a sessao administrativa nao possui foto ou algum dado opcional de perfil
- **THEN** o cabecalho mostra um fallback visual e usa somente os dados disponiveis da sessao sem bloquear a navegacao

#### Scenario: Pessoa sem acesso administrativo tenta obter a identidade administrativa
- **WHEN** uma pessoa visitante ou membro solicita os dados destinados ao cabecalho administrativo
- **THEN** o backend rejeita a solicitacao sem revelar dados administrativos
