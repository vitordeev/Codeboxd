## Purpose

Oferecer descrições de obras em português brasileiro preservando disponibilidade,
identidade dos registros e privacidade das credenciais do provedor de tradução.

## ADDED Requirements

### Requirement: Tradução de descrições nas fichas
O sistema MUST traduzir descrições não vazias de animes e livros para PT-BR quando
o serviço estiver configurado, sem alterar título, identidade ou outros metadados.

#### Scenario: Descrição estrangeira
- **WHEN** a ficha de anime ou livro recebe uma descrição e o provedor responde
- **THEN** a descrição em português brasileiro é apresentada na ficha

#### Scenario: Português ou conteúdo vazio
- **WHEN** o provedor detecta português ou a descrição está vazia
- **THEN** o texto original é preservado e texto vazio não gera chamada

### Requirement: Reutilização persistente
O sistema MUST reutilizar traduções bem-sucedidas do mesmo conteúdo e destino,
inclusive após reinício, e solicitar nova tradução se o conteúdo mudar.

#### Scenario: Reabertura da ficha
- **WHEN** a mesma descrição possui tradução no cache persistente
- **THEN** a tradução é reutilizada sem nova chamada ao provedor

### Requirement: Disponibilidade e credenciais
O sistema MUST manter o original quando faltar chave, ocorrer erro ou esgotar
cota; MUST manter a chave somente no servidor e fora de logs e respostas.

#### Scenario: Serviço indisponível
- **WHEN** a tradução falha por rede, HTTP, formato, cache ou limite
- **THEN** a ficha continua disponível com a descrição original sem expor a chave

#### Scenario: Português do TMDB
- **WHEN** uma ficha de filme ou série é carregada pelo TMDB em pt-BR
- **THEN** nenhuma tradução adicional é solicitada
