## Purpose

Entregar códigos de recuperação por e-mail usando SendGrid com configuração privada, preservando os controles e respostas de recuperação existentes.

## ADDED Requirements

### Requirement: Envio privado pelo SendGrid
O backend MUST usar chave privada e remetente configurado para enviar o código ao endereço da conta ativa pelo SendGrid. Credenciais e códigos MUST permanecer fora do frontend, logs e respostas públicas.

#### Scenario: Envio aceito
- **WHEN** o SendGrid responde HTTP 202 ao envio do código
- **THEN** a solicitação mantém sua resposta genérica de sucesso, mesmo com corpo vazio do provedor

#### Scenario: Configuração ausente ou envio rejeitado
- **WHEN** falta chave/remetente ou o provedor rejeita ou interrompe a chamada
- **THEN** o backend apresenta erro sanitizado sem revelar a resposta do provedor ou repetir o envio automaticamente

#### Scenario: Conta inelegível ou cooldown
- **WHEN** a geração existente não emite um código
- **THEN** o backend não chama o SendGrid e preserva as regras de elegibilidade/cooldown vigentes, incluindo HTTP 404 para conta ausente/inativa

#### Scenario: Remetente individual verificado
- **WHEN** o projeto utiliza uma caixa individual verificada no SendGrid e não dispõe de domínio próprio
- **THEN** a integração MUST usar somente o remetente configurado e tratar a aceitação ou rejeição do provedor sem exigir aquisição de domínio nem prometer prazo de entrega
