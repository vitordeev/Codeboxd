## ADDED Requirements

### Requirement: Remover o alvo correto apos revisao de report
Somente uma administradora autorizada MUST poder remover ou ocultar o alvo de um report pendente ou em analise, com confirmacao e justificativa obrigatoria. A remocao MUST corresponder ao tipo do alvo: publicacao (`post`), obra (`media`), comentario (`comment`) ou avaliacao (`review`). A acao MUST preservar o report, seu snapshot e auditoria. Remover comentario MUST afetar somente aquele comentario; remover avaliacao MUST limpar nota, critica e spoiler sem apagar o status da obra na biblioteca. Reports de mensagem e perfil MUST NOT oferecer acao de remocao por este fluxo.

#### Scenario: Publicacao removida durante a moderacao
- **WHEN** a administradora confirma a remocao de uma publicacao reportada e informa a justificativa
- **THEN** a publicacao e seus comentarios e curtidas deixam de ser exibidos, o report permanece com snapshot e decisao, e a auditoria registra a remocao

#### Scenario: Obra removida durante a moderacao
- **WHEN** a administradora confirma a remocao de uma obra reportada e informa a justificativa
- **THEN** a obra e ocultada do catalogo comum sem apagar suas referencias historicas, e o report e a auditoria sao preservados

#### Scenario: Comentario removido durante a moderacao
- **WHEN** a administradora confirma a remocao de um comentario reportado
- **THEN** somente o comentario e removido, a publicacao pai permanece e o report e sua auditoria sao preservados

#### Scenario: Avaliacao removida durante a moderacao
- **WHEN** a administradora confirma a remocao de uma avaliacao reportada
- **THEN** a nota, critica e spoiler sao limpos da avaliacao reportada, o status da obra na biblioteca permanece e o report e sua auditoria sao preservados

#### Scenario: Tipo de report sem acao de remocao
- **WHEN** o report se refere a mensagem ou perfil
- **THEN** o sistema nao permite executar a remocao de publicacao, obra, comentario ou avaliacao por esse report

#### Scenario: Justificativa ausente ou report ja finalizado
- **WHEN** a justificativa esta vazia, o report nao esta pendente/em analise ou o alvo nao corresponde ao tipo esperado
- **THEN** o backend rejeita a remocao sem alterar o alvo nem o report

#### Scenario: Pessoa sem permissao tenta remover alvo
- **WHEN** visitante ou membro solicita a acao de remocao
- **THEN** o backend rejeita a solicitacao sem revelar nem alterar o conteudo
