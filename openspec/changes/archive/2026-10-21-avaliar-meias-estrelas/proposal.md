## Why

O usuário quer avaliar em meias estrelas, incluindo 0,5 e 1,5. O contrato Xano já
aceita decimais em passos de 0,5, mas os botões e a restauração de visitante só
aceitam inteiros e o formulário não interpreta vírgula decimal.

## What Changes

- Selecionar metade ou estrela inteira e visualizar preenchimento parcial.
- Oferecer valores 0,5–5 com rótulos em português; zero remove a nota.
- Normalizar vírgula/ponto e preservar notas decimais em conta e navegador.
- Trocar nota sem remontar o formulário e perder uma crítica em edição.

## Capabilities

### New Capabilities
Nenhuma.

### Modified Capabilities
- `media-interactions`: escala de meia estrela, exibição parcial e restauração.

## Impact

Estado social, ficha compartilhada, CSS e testes. Sem alteração do modelo Xano,
traduções, provedores de catálogo ou uso de Docker. Validação remota controlada.
