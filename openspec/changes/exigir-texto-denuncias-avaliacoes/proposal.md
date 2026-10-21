## Why

Denúncias e avaliações aceitam texto vazio, permitindo envios sem contexto.
O usuário solicitou impedir esses envios, inclusive conteúdo formado só por espaços.

## What Changes

- Exigir detalhes escritos em toda denúncia e texto em toda submissão do formulário de avaliação.
- Rejeitar texto ausente, vazio ou composto apenas por espaços antes de autenticar/persistir.
- Preparar proteção equivalente no Xano: descrição de report obrigatória e nota positiva exige review.
- Preservar ações de organização sem nota, como Quero ver/Já assisti, que não são submissões de avaliação.
- **BREAKING**: denúncias sem descrição e avaliações somente com nota deixam de ser aceitas.

## Capabilities

### New Capabilities

- `submission-content-validation`: conteúdo escrito obrigatório e validação consistente de denúncias/avaliações.

### Modified Capabilities

Nenhuma alteração silenciosa de specs arquivadas; o requisito transversal novo
complementa media-interactions e substitui a descrição opcional da proposta administrativa ativa.

## Impact

Páginas/estado social, POST reports e PUT interactions no Xano, testes e documentação.
Sem migração ou exclusão de registros antigos, dependências novas ou Docker.
Publicação Xano e validação remota serão registradas separadamente do resultado local.
