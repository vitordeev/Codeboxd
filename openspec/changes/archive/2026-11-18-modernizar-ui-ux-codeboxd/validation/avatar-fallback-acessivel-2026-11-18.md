# Avatar alternativo acessível — 18/11/2026

## Mudança

O componente compartilhado `avatar()` apresentava apenas um ícone quando a foto
estava ausente, sem nome acessível. O fallback agora expõe o nome como imagem
semântica e marca o ícone como decorativo. O caminho com foto mantém o `alt`
existente. Nenhuma chamada, estado ou contrato de backend foi alterado.

## Validação local

- `python -B -m unittest tests.test_social_ui_components`: **8 testes aprovados**,
  incluindo regressão para nome acessível do fallback e ícone oculto.
- `python -B -m reflex compile --dry`: **compilação aprovada** em 19,732 s.
- Teste em navegador/leitor de tela não executado nesta rodada. Portanto, a tarefa
  2.2 permanece aberta para foco/retorno, colagem e demais estados previstos.
