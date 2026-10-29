## 1. Layout do post

- [x] 1.1 Mover o card da obra para a faixa do autor e manter foto pessoal, texto e interações na ordem atual; conferir no renderer que há um único card e que ele mantém o link `/obra/<id>`.
- [x] 1.2 Aplicar compactação e quebra responsiva ao cabeçalho; revisar no componente a quebra de linha, o limite do título e a permanência do link.

## 2. Revisão

- [x] 2.1 Revisar o diff, executar `reflex compile --dry` e `openspec validate reposicionar-card-obra-feed --type change`; registrar que nenhuma API, payload ou dado de post foi alterado.
