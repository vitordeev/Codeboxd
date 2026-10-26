## Why

O usuário relatou várias listas “Quero ver / ler” e “Já assisti / li” após login. Cada perfil deve possuir uma lista padrão de cada tipo, preservando listas personalizadas e obras salvas. É necessário distinguir registros duplicados no Xano de listas de outros perfis exibidas na interface.

## What Changes

- Diagnosticar registros reais, propriedade e composição da tela de listas, sem mutações remotas nesta investigação.
- Garantir preparação idempotente das duas listas padrão, inclusive sob concorrência, paginação e troca de conta.
- Corrigir a apresentação para distinguir listas próprias e públicas de outros perfis.
- Agrupar descoberta pública por proprietário, com foto e nome clicáveis para o perfil acima das respectivas listas, conforme refinamento solicitado pelo usuário.
- Preparar reconciliação com backup e união das obras, preservando personalizações e visibilidade; executar somente no escopo revisado.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `data-user-lists`: unicidade por proprietário/tipo padrão e reconciliação sem perda de itens.
- `user-lists`: exibição de listas próprias separada da descoberta de listas públicas de outros perfis.

## Impact

Estado e interface de listas, contratos Xano de cadastro/criação/consulta, eventual esquema de identidade padrão, testes e ferramenta de reconciliação. Não repetir o reset destrutivo histórico nem alterar avaliações, catálogo ou contas. Operação local com `.venv`, sem Docker. Diagnóstico e planejamento não significam correção publicada.
