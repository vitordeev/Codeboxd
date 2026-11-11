## Purpose

Hospedar anexos de publicações fora do processamento de imagens do Xano, mantendo autoria, URLs de exibição e identificação segura dos arquivos externos.

## ADDED Requirements

### Requirement: Upload externo privado
Upload de anexo MUST usar assinatura privada no servidor e validar configuração antes de chamar o provedor. Arquivo MUST respeitar limite de 5MB e tipo permitido; credenciais e erro bruto do provedor não podem chegar ao frontend.

#### Scenario: Configuração ainda indisponível
- **WHEN** a integração está desativada ou incompleta
- **THEN** o adaptador rejeita a operação sem chamada externa

#### Scenario: Upload válido
- **WHEN** usuário autenticado envia anexo válido pela integração habilitada
- **THEN** a hospedagem retorna URL HTTPS e identificadores de asset próprios para persistência no post

#### Scenario: Recibo ou URL inconsistentes
- **WHEN** a resposta não tem assinatura válida para public_id/versão ou sua URL aponta a outro asset/versão
- **THEN** o adaptador rejeita a resposta com erro sanitizado, sem autorizar persistência ou exclusão

#### Scenario: Recibo pertence a outro autor
- **WHEN** a preparação de metadados recebe identidade de asset fora do namespace do autor
- **THEN** rejeita o payload antes da gravação, sem substituir a validação independente de autoria no backend

### Requirement: Persistência e ciclo de vida
Publicação com imagem externa MUST guardar URL e identificador/provedor vinculados ao autor, preservar leitura de imagens legadas e controlar limpeza na remoção/substituição sem apagar asset arbitrário.

#### Scenario: Exibição de post
- **WHEN** o feed contém imagem externa ou legada
- **THEN** a imagem correspondente é exibida pela URL compatível sem reprocessar o arquivo externo no Xano

#### Scenario: Falha após upload
- **WHEN** o upload foi concluído e a gravação do post falha
- **THEN** o sistema preserva rascunho e reconcilia o asset, sem apagar imagem possivelmente vinculada após falha de resultado incerto

### Requirement: Reserva recuperável de upload
O sistema MUST registrar uma identidade durável e exclusiva de upload vinculada ao usuário autenticado e à operação antes do envio. Perda de conexão, recarga ou reinício MUST permitir reconciliar o resultado sem perder essa referência.

#### Scenario: Interrupção durante o envio
- **WHEN** a conexão cai depois de iniciar o upload
- **THEN** a reserva MUST continuar consultável pelo dono autorizado, distinguindo pendência de sucesso e sem repetir envio ou excluir arquivo automaticamente

#### Scenario: Consulta de reserva alheia
- **WHEN** outra conta ou visitante tenta consultar uma reserva
- **THEN** o sistema MUST negar acesso aos dados da reserva e do arquivo

### Requirement: Associação autorizada no servidor
O backend MUST verificar sessão atual, conta ativa, autoria do post, propriedade da reserva e identidade/versão do recurso antes de associar uma imagem. Metadados do frontend ou assinatura isolada MUST NOT substituir essas verificações.

#### Scenario: Associação arbitrária de imagem
- **WHEN** um cliente chama diretamente a API com arquivo de outro dono, reserva consumida em outro post ou versão incompatível
- **THEN** o servidor MUST recusar a associação sem alterar o post ou excluir o arquivo

#### Scenario: Metadados não cobertos pelo recibo
- **WHEN** URL, formato, tamanho ou asset_id recebidos divergem do recurso confirmado
- **THEN** o backend MUST rejeitar os dados e usar somente metadados verificados do provedor configurado

#### Scenario: Sessão inválida ou conta desativada
- **WHEN** um usuário tenta reservar ou confirmar imagem com sessão inválida, expirada, de recuperação ou conta desativada
- **THEN** o servidor MUST recusar a escrita, preservando dados históricos

### Requirement: Persistência idempotente e concorrência
A confirmação de imagem e seu vínculo ao post MUST ser atômicos. Repetir a mesma operação confirmada MUST retornar o resultado existente, sem duplicar post ou vínculo. Substituição e remoção MUST verificar a revisão esperada da imagem.

#### Scenario: Resposta perdida após commit
- **WHEN** o servidor gravou o post mas o cliente perdeu a resposta
- **THEN** a reconciliação ou repetição identificada da mesma operação MUST recuperar o mesmo post, sem novo upload ou duplicação

#### Scenario: Duas substituições concorrentes
- **WHEN** duas operações tentam substituir a imagem com a mesma revisão esperada
- **THEN** somente uma MUST confirmar essa revisão e a outra MUST informar conflito sem destruir o asset vencedor ou a imagem anterior ainda referenciada

### Requirement: Publicação sem imagem e edição preservadora
Criar publicação sem imagem MUST continuar funcionando sem Cloudinary. Editar somente texto ou obra associada MUST preservar a imagem existente quando não houver ação explícita sobre ela. Imagem externa e campos legados contraditórios MUST ser recusados, sem escolha silenciosa.

#### Scenario: Serviço externo indisponível sem anexo
- **WHEN** o usuário cria post sem imagem enquanto o Cloudinary está desativado ou indisponível
- **THEN** o sistema MUST manter o fluxo sem imagem e não realizar upload externo

