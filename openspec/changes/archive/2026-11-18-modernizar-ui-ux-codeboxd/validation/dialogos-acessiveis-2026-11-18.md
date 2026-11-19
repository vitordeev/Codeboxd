# Foco e colagem em diálogos — 18/11/2026

## Correção

Os diálogos controlados por estado abriam sem posicionar o foco dentro deles e
não tinham um acionador Radix para receber o foco ao fechar. Um script local
pequeno agora identifica acionadores declarados, foca o primeiro controle do
diálogo ao abrir e devolve foco ao acionador após fechar. O tratamento roda no
navegador e não envia eventos Reflex por apresentar/fechar o diálogo. O editor
de publicação e o editor de lista declaram seus acionadores.

## Validação

- `python -B -m unittest discover -s tests`: **758 testes aprovados**.
- `python -B -m reflex compile --dry`: compilação aprovada.
- `python -B -m py_compile` nos módulos UI e harness: aprovado.
- `tools.feed_lists_browser`, fixture local: **8/8 casos aprovados** em 1440 e
  390 px, zero erros JavaScript. Verificados foco no diálogo, restauração do
  foco ao botão de edição após salvar, Ctrl+A/Ctrl+V no campo e fluxos de lista.
- As chamadas de API da fixture são fictícias e locais; nenhum serviço remoto
  foi acessado ou modificado.

## Limites

O harness usa Chromium headless com fixture, não leitor de tela nem navegador
físico. As falhas de pré-renderização das primeiras execuções foram corrigidas
isolando as leituras do catálogo na fixture; somente a execução final aprovada
é usada como evidência.
