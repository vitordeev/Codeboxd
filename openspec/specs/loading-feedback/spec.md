# loading-feedback Specification

## Purpose

Informar operações em andamento de maneira contextual, acessível e consistente, sem simular progresso ou bloquear o uso desnecessariamente.

## Requirements

### Requirement: Feedback contextual durante espera

O sistema SHALL indicar a operação em andamento enquanto sua flag existente estiver ativa e encerrar o feedback quando ela terminar. MUST preservar mensagens de erro, ações de repetição e conteúdo já disponível, sem percentuais fictícios ou overlay global.

#### Scenario: Conteúdo inicial pendente
- **WHEN** uma seção aguarda dados e não possui conteúdo para mostrar
- **THEN** apresenta texto específico e placeholders não interativos com dimensões reservadas

#### Scenario: Atualização e conclusão
- **WHEN** uma seção com conteúdo existente é atualizada e termina em sucesso ou falha
- **THEN** mantém o conteúdo conforme sua política funcional e mostra status inline durante a espera, substituído pelo resultado ou erro ao terminar

### Requirement: Carregamento acessível

O feedback SHALL ser anunciado como status educado com texto legível; placeholders MUST ser decorativos. Animações MUST parar quando houver preferência por movimento reduzido.

#### Scenario: Movimento reduzido
- **WHEN** a pessoa prefere movimento reduzido
- **THEN** o texto de status continua visível e compreensível sem depender de animação
