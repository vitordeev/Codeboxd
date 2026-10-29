## Why

Ao escolher uma foto no formulário do feed e publicar sem acionar a etapa
separada de carregamento, o post é salvo com o texto e a obra associada, mas sem
a foto. A imagem selecionada deve acompanhar a publicação sem exigir uma ação
intermediária que permita esse envio incompleto.

## What Changes

- Iniciar o envio da imagem selecionada pelo próprio seletor do formulário.
- Manter validação de formato e tamanho, preview, remoção e preservação do
  rascunho quando o envio falhar.
- Impedir que a publicação seja enviada como sucesso enquanto uma imagem
  selecionada ainda não estiver pronta para ser anexada.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `social-feed`: uma foto escolhida para publicação deve ser incluída no post
  sem uma etapa manual separada de carregamento.

## Impact

Afeta o seletor de imagem e o estado de publicação em `Codeboxd_main/pages/social.py`
e `Codeboxd_main/state/social.py`, testes locais do feed e esta documentação
OpenSpec. Usa o endpoint multipart existente; não requer alteração de contrato
Xano, dependência, migração ou publicação remota.
