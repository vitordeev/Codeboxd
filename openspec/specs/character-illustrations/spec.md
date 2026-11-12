# character-illustrations Specification

## Purpose

Evoluir os robôs ilustrativos do Codeboxd para uma família original coerente, preservando a identidade do aplicativo e a legibilidade das mensagens.

## Requirements

### Requirement: Família original consistente

As oito cenas SHALL compartilhar cinco papéis de cor, formas simples, contorno único de 2px, proporções e detalhe de assinatura do personagem, com sombra plana a 10–15%. MUST evitar gradientes, brilhos e anatomia detalhada e funcionar nos temas claro e escuro em 360px/1440px.

#### Scenario: Revisão do conjunto
- **WHEN** onboarding, vazio, 404, 500, sucesso, carregando, offline e sem resultados são apresentados lado a lado
- **THEN** pertencem à mesma família visual e cada cena comunica uma ideia com no máximo dois objetos de apoio

### Requirement: Apresentação acessível e leve

As cenas SHALL reservar espaço e manter mensagem e ação independentes da imagem. SVGs MUST ter menos de 30 KB; imagens decorativas MUST ser ocultadas e informativas MUST possuir nome acessível.

#### Scenario: Imagem indisponível
- **WHEN** uma imagem não pode ser apresentada
- **THEN** a mensagem e a ação continuam disponíveis sem deslocar conteúdo
