## Why

Existe uma pendência registrada de sobreposição entre capa e sinopse de livro
em 390px. A capa absoluta ocupa a mesma área do texto no layout móvel atual.

## What Changes

- Colocar capa e texto em fluxo vertical nas fichas até 640px.
- Preservar a composição desktop e a leitura integral de textos longos.
- Verificar a geometria real no navegador com capas e títulos de quatro tipos.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `media-catalog`: apresentação legível da capa e da sinopse no celular.

## Impact

CSS de `assets/codeboxd.css`; nenhuma alteração em endpoints ou dados.
Evidências em OpenSpec. Sem Docker ou dependência adicional.
