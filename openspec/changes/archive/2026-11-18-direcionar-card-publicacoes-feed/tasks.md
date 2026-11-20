## 1. Atualizar card de publicacoes

- [x] 1.1 Ligar o card a `/feed` e movê-lo para depois dos outros tres indicadores; verificar destino e ordem no markup do dashboard.
- [x] 1.2 Atualizar cobertura automatizada para garantir o link `/feed` e a posicao final do card.

## 2. Validar e registrar

- [x] 2.1 Executar teste direcionado, `reflex compile --dry`, `git diff --check` e `openspec validate direcionar-card-publicacoes-feed --type change`.

## Evidencias locais (2026-11-18)

- O teste de contrato do dashboard confirma os quatro cards na ordem Usuarios, Catalogo, Reports e Publicacoes, e confirma o link `/feed` e a rota registrada.
- Teste direcionado aprovado; compilacao Reflex concluida; validacao OpenSpec e `git diff --check` aprovados.
- Alteracao esta somente na copia de trabalho local; nao foi enviada ao remoto.
