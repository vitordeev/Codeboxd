## Why

Sinopses de animes Kitsu e livros Open Library chegam em outros idiomas. O usuário
escolheu integrar DeepL API Free e forneceu credencial para a configuração local.

## What Changes

- Traduzir descrições das fichas de anime/livro para português brasileiro no servidor.
- Reaproveitar traduções em cache persistente por conteúdo e idioma de destino.
- Preservar o original para português detectado, ausência de chave ou falhas.
- Manter TMDB em pt-BR, sem chamadas adicionais de tradução para filmes/séries.

## Capabilities

### New Capabilities
- `description-translation`: tradução opcional de sinopses com cache e fallback.

### Modified Capabilities
Nenhuma.

## Impact

Serviços Python de catálogo e tradução, testes, `.env.example` e configuração
privada `.env`. Sem nova dependência, migração Xano ou Docker. Não traduz títulos,
reviews, posts ou o catálogo inteiro em lote. Validação remota será limitada.