#### Scenario: Edição sem nova imagem
- **WHEN** o dono salva somente texto, spoiler ou obra associada
- **THEN** o post MUST conservar sua identidade e imagem sem reenviar ou excluir o asset

#### Scenario: Campos de imagem contraditórios
- **WHEN** uma requisição tenta manter e substituir a imagem simultaneamente ou mistura formatos incompatíveis
- **THEN** o servidor MUST rejeitar a entrada sem modificar o vínculo existente

### Requirement: Leitura compatível e rollback
O sistema MUST exibir imagens legadas e externas válidas sem migrar ou reprocessar destrutivamente arquivos antigos. Desativar novos uploads MUST preservar leitura das imagens externas já publicadas. Leituras públicas MUST NOT expor credenciais, assinaturas ou journal operacional.

#### Scenario: Feed com formatos mistos
- **WHEN** um feed ou perfil contém posts sem imagem, com imagem antiga e com imagem externa confirmada
- **THEN** cada post MUST renderizar sua imagem aplicável ou ausência dela, mantendo texto, obra, autoria e interações

#### Scenario: Desativação da integração
- **WHEN** o operador desativa novos uploads após haver posts externos persistidos
- **THEN** essas imagens MUST continuar recuperáveis sem apagar metadados, arquivos ou pendências de reconciliação

### Requirement: Substituição e remoção explícitas
O dono MUST poder substituir ou remover a imagem de um post por ação explícita e autorizada. A imagem anterior MUST permanecer associada até confirmar a alteração; somente após desvinculação confirmada ela pode ser candidata à limpeza.

#### Scenario: Falha ao substituir
- **WHEN** o novo upload falha ou a persistência não foi confirmada
- **THEN** a imagem antiga MUST permanecer intacta e o sistema MUST preservar rascunho e referências para reconciliar a nova tentativa

#### Scenario: Remover somente a imagem
- **WHEN** o dono confirma remoção da imagem e a revisão é válida
- **THEN** o post MUST continuar disponível sem esse anexo e sem exclusão de texto, obra, comentários ou likes

#### Scenario: Exclusão da publicação
- **WHEN** o dono confirma exclusão do post
- **THEN** o sistema MUST preservar a referência operacional do asset para limpeza após confirmar a remoção, sem apagar previamente o arquivo ou afetar posts alheios

### Requirement: Resultados incertos e falhas parciais
Timeout, 5xx e resposta incompleta MUST ser distinguidos de sucesso ou ausência comprovada. O sistema MUST preservar rascunho e reconciliar a operação exata antes de compensar ou reenviar; falha externa MUST NOT acionar fallback silencioso para outro storage quando a integração estiver habilitada.

#### Scenario: Upload sem resposta verificável
- **WHEN** o envio termina em timeout ou resposta sem recibo válido
- **THEN** o sistema MUST informar pendência/falha e reconciliar a identidade reservada, sem afirmar que o arquivo não existe

#### Scenario: Persistência Xano incerta
- **WHEN** uma gravação retorna timeout ou erro após possível commit
- **THEN** o sistema MUST verificar reserva e post antes de permitir compensação, sem apagar imagem possivelmente vinculada

#### Scenario: Mudança de editor ou conta
- **WHEN** uma resposta chega após o usuário mudar de conta ou abrir outro editor
- **THEN** ela MUST NOT salvar, limpar ou substituir dados no contexto novo

### Requirement: Limpeza supervisionada e retenção
A limpeza MUST exigir prévia aprovada e revalidar dono, propriedade no provedor, escopo, estado, retenção e ausência de referências antes de cada exclusão. Idade ou URL isoladas MUST NOT autorizar remoção. Estado incerto e asset referenciado MUST bloquear limpeza.

#### Scenario: Órfão confirmado elegível
- **WHEN** um asset próprio não referenciado cumpre a retenção aprovada e aparece em lote autorizado
- **THEN** o executor MUST revalidá-lo, excluir somente sua identidade confirmada e registrar o resultado sem segredos

#### Scenario: Referência reaparece após prévia
- **WHEN** o asset passa a ser referenciado ou seu estado/propriedade muda antes da execução
- **THEN** a limpeza MUST recusar esse item, preservando o arquivo e registrando a divergência

#### Scenario: Asset legado ou arbitrário
- **WHEN** um candidato é imagem antiga do Xano, URL arbitrária ou recurso fora da propriedade autorizada
- **THEN** o executor MUST rejeitar a exclusão sem acessar esse recurso como alvo destrutivo

#### Scenario: Limpeza com resultado incerto
- **WHEN** o provedor não confirma exclusão ou há timeout
- **THEN** a pendência MUST permanecer recuperável sem declarar sucesso ou repetir exclusão cegamente

### Requirement: Ativação controlada e cotas
Novos uploads MUST permanecer desativados até contrato, configuração, ensaio integrado e autorização de ativação estarem verificados. O sistema MUST respeitar tamanho, cotas e limites de requisições e sanitizar erros sem vazar credenciais.

#### Scenario: Contrato indisponível
- **WHEN** há credenciais locais mas o backend não oferece o contrato externo compatível
- **THEN** o caminho de upload externo MUST permanecer bloqueado e não consumir recursos por ativação parcial

#### Scenario: Limite de serviço ou arquivo
- **WHEN** o arquivo excede 5 MiB ou o serviço recusa por cota/limitação
- **THEN** o sistema MUST informar a restrição, preservar rascunho e não repetir escrita automaticamente nem contratar plano
