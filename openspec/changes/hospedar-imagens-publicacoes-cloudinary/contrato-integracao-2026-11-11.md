# Contrato candidato de imagens em posts — 11/11/2026

## Estado e escopo

Continuação local autorizada pelo usuário após o ensaio isolado. Não publicado,
não ligado a SocialState e não habilitado. Este documento detalha o restante de
2.1; não substitui backup/prévia remotos nem encerra 2.1/2.2. O ensaio anterior
valida o executor isolado, não o adaptador endurecido nesta rodada.

## Incremento implementado

`cloudinary_uploads._read_image` verifica assinatura de resposta Cloudinary sobre
`public_id` e `version` (SHA-1/SHA-256 conforme protocolo), com comparação constante;
rejeita versão ausente/inválida e URL que não seja a original canônica do mesmo
asset, versão e formato. Continua validando host, tipo, tamanho e dimensões.
`CloudinaryImage` passa a carregar versão e assinatura (oculta em repr).

`post_image_payload` revalida recibo/configuração e namespace exato
`codeboxd/posts/u<owner>/<uuid hex de 32 caracteres>`, retornando somente
`image_provider`, `image_public_id`, `image_version`, `image_signature`.
Não retorna URL arbitrária nem asset_id como prova de persistência. O helper é
server-side, não está conectado aos posts e não autoriza escrita ou exclusão.

Fonte primária: [payloads assinados Cloudinary](https://cloudinary.com/documentation/signatures).
A assinatura da resposta cobre public_id/version: não autentica separadamente
asset_id, URL, tamanho ou dono. A associação ao autor exige o prefixo autenticado
e a reserva descrita abaixo. Validar esse recibo no Python não substitui a
validação na API Xano, que também pode ser chamada diretamente.

## Persistência proposta, ainda não implementada

Adicionar à tabela `post` campos opcionais: `image_provider`, `image_public_id`,
`image_version`, `image_url`, `image_asset_record_id`. Campos atuais `image` e
conteúdo/autoria permanecem; nenhuma migração ou limpeza de legado.

Usar registro durável próprio `post_image_asset`: dono, public_id único,
versão, estado, post vinculado, criação/atualização e resultado da reconciliação.
Não guardar credenciais, códigos ou corpo bruto do provedor. Esse registro é
necessário antes do upload: perder a conexão/estado do processo não pode apagar
o único identificador que permite reconciliar um envio incerto.

Sequência candidata de criação/substituição:

1. Xano valida sessão atual, conta ativa, autoria de post existente e entrada;
   reserva uma identidade única vinculada ao usuário e à operação. Python nunca
   aceita owner_id do formulário como identidade autenticada.
2. Adaptador usa exatamente a identidade reservada, overwrite=false. A interface
   preserva rascunho durante falha e impede envio concorrente. É necessário evoluir
   o adaptador para receber reserva validada antes de conectá-lo ao fluxo.
3. API de commit verifica reserva, dono, estado permitido, assinatura e versão.
   Constrói URL do cloud configurado com public_id/versão validados; não aceita
   URL, provider ou campos do asset sem validação. Requer configuração privada
   do verificador no backend, sujeita à autorização de configuração remota.
4. Na mesma transação, grava/vincula post e asset; repetir commit da mesma reserva
   deve devolver o mesmo resultado, sem criar segundo post. Reutilizar em outro
   post/conta deve ser rejeitado. Checar versão esperada do post na substituição
   para não sobrescrever edição concorrente.
5. Imagem anterior fica candidata à limpeza somente após confirmar o novo vínculo.
   Feed prioriza a imagem externa vinculada; se inexistente, usa o legado atual.
   Desligar uploads deve preservar leitura das imagens externas já publicadas.

Nenhum desses endpoints/campos novos existe por consequência deste documento.
Não enviar o payload candidato aos endpoints atuais nem ativar a flag.

## Reconciliação e exclusão propostas

| Situação | Ação requerida |
| --- | --- |
| Upload com timeout/resposta não verificável | Marcar resultado incerto no registro durável; reconciliar public_id exato, sem reenviar ou excluir cegamente |
| Commit com timeout/5xx | Reconsultar reserva/post; não tratar status isolado como prova de que a transação não ocorreu |
| Validação recusada definitivamente antes de commit | Reconciliar registro e referências antes de autorizar limpeza |
| Substituição confirmada | Enfileirar asset anterior próprio, mantendo o novo vínculo |
| Exclusão de post confirmada | Na transação que remove o post, preservar referência de limpeza em registro separado |
| Limpeza | Validar dono, cloud, namespace, identidade, estado e ausência de referências; excluir só public_id do registro confirmado |
| Timeout de limpeza | Manter pendência durável e reconciliar antes de outra tentativa |
| Imagem legada | Nunca excluir no Cloudinary ou interpretar URL legada como instrução de exclusão |

O plano precisa de processamento autenticado de pendências; não presumir suporte
a tarefa agendada no plano Xano. Um executor administrativo supervisionado é
candidato, mas deve ser implementado/testado com recibos e limites próprios antes
de qualquer limpeza. Não usar DELETE HTTP de URL fornecida pelo cliente.

## Matriz mínima do aceite restante

- Membro cria post externo e lê feed após nova sessão; imagem legada permanece.
- Outra conta, visitante e conta desativada não reservam/alteram asset alheio.
- Recibo/versão/namespace/URL adulterados, replay e commit concorrente são rejeitados.
- Falhas entre reserva/upload/commit geram pendências recuperáveis sem perda do
  rascunho, envio duplicado ou exclusão de asset possivelmente referenciado.
- Substituição/exclusão deixam somente candidatos próprios e confirmados à limpeza.
- Rollback da flag interrompe novos uploads sem quebrar posts externos existentes.
- Ensaios locais, publicação real e navegador são evidências distintas.

## Validação desta rodada

18 testes Cloudinary aprovados: 12 do adaptador e seis do executor de ensaio.
Suíte completa: `python -B -m unittest discover -s tests`, **632 testes aprovados
em 25,189 s**; log privado `.local/cloudinary-integration-tests-20261111.log`.
Novas regressões cobrem URL de outro asset/versão/formato/transformação no mesmo
domínio, recibos ausentes/adulterados, SHA-256 válido, dono divergente e objeto
adulterado antes do payload. Não houve upload adicional, chamada Xano, mudança
de segredo, ativação, exclusão ou reinício nesta rodada.
