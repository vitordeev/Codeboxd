## Why

A marca nas referências locais é um cubo com código à esquerda e reprodução à direita. O ícone inline atual é uma aproximação incompleta; o usuário pediu analisar as imagens e aplicar a logo ao projeto, mantendo o design antigo restaurado.

## What Changes

- Reproduzir em SVG o símbolo observado em `Imagens/HomePage.png` e `Imagens/MoviePage.png`, pois não há arquivo isolado da logo nessas pastas.
- Usar o mesmo asset em todos os cabeçalhos que já compartilham `_logo_icon` e no ícone da aba.
- Preservar os textos da marca, tamanhos dos cabeçalhos, paleta existente, mascotes e jornadas.
- Registrar referência e limites da reprodução vetorial; não retomar o redesign cancelado.

## Capabilities

### New Capabilities

- `brand-logo`: identificação consistente do Codeboxd com o símbolo das referências locais, em interface e aba do navegador.

### Modified Capabilities

Nenhuma.

## Impact

`assets/codeboxd-logo.svg`, helper compartilhado e head em `Codeboxd_main/pages/login.py`, seletores de tamanho em `assets/codeboxd.css`. Sem novas dependências, backend, rotas ou publicação. Assets locais continuam conforme documentação Reflex. A reprodução vetorial não é o arquivo-fonte original do autor.
