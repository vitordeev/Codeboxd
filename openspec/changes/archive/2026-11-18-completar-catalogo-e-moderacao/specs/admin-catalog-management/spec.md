## ADDED Requirements

### Requirement: Excluir logicamente obra removida por moderacao
Uma obra removida por decisao administrativa MUST deixar de aparecer no catalogo publico e MUST deixar de aceitar novas interacoes/listas. A remocao MUST preservar o registro, as referencias historicas de usuarios, o report e sua auditoria; a area administrativa MUST identificar a obra como removida.

#### Scenario: Obra reportada e removida
- **WHEN** uma administradora confirma a remocao da obra vinculada a um report
- **THEN** a obra desaparece de buscas e selecoes publicas, referencias historicas permanecem consistentes e o report continua consultavel

#### Scenario: Usuario tenta criar nova referencia a obra removida
- **WHEN** uma pessoa tenta avaliar, listar ou vincular uma obra removida
- **THEN** o backend rejeita a nova referencia sem apagar dados historicos existentes
