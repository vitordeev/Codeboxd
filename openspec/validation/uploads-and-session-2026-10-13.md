# Uploads e sessão — P.3/P.5 — 13/10/2026

Rodada autorizada pelo usuário para configurar pendências do projeto. Acompanhamento
transversal, sem reabrir ou alterar o histórico das changes arquivadas.

## Defeito encontrado no navegador

O estágio de imagem concluía, mas o editor do feed fechava e a prévia não ficava
visível. A revalidação temporariamente indisponível de `/auth/me` mantinha a
identidade/cache em SessionState, enquanto SocialState limpava os dados pessoais
por `not valid`. `_require_user` continuava pelo fallback da sessão, gravando a
imagem depois de apagar o rascunho. O Xano apresentou HTTP 429 nesta rodada.

Correção implementada: preservar o rascunho quando a validação falhar temporariamente
sem trocar/limpar a identidade; continuar limpando dados e arquivos temporários
quando a identidade mudar ou a sessão for invalidada. Escritas continuam sujeitas
à autorização remota. Os critérios de browser e limpeza foram conferidos na
rodada final abaixo, sem ampliar os checkboxes administrativos.

Implementação local: condição de limpeza agora distingue identidade trocada ou
invalidada de falha transitória com identidade mantida. O teste de HTTP 429 falhou
antes da correção e passou depois; outro teste confirma limpeza após HTTP 401.
Fechar o editor chama `cancel_post`, descartando apenas o arquivo temporário do
rascunho e preservando imagens existentes. A suíte ganhou uma regressão para esse
cancelamento. A primeira reexecução do browser com a correção de sessão confirmou
prévia visível e remoção da imagem. A rodada final conferiu gravação/recarga/edição.

## Contrato multipart rejeitado

POST real retornou HTTP 400, `ERROR_CODE_INPUT_ERROR`, parâmetro `image.path`.
O tipo `image` recebe metadados, enquanto o multipart leva arquivo bruto.
Correção local em POST/PUT de posts: entrada opcional `file image_upload`,
convertida por `storage.create_image` somente depois da autorização e validação
do alvo/mídia. Entrada `image` existente preservada para compatibilidade; edição
sem nova imagem mantém a anterior. O Python passa o arquivo em `image_upload`.

Referência: [armazenamento Xano](https://docs.xano.com/xanoscript/function-reference/file-storage).
O preview posterior, com o tipo `file` confirmado na extensão oficial Xano,
mostrou somente dois endpoints alterados. O push publicou ambos, sem modificar
tabela ou importar registros. Dry-run final dos doze documentos (admin + posts):
**No changes to push**. A tentativa intermediária com `file_resource` foi bloqueada
no dry-run e não chegou a ser publicada.

## Resultado final — rodada encerrada em 14/10/2026

Os arquivos de resultados mantêm 13/10 no nome porque a rodada começou nessa
data. O commit de backup foi criado às 23h42 de 13/10; o encerramento documental
ocorreu em 14/10. Históricos anteriores não foram sobrescritos.

- 120 testes locais passaram e a aplicação Reflex compilou após as correções.
- [Browser](../changes/gerenciamento-website/validation/browser-after-publication-2026-10-13.json):
  15 cenários passaram, zero exceções JavaScript; Edge headless em execução local
  de produção. Inclui visitante/membro, login em 1440/390, imagem inválida,
  prévia/remoção, criação, recarga, edição preservando imagem, exclusão e cancelamento.
- A fixture PNG mínima anterior foi rejeitada pelo processador de imagens Xano;
  a execução válida usou `assets/default-movie-cover.png`. Isso não é evidência de
  defeito para esse PNG válido. [Diagnóstico intermediário](post-upload-transport-after-2026-10-13.json).
- A carga rápida de ações provocou HTTP 429 na exclusão; a rodada final respeitou
  o limite com pausas de 20 segundos antes de gravar/editar/excluir.
- Posts temporários foram excluídos pela UI e conferidos pela API. Os dois blobs
  de imagens dos testes também foram removidos pela Metadata API, depois de
  conferir IDs/nomes exatos e ausência posterior: [primeiro](post-file-cleanup-first-2026-10-13.json)
  e [último](post-file-cleanup-final-2026-10-13.json). Nenhum arquivo existente de
  usuário foi removido.
- `uploaded_files/` terminou com os dois banners originais, sem imagens staged
  dos testes. O servidor local de validação foi encerrado.
- P.5 concluída para os cenários desta rodada. Não comprova integração completa
  da administração nem entrega de e-mail; P.6/admin continuam pendentes.

[Runner preservado](post_image_browser_probe.py) com porta/conta/resultado por
argumentos, recusa de sobrescrita de resultado e screenshots privados em uma nova
pasta `.local`. As adaptações de argumentos passaram em `py_compile`; o browser
executado foi a versão de teste da rodada antes dessas adaptações. Para uma nova
execução, iniciar o servidor, usar conta controlada e novo nome de resultado.
O runner limpa posts; blobs de teste exigem limpeza específica pelo operador,
como a conferida nesta rodada. Não executar sobre uma conta sem autorização.

## Backup local verificado

`tools/backup_uploads.py` criou `.local/backups/uploads-before-admin-2026-10-13.zip`
com dois arquivos (86.516 bytes originais), preservando as fontes. CRC e hashes
SHA-256 foram conferidos após escrever o arquivo. Backup:
`c310d4da3a2c639d120a2b923313cc2312ce0c69d2acb71dc96e989ff2e1096d`.

Essa cópia local no mesmo disco protege contra alterações acidentais; uma cópia
externa para falha/perda do disco e persistência de hospedagem continuam pendentes.
