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

### Requirement: Persistência e ciclo de vida
Publicação com imagem externa MUST guardar URL e identificador/provedor vinculados ao autor, preservar leitura de imagens legadas e controlar limpeza na remoção/substituição sem apagar asset arbitrário.

#### Scenario: Exibição de post
- **WHEN** o feed contém imagem externa ou legada
- **THEN** a imagem correspondente é exibida pela URL compatível sem reprocessar o arquivo externo no Xano

#### Scenario: Falha após upload
- **WHEN** o upload foi concluído e a gravação do post falha
- **THEN** o sistema preserva rascunho e reconcilia o asset, sem apagar imagem possivelmente vinculada após falha de resultado incerto
