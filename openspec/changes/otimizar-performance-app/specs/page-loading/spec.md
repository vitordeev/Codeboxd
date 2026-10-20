# Page loading

## Purpose

Definir uma navegação responsiva e verificável em todas as jornadas do Codeboxd,
com conteúdo progressivo e estados consistentes durante esperas e falhas.

## ADDED Requirements

### Requirement: Render primary content independently
O sistema SHALL disponibilizar conteúdo principal assim que suas dependências estiverem prontas, sem aguardar dados complementares independentes.

#### Scenario: Slow optional section
- **WHEN** uma seção complementar está lenta e o conteúdo principal já está disponível
- **THEN** o sistema SHALL permitir uso do conteúdo principal e indicar espera apenas na seção pendente

### Requirement: Keep navigation results current
O sistema SHALL aplicar resultados somente à rota, consulta, conta e obra que originaram a operação e que ainda correspondem à tela ativa.

#### Scenario: Fast navigation between works
- **WHEN** uma resposta da obra anterior chega depois de o usuário abrir outra obra
- **THEN** o sistema SHALL ignorar essa resposta na ficha atual e preservar a identidade da avaliação

### Requirement: Communicate pending and failed actions
O sistema SHALL apresentar estado visível durante carregamento ou gravação, preservar entrada recuperável em falhas transitórias e distinguir sucesso, vazio e erro.

#### Scenario: Temporary save failure
- **WHEN** uma gravação falha por indisponibilidade ou limite temporário
- **THEN** o sistema SHALL preservar o rascunho e informar como tentar novamente sem indicar sucesso

#### Scenario: Partial page failure
- **WHEN** uma seção falha e outra carrega corretamente
- **THEN** o sistema SHALL manter a seção disponível utilizável e identificar a seção com falha

### Requirement: Meet approved journey performance budgets
O sistema SHALL atender aos orçamentos de tempo e requisições aprovados por jornada, com comparações reproduzíveis de cache vazio e aquecido em desktop e celular.

#### Scenario: Journey acceptance
- **WHEN** uma jornada otimizada é candidata a conclusão
- **THEN** a validação SHALL comparar medidas anteriores e posteriores contra as metas aprovadas
- **AND** a jornada SHALL permanecer pendente se não houver evidência ou se a meta não for atendida
