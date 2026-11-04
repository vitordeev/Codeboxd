# Validação — upload de imagem no feed

Data: 29/10/2026. Validação local no branch `develop`; sem alteração de branch,
publicação Xano, uso de conta real ou reinício da instância normal.

## Implementação local

- O seletor `post_image_upload` chama `stage_post_image` pelo evento `on_drop`;
  não há mais botão intermediário “Carregar imagem”.
- O formulário desabilita publicar enquanto há arquivo selecionado no browser.
  Após o staging bem-sucedido, o nome selecionado é limpo e o preview local
  continua visível; falhas mantêm a seleção bloqueando envio parcial e permitem
  descartá-la.
- A publicação mantém o POST multipart existente com `image_upload`, texto,
  obra e spoiler. O endpoint Xano não foi alterado.

## Verificações executadas

- `.venv/Scripts/python.exe -B -m unittest tests.test_feed_list_workflows tests.test_feed_navigation_performance -v` — 22 testes aprovados.
- Regressões focadas de picker, staging e multipart — 3 testes aprovados.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -q` — 434 testes aprovados.
- `.venv/Scripts/python.exe -B -m reflex compile --dry` — compilação aprovada em 4,135 s.
- `openspec validate corrigir-upload-imagem-feed --type change` — change válida.
- `git diff --check` — sem erros; Git avisou somente sobre conversão futura de LF para CRLF nos arquivos já modificados.

A suíte registrou `NORMAL_RESTORE_BLOCKED: network unavailable`; terminou com
código 0. Nenhum servidor normal foi reiniciado.

## Limites

Não foi executado cenário em navegador real nem upload autenticado contra Xano.
Os testes comprovam o vínculo de evento Reflex gerado, o estado local e o
payload multipart simulado; não comprovam armazenamento ou entrega da imagem no
serviço remoto. A validação visual e remota permanece pendente.
