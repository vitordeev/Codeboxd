# Preparação Cloudinary — 10/11/2026

## Entrega desta rodada

- `.venv/Scripts/python.exe` disponível; `pip check` retornou “No broken requirements found”. httpx/python-dotenv já existentes; nenhuma dependência instalada ou requisito alterado.
- Criadas somente variáveis ausentes no `.env` privado: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET e CLOUDINARY_UPLOADS_ENABLED=false. Verificações booleanas confirmaram campos presentes e flag false; nenhum valor secreto impresso. Exemplos vazios em .env.example.
- Adaptador server-side `services/cloudinary_uploads.py` pronto: assinatura SHA-256 dos campos ordenados, public_id exclusivo por proprietário, overwrite=false, arquivo multipart, limite 5MB e tipos aceitos, timeout sem retry/redirect e erros sanitizados. Configuração desativada/incompleta falha antes da rede. Representação da configuração oculta key/secret; retorno limitado aos metadados validados de asset e URL HTTPS da conta Cloudinary esperada.
- Adaptador não é chamado por SocialState nesta rodada. Fluxo atual de publicação não alterado. Sem esquema/endpoints Xano publicados ou uploads reais.

## Verificações

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_cloudinary_uploads.py -q`: 7 testes passaram, com transporte HTTP simulado. Cobertura de assinatura/transporte sem envio do secret, configuração ausente/desativada, proprietário/tamanho/tipo inválidos, falha de rede, erros do provedor sem retry, JSON inválido e URLs/metadados não confiáveis.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_uploads.py -q`: 4 regressões do transporte atual passaram.
- `git check-ignore .env`: `.env`, confirmando exclusão do arquivo privado.
- `openspec validate hospedar-imagens-publicacoes-cloudinary --type change` e `git diff --check`: aprovados.
- `.venv/Scripts/python.exe -B tools/check_staged_secrets.py`: aprovado, mas **zero arquivos no índice**. Não há validação dos arquivos ainda não adicionados nem dos commits anteriores; executar novamente após preparar o commit. `git status --short` mostrou modificações e arquivos novos sem staging; nenhum commit/push realizado pelo agente.

## Pendências e limites

Conta/credenciais ainda em criação. Não comprovado upload Cloudinary, recebimento/exclusão de asset, feed sem marca ou contrato Xano para URL/IDs. Tarefas 2.1/2.2 abertas: detalhar/publicar contrato aditivo após backup/prévia e integrar criação/edição/exclusão/compensação, preservar imagens legadas e fazer ensaio real com limpeza antes da ativação.

Assinatura e API conferidas na [documentação oficial](https://cloudinary.com/documentation/authentication_signatures). Configuração do usuário em [setup.md](setup.md). Execução local continua com .venv, sem Docker. Nenhum envio de mensagem, conta remota criada ou dado externo modificado nesta preparação.

# Continuação local — 18/11/2026

## Correção de idempotência

Na sub-branch `task/cloudinary-post-images-continuacao-20261118`, a resposta de
uma reserva já anexada passou a incluir a versão Cloudinary confirmada. O cliente
agora reutiliza essa reserva ao repetir criação ou substituição, em vez de
prosseguir sem `image_reservation_id` ou iniciar outro upload.

Arquivos alterados:

- `Codeboxd_main/services/post_image_reservations.py`
- `Codeboxd_main/state/social.py`
- `xano/api/codeboxd/post_image_uploads_POST.xs`
- `xano/api/codeboxd/post_image_uploads_id_GET.xs`
- testes focados de reserva e fluxo

## Evidência executada

- 57 testes Cloudinary/reserva/fluxo/contratos: aprovados.
- Suíte completa: 726 testes aprovados.
- `python -m reflex compile --dry`: aplicativo compilado com sucesso.
- `python -m pip check`: nenhuma dependência quebrada.
- `openspec validate hospedar-imagens-publicacoes-cloudinary --type change`: aprovado.
- `git diff --check`: aprovado.

## Limites desta continuação

Esta rodada não enviou arquivos ao Cloudinary, não publicou contratos no Xano,
não ativou flags e não alterou posts ou registros reais. Os checkboxes remotos
2.1.2, 2.1.4–2.1.7 e 2.1.9/2.2.x permanecem abertos até haver evidência integrada
com contas, concorrência e navegador controlados.

## Prévia supervisionada de limpeza — 18/11/2026

- Implementado `Codeboxd_main/services/post_image_cleanup.py`.
- A prévia valida dono, cloud, namespace do asset, estado `cleanup_pending`,
  retenção já vencida, ausência de referências e limite máximo de dez itens.
- A implementação não chama Cloudinary, não executa `destroy` e não altera Xano.
- 60 testes direcionados aprovados após incluir estrangeiro, duplicata,
  referência ativa, retenção futura, estado divergente e limite excedido.
- Nenhuma exclusão física foi preparada além de objetos locais em memória.

## Alinhamento de leitura de reserva — 18/11/2026

- O endpoint Xano `post_image_uploads/{id}` agora projeta `version` no resultado.
- A versão anexada pode ser reconciliada sem repetir o upload ou consumir outra
  escrita externa.
- Validação adicionada ao teste estrutural da reserva.

## Reconciliação de commit incerto — 18/11/2026

- `SocialState.save_post` consulta a reserva conhecida após timeout/erro transitório
  do commit e nunca deduz sucesso apenas da ausência de resposta.
- O editor só é limpo quando a mesma chave de operação volta com estado
  `attached`; rascunho e arquivo permanecem em estado incerto ou divergente.
- O código não consulta reservas alheias nem repete o upload durante a leitura.
- Testes locais cobrem timeout pendente e timeout confirmado como anexado.

## Persistência de sessão da reserva — 18/11/2026

- O ID da reserva e a chave da operação são mantidos em `SessionStorage`.
- Nenhum arquivo, secret, token do Cloudinary ou URL arbitrária é persistida nesse
  armazenamento.
- Uma operação pendente só é considerada no mesmo contexto de sessão; trocar de
  conta ou editor ainda exige reabertura e rejeita contexto divergente.

## Guardas da prévia de limpeza — reforço local

- IDs de asset e referências agora exigem inteiro positivo ou contador inteiro;
  valores booleanos são rejeitados.
- Candidatos duplicados continuam bloqueados.
- Nenhuma operação destrutiva foi adicionada ou executada.
