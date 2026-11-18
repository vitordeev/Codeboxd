# Navegação do shell e diálogos — 18/11/2026

## Shell

- Harness `tools.feed_lists_browser` com backend local fictício passou **8/8
  cenários** em 1440 e 390 px, sem erros JavaScript.
- Cada cenário confirmou as rotas principais Início, Buscar, Feed e Biblioteca;
  menu Conta abre por Enter, expõe Meu perfil por Tab e navega por Enter.
- Foco visível permaneceu dentro da largura da viewport. Abrir o menu não
  alterou o contador de chamadas da fixture.
- O mapa atual→novo e a preservação dos atalhos/rotas estão descritos em
  `design.md`.

## Diálogos

- A mesma matriz verificou foco dentro do diálogo de edição, Ctrl+A/Ctrl+V no
  campo e retorno ao acionador depois de salvar.
- Sem erros JavaScript; chamadas são somente contra fixture local. Nenhum dado,
  conta ou endpoint Xano real foi usado.

## Limite

É validação em Chromium headless com viewports emulados, não teste em leitor de
tela, navegador físico ou aparelho touch. A evidência não substitui as tarefas
3.2 e 7.1 de hardware/matriz WCAG.
