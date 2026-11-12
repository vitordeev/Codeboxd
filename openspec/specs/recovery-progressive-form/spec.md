# recovery-progressive-form Specification

## Purpose

Simplificar a recuperação de acesso mostrando somente os campos da etapa atual e preservando o e-mail informado ao longo da jornada.

## Requirements

### Requirement: Formulário progressivo
A página MUST mostrar inicialmente somente o campo de e-mail. Após solicitação aceita, MUST mostrar código, nova senha e confirmação, reutilizando o e-mail anterior sem exigir nova digitação.

#### Scenario: Solicitar código
- **WHEN** a solicitação de código recebe resposta genérica aceita
- **THEN** a página mostra a etapa de código e senha, mantendo o endereço informado

#### Scenario: Alterar endereço ou reenviar
- **WHEN** a pessoa escolhe trocar e-mail ou reenviar código
- **THEN** ela retorna à etapa de e-mail sem requisição ou solicita reenvio para o endereço mantido, respectivamente

#### Scenario: Conclusão
- **WHEN** a troca de senha é confirmada
- **THEN** os formulários dão lugar à confirmação e à ação de entrar, sem permitir novo envio do código consumido

#### Scenario: Falha
- **WHEN** o envio ou a validação falha
- **THEN** a etapa corrente apresenta feedback acessível e permite correção sem perder o endereço

#### Scenario: Endereço sem conta ativa
- **WHEN** a solicitação é rejeitada por ausência de conta ativa
- **THEN** a página permanece ou retorna à etapa de e-mail com o endereço mantido e mensagem de correção, conforme decisão posterior da change impedir-recuperacao-email-sem-conta
