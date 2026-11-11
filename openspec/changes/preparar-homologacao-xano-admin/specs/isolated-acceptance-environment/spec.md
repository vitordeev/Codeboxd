## Purpose

Disponibilizar preparação verificável de backend isolado para homologação do
Codeboxd, preservando o ambiente compartilhado e seus dados.

## ADDED Requirements

### Requirement: Destino de homologação identificado
O ambiente MUST ter identidade e configuração próprias verificadas antes de
publicar contratos ou criar dados de teste. Destino ausente, ambíguo ou igual
ao ambiente protegido MUST bloquear operações. Rodar frontend local não prova
isolamento do backend.

#### Scenario: Destino corresponde ao ambiente protegido
- **WHEN** a configuração de homologação aponta ao mesmo backend e workspace da origem
- **THEN** a preparação rejeita a configuração sem publicar ou modificar dados

#### Scenario: Recurso isolado indisponível
- **WHEN** o provedor recusa criação ou exige plano não autorizado
- **THEN** a tarefa registra a limitação e mantém o ambiente atual intacto

### Requirement: Pacote sem dados e efeitos externos
O pacote de homologação MUST conter somente contratos necessários ao aceite
administrativo, sem registros, variáveis privadas, credenciais, tarefas
automáticas, remetentes ou integrações de envio. Identidades externas de API
MUST ser geradas para o destino, sem reaproveitar canonical/GUID da origem.

#### Scenario: Preparar contratos aprovados
- **WHEN** o pacote é gerado dos arquivos locais permitidos
- **THEN** um manifesto identifica arquivos, contagens e hashes, sem dados privados

#### Scenario: Documento contém configuração ou efeitos proibidos
- **WHEN** a preparação detecta registros, env, envio externo ou documento não permitido
- **THEN** rejeita o pacote antes da publicação

### Requirement: Ativação por prévia verificável
Publicação MUST usar prévia de delta limitada ao destino isolado identificado,
sem importar registros/env, sem exclusão ou truncamento. Ambiente existente
não vazio MUST exigir decisão própria antes de qualquer mudança. Preparação
local, publicação e aceite remoto MUST ter evidências distintas.

#### Scenario: Sandbox já possui conteúdo
- **WHEN** a descoberta encontra sandbox pessoal com dados ou contratos existentes
- **THEN** preserva o conteúdo e não executa reset, sincronização destrutiva ou sobrescrita

#### Scenario: Backend vazio foi publicado
- **WHEN** contratos passam na prévia e a publicação autorizada é executada no destino
- **THEN** verifica estrutura, ausência de dados copiados e configuração separada antes do piloto
