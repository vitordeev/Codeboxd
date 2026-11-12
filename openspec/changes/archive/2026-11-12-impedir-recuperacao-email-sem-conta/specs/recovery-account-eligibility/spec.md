## Purpose

Impedir que solicitações para endereços sem conta ativa avancem à confirmação de código e evitar que erros de envio sejam apresentados como sucesso.

## ADDED Requirements

### Requirement: Conta ativa para solicitar código
O backend MUST rejeitar solicitação de recuperação para endereço sem conta ativa antes de gerar ou enviar código. A interface MUST permanecer na etapa de e-mail, preservar o endereço informado e orientar sua correção.

#### Scenario: Endereço sem cadastro ou conta inativa
- **WHEN** a solicitação usa endereço sem conta ativa
- **THEN** o backend retorna 404 sem gerar código ou chamar provedor e a interface não mostra os campos de código/senha

#### Scenario: Conta ativa aceita
- **WHEN** a solicitação de conta ativa é aceita
- **THEN** a interface avança para código e senha, preservando o e-mail

### Requirement: Falha de envio não significa sucesso
A interface MUST apresentar falhas de envio como erro e não avançar a partir da primeira etapa quando o backend rejeita a solicitação.

#### Scenario: Provedor rejeita envio
- **WHEN** a solicitação retorna erro 400
- **THEN** a interface mostra falha de envio e não declara sucesso nem avança da etapa inicial
