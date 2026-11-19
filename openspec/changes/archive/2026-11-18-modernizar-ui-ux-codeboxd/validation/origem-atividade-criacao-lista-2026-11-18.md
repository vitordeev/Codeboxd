# Origem da atividade de criação de listas — 18/11/2026

## Cenário local autorizado

Com conta e serviços fictícios da fixture, a interface criou uma lista própria
em `/listas`. O registro foi aceito pela chamada `POST /lists`; a fixture não
recebeu `POST /posts`, e retornar ao feed preservou exatamente o post inicial,
sem publicação adicional. O cenário passou em 1440 e 390 px.

## Conferência dos contratos locais

- `xano/api/codeboxd/lists_POST.xs` cria/garante uma linha `user_list`; não
  insere em `post` nem registra atividade de feed.
- `xano/api/codeboxd/feed_GET.xs` lê registros da tabela `post` para quem a
  conta segue.
- A revisão é de arquivos locais e fixture; não houve leitura ou escrita de
  conta real, nem publicação no Xano.

## Recomendação

Não adicionar autopost nem remover eventos/handlers sem reprodução do relato
numa conta autorizada. Se voltar a ocorrer, registrar rota, autor e hora e
comparar a sequência de chamadas daquele caso antes de propor mudança.

## Validação

`tools.feed_lists_browser`: **10/10 cenários** em 1440/390 px, zero erros
JavaScript. A fixture foi limpa ao terminar o processo local.
