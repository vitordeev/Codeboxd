## ADDED Requirements

### Requirement: Feed independent of own publishing
O feed SHALL consultar posts dos seguidos independentemente de publicação ou
registro prévio de timeline do leitor. Falha SHALL ser distinguida de vazio.

#### Scenario: New reader follows an author
- **WHEN** uma conta sem posts segue um perfil que tem posts e abre o feed
- **THEN** os posts existentes do perfil SHALL aparecer imediatamente

#### Scenario: Feed request failure
- **WHEN** a consulta do feed falha
- **THEN** a interface SHALL apresentar erro e opção de tentar novamente em vez de afirmar ausência de conteúdo

#### Scenario: Ancillary read failure
- **WHEN** posts dos seguidos foram recebidos e a consulta opcional de posts próprios ou likes falha transitoriamente
- **THEN** os posts recebidos SHALL permanecer disponíveis com aviso da falha parcial
