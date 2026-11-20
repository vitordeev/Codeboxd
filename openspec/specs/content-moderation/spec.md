# content-moderation Specification

## Purpose

Permite revisar reports de mensagens e outros conteúdos do Codeboxd em uma fila rastreável, preservando o conteúdo reportado e registrando as decisões da moderação.

## Requirements

### Requirement: Registrar reports de conteúdo
O sistema MUST permitir registrar um report com o tipo e identificador do conteúdo alvo, a categoria do motivo, a descrição escrita obrigatória, a pessoa denunciante e uma cópia contextual suficiente para análise. O fluxo MUST aceitar mensagens como tipo de conteúdo reportável sem exigir que esta mudança crie um sistema de mensagens.

Atualização solicitada em 20/10/2026 pela change exigir-texto-denuncias-avaliacoes:
texto vazio ou composto apenas por espaços é inválido. Evidências anteriores
que tratavam descrição como opcional são históricas.

#### Scenario: Report válido recebido
- **WHEN** um report válido é enviado sobre uma mensagem, publicação, comentário, perfil ou outro tipo de conteúdo suportado
- **THEN** o sistema registra o report como pendente e preserva os dados necessários para revisá-lo

#### Scenario: Report sem alvo ou motivo válido
- **WHEN** um report não contém um alvo identificável ou um motivo aceito
- **THEN** o sistema rejeita o registro e informa o que precisa ser corrigido

#### Scenario: Report sem descrição escrita
- **WHEN** a descrição está ausente, vazia ou contém apenas espaços
- **THEN** o sistema rejeita o envio sem criar um report e pede detalhes escritos

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
