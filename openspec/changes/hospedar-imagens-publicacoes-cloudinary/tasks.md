## 1. Preparação autorizada

**Replanejamento solicitado — somente documentação:** marcos originais 1.1–1.3
concluídos e 2.1/2.2 abertos, preservados. Subtarefas abaixo tornam o esforço
restante explícito; contagem expandida não mede percentual nem nova entrega.
Proposta/design/specs atualizados aguardam aprovação junto à change UI/UX.
Nenhum teste remoto ou implementação foi executado nesta rodada de planejamento.

11/11/2026, continuação local de 2.1: [contrato candidato e endurecimento do recibo](contrato-integracao-2026-11-11.md).
Assinatura/versão/URL verificadas e payload vinculado ao autor implementado no
adaptador; 18 testes Cloudinary e suíte completa de 632 testes aprovados.
Persistência durável, endpoints, integração SocialState e publicação continuam
pendentes; nenhum checkbox funcional adicional concluído. Flag false.

11/11/2026, ensaio real autorizado e executado: [resultado](ensaio-real-2026-11-11.md).
Upload/download/limpeza HTTP 200; bytes idênticos e exclusão confirmada pela API.
Zero chamadas Xano, sem alterar flag ou dados existentes. Mantido 3/5 porque
persistência e ciclo de vida integrados continuam pendentes. A prévia abaixo
registra o estado histórico antes dessa autorização.

11/11/2026, após preenchimento: [conta Free validada por leitura e prévia do ensaio](preflight-cloudinary-2026-11-11.md).
GET /usage HTTP 200, 0/25 créditos e nenhum recurso reportado. Flag false.
Executor opt-in preparado com seis testes simulados aprovados, sem execução
remota. A ausência de credenciais abaixo descreve a rodada anterior.

11/11/2026, continuação: [cotas, alternativa R2 e revisão de configuração](limites-alternativas-2026-11-11.md).
22 testes locais aprovados novamente. Usuário informou preenchimento, mas os
valores não foram localizados nos .env das worktrees; caminho solicitado.
Plano/consumo da conta ainda não consultados. Integração e ativação mantidas abertas.

11/11/2026: [revisão de prontidão e testes](aceite-2026-11-11.md). Credenciais
locais ausentes, flag false e contrato externo de post ainda incompleto.
22 testes locais passaram; nenhum asset real acessado ou alterado. Mantido 3/5.

- [x] 1.1 Preparar variáveis privadas ausentes, exemplos sem valores e flag desativada, verificar presença/ignore sem expor segredos e pip check na .venv.
- [x] 1.2 Implementar adaptador assinado com guardas e erros sanitizados; verificar configuração, assinatura/transporte, limites e respostas com testes simulados sem rede real.
- [x] 1.3 Registrar uso e limites, validar OpenSpec e git diff --check.

Evidências em [validation.md](validation.md), configuração em [setup.md](setup.md). Preparação 3/3 concluída; integração/ativação 2.1/2.2 pendentes.

## 2. Integração e ativação posteriores

Incremento local planejado de 2.1: verificar recibo Cloudinary (assinatura,
versão e URL canônica do mesmo asset), preparar payload vinculado ao autor e
regressões contra URL/assinatura adulterada, dono diferente e identidade inválida.
Documentar contrato futuro e reconciliação; não conectar posts a metadados sem
validação independente no Xano nem marcar 2.1 completo por esse incremento.

Preparação incremental de 2.1/2.2: credenciais agora presentes e GET /usage
autenticado (Free, 0/25 créditos). Preparar executor opt-in de um PNG sintético,
recuperação por HTTPS e exclusão somente do asset criado nessa execução, com
journal privado anterior ao envio e sem retries de escrita. Validar com mocks;
execução remota aguarda autorização específica da prévia. Não conclui 2.1/2.2
nem ativa posts. Evidências: limites-alternativas-2026-11-11.md e
preflight-cloudinary-2026-11-11.md.

- [ ] 2.1 Com credenciais, detalhar e publicar contrato aditivo de URL/asset/provedor no Xano após backup/prévia, integrar criar/editar/excluir e compensação/reconciliação; testar autoria e legados.
- [ ] 2.2 Ativar configuração somente após ensaio real de upload/post/feed/substituição/exclusão e limpeza em conta/asset descartáveis, sem marcas do processamento Xano em imagens novas.

### Desdobramento de 2.1 — contrato, ciclo de vida e publicação

Cada subtarefa inclui testes e evidência no mesmo lote. 2.1 só é concluída após
validar o conjunto; aprovação documental não autoriza seus passos remotos.

- [x] 2.1.1 Preparar localmente campos aditivos de post e registro durável de asset, índices/constraints e retenção do design; verificar fixtures legadas, ausência de cascata do journal e invariantes de propriedade/estado em testes, documentando contratos sem publicar.
- [ ] 2.1.2 Implementar localmente reserva e consulta por operação com sessão atual/conta ativa/autoria; testar visitante, conta desativada, sessão de recuperação, dono divergente, troca de editor/conta e reinício recuperável, registrando recibos sanitizados.
- [x] 2.1.3 Adaptar upload à identidade reservada e implementar verificação independente server-side de assinatura/recurso/versão; testar replay, URL/asset_id/formato adulterados, limite 5 MiB, quota/429 e resposta incompleta, documentando escopo privado do verificador.
- [ ] 2.1.4 Implementar commit idempotente de criação com imagem e criação sem anexo; testar dois commits da mesma reserva, falha entre upload/commit, post sem Cloudinary e reconciliação após timeout/5xx sem duplicar, documentando estados e erros.
- [ ] 2.1.5 Implementar edição preservadora, substituição e remoção explícita de imagem com revisão atômica; testar concorrência, imagem antiga preservada na falha, corpo/obra/spoiler sem reupload e compatibilidade legada, registrando a matriz de comportamentos.
- [ ] 2.1.6 Integrar exclusão do post à fila durável sem destruir antecipadamente arquivos ou journal; testar transação, referências restantes, timeout da remoção e permissões de outra conta, preservando comentários/likes conforme regra existente e documentando limites.
- [x] 2.1.7 Preparar executor supervisionado de reconciliação/prévia/limpeza com carência e limite propostos; testar identidade/propriedade/versão/referências/estado antes da execução, prévia envelhecida, resultado incerto e rejeição de legado/URL arbitrária; manter execução real bloqueada sem aprovação do lote.
- [x] 2.1.8 Conectar localmente staging, salvar/remover e leitura de posts/feed ao contrato externo compatível, mantendo flag false; testar rascunho, invalidação de cache, editor/sessão tardios, rollback de leitura e ausência de fallback silencioso, compilando conforme skill Reflex e documentando a integração local.
- [x] 2.1.9 Com destino disponível e aprovação específica, revisar backup/dry-run exato e configuração privada, publicar somente contratos aprovados no Xano e verificar schema/guards/projeções/legados por leitura independente; registrar IDs e limites sem copiar segredos ou dados reais. Manter aberta se não houver ambiente/autorização.

### Desdobramento de 2.2 — aceite e liberação

- [ ] 2.2.1 Após autorização do cenário e das fixtures, executar API integrada com duas contas controladas nos onze fluxos do design, incluindo falhas/concorrência/retomada e todos os candidatos próprios à limpeza; registrar resultados reais, autoria e retenção, sem inferir entrega por mocks.
- [ ] 2.2.2 Validar no navegador posts mistos/legados e externos, ausência de imagem, edição/substituição/remoção, foco/rascunho e feedback em 390/1440px; verificar imagem recuperada após nova sessão e rollback de uploads, distinguindo frontend, API e CDN.
- [ ] 2.2.3 Revisar cotas e pendências duráveis, confirmar limpeza autorizada/retidos, obter aprovação específica de ativação e aplicar flags somente após critérios completos; testar rollback preservando leitura/journal, revisar diff e validar esta change antes de recomendar conclusão.

## Workflow follow-up

- 17/11/2026 — Reformulação autorizada: 2.1.2, 2.1.4–2.1.6 e 2.1.9/2.2.x podem ser validadas no workspace atual com duas contas/assets descartáveis, lote e limpeza revisados. Falhas induzidas ficam locais; persistência/autoria/privacidade e transação continuam exigindo prova real controlada. [Estratégia e limites](../validar-integracoes-xano-atual/design.md). Nenhuma tarefa funcional foi encerrada por mudar o plano; flags false.

- 17/11/2026 — Implementação solicitada explicitamente. 2.1.1, 2.1.3 e 2.1.8 concluídas localmente; **6/17**. Suíte **718/718**, 43 testes direcionados, compile, pip check e prévia Xano de 13 documentos aprovados. [Evidências e limites](implementacao-2026-11-17.md). Reserva/commit/edição/fila candidatos preparados; 2.1.2 e 2.1.4–2.1.7 continuam abertas pelos critérios ainda não comprovados. Sem publicação, ativação, assets reais ou arquivo. A espera por aprovação abaixo descreve a rodada anterior e foi substituída pelo pedido atual de implementação.

- Aguardar aprovação das duas changes antes de iniciar implementação.
- Não fazer push, merge, sincronização de specs ou arquivamento nesta rodada.
- Manter abertas verificações de Xano/conta/limpeza/navegador sem evidência própria;
  o PNG descartável e os 632 testes anteriores não substituem aceite integrado.

### Retomada em 18/11/2026

A próxima change funcional escolhida foi `hospedar-imagens-publicacoes-cloudinary` (6/17). Revisão da tarefa 2.1.2 confirmou que cliente de reserva e endpoints Xano candidatos já existem. `.\.venv\Scripts\python.exe -m unittest tests.test_post_image_reservations -q` passou em 16 testes locais, com respostas simuladas e verificações estruturais. Isso não prova execução no Xano: visitante, conta desativada, sessão de recuperação, autoria e recuperação após reinício ainda precisam de validação de integração. Nenhuma publicação ou flag foi alterada; 2.1.2 permanece aberta. Próximas etapas locais devem ser registradas com sua evidência antes de fechar qualquer tarefa.
Checagem adicional da retomada: `.\.venv\Scripts\python.exe -m unittest tests.test_post_image_flow -q` passou em 19 testes do fluxo/estado local. Esses testes não substituem as provas de transação, corrida e persistência no banco Xano exigidas por 2.1.4–2.1.6; os checkboxes permanecem abertos.
Verificação de retomada em 18/11: os quatro módulos direcionados somaram 55 testes aprovados; a suíte completa passou com 756 testes; `reflex compile --dry` compilou a aplicação e `pip check` não encontrou dependências quebradas. A prévia `xano workspace push -d xano -w 147717 -b v1 --dry-run --no-guids` não iniciou: CLI encerrou com `uv_os_get_passwd returned ENOMEM`; não houve publicação. Sem prévia atual e sem validação Xano/API ou navegador, as tarefas remotas e 2.1.9/2.2.x ficam abertas; flags permanecem desativadas.
Prévia preparada para publicação supervisionada em 18/11: backup sem ambiente/records com 85 documentos e manifesto SHA-256; bundle filtrado a 13 arquivos teve prévia sem erros críticos: tabela post com campos aditivos, journal post_image_asset, quatro funções e sete endpoints (quatro novos, três atualizados). A prévia geral falhou somente por incluir função Quick Start alheia à change; filtro exato excluiu esse documento. Recibo `xano-contract-preflight-2026-11-18.json` contém hashes do bundle/baseline, destino, escopo e comando com `--no-records --no-env`. Nenhum contrato, dado, segredo/flag foi alterado. 2.1.9 aguarda aprovação específica deste hash antes de publicar.
Execução autorizada em 18/11: o bundle aprovado foi publicado no workspace 147717/branch `v1` em transação, com 13 documentos, sem importar registros/ambiente e sem ativar flags. Pull independente encontrou os 94 documentos e todos os artefatos do bundle; confirmou preservação da imagem legada, projeção completa de posts e dependências `user`, `media` e `Security/require_current_session` apesar dos avisos do CLI filtrado. GET público de capacidades retornou HTTP 200 com uploads desativados; POST sintético sem token retornou 401 e não criou reserva. Recibo `xano-contract-execution-2026-11-18.json`. Os 756 testes locais e validações OpenSpec passaram. Não fechar tarefas: credenciais/config privada não foram importadas, flags seguem false, e ainda faltam cenários autenticados com duas contas, transações/concorrência, upload Cloudinary integrado, limpeza supervisionada e navegador. Progresso permanece 6/17.
### Retomada em 19/11/2026

Confirmação local sem revelar valores: `.env` existe, mas as três variáveis Cloudinary não estão preenchidas neste checkout; `CLOUDINARY_UPLOADS_ENABLED` está false e `CLOUDINARY_POST_IMAGES_CONTRACT_READY` não está definido. Isso não verifica a configuração privada do Xano. O módulo Python está conectado ao fluxo opt-in de publicações; corrigida somente sua docstring desatualizada. Testes direcionados: 61 aprovados (reserva, fluxo, contratos Xano, transporte e probe). `openspec validate hospedar-imagens-publicacoes-cloudinary --type change` aprovado. Nenhum upload, exclusão, publicação, ativação ou teste de navegador foi executado. As 11 tarefas ainda abertas incluem critérios de execução integrada, limpeza supervisionada e navegador; progresso permanece 6/17.

### Preparacao local da limpeza supervisionada - 19/11/2026

Criado `tools/post_image_cleanup_preflight.py` como preflight estritamente somente leitura, ligado a export JSON de candidatos. Exige snapshot recente, lote de ate 10, estado `cleanup_pending`, dono e namespace coerentes, asset/version, zero referencias e retencao vencida; rejeita estados incertos/legados e qualquer campo de URL. Gera hash de lote e referencia de aprovacao, sem chamar Xano/Cloudinary e sem executar exclusao. Sete testes sinteticos passaram. `2.1.7` permanece aberta porque ainda faltam releitura autenticada do journal no Xano, invalidez real de uma previa envelhecida frente ao banco e executor de limpeza aprovado; o plano local nao e prova dessas operacoes.

Continuação local em 19/11/2026: adicionada `validate_execution_approval` ao mesmo preflight. Ela rejeita referência de aprovação divergente, prévia vencida e qualquer diferença entre o lote aprovado e uma nova leitura fornecida pelo chamador; não acessa serviços nem executa limpeza. `.\.venv\Scripts\python.exe -m unittest tests.test_post_image_cleanup_preflight -v` passou em 9 testes sintéticos; `git diff --check` e `openspec validate hospedar-imagens-publicacoes-cloudinary --type change` passaram. Ainda falta ligar a leitura recente a uma rota autenticada/autoritativa do Xano e implementar o executor supervisionado com gravação de resultado. `2.1.7` segue aberta e as flags continuam desligadas.

Revisão de privacidade das leituras em 19/11/2026: `posts_GET` e `feed_GET` retornavam objetos completos, expondo `image_asset_record_id` (referência interna do journal). Ambos agora removem somente esse campo da projeção pública, preservando os demais dados existentes. Regressão com execução das lambdas em Chromium: 9 testes de `tests.test_post_image_backend_contracts` passaram. A correção está apenas local; não foi publicada no Xano. `2.1.9` e o aceite remoto continuam abertos até prévia/publicação autorizada e leitura independente do contrato ativo.

Validação conjunta em 19/11/2026 após a revisão: 71 testes focados passaram (`test_post_image_backend_contracts`, `test_post_image_reservations`, `test_post_image_flow`, `test_cloudinary_uploads`, `test_cloudinary_acceptance_probe`, `test_post_image_cleanup_preflight`); `git diff --check` e validação da change passaram. Leitura pública atual de `/post-image-capabilities` retornou contrato v1, 5 MiB e `uploads_enabled=false`. A leitura não valida a alteração local da projeção, que permanece sem publicação, nem a configuração secreta do Xano.

Atualização relatada pelo usuário em 19/11/2026, a partir do agente do Xano: `POST /auth/login` e `GET /feed` estão no mesmo workspace/branch; login normal gerou token com finalidade `session` e versão atual; chamada autenticada a `/feed` retornou sucesso e omitiu `image_asset_record_id`. O token anterior era de recuperação (`password_reset`) e foi corretamente rejeitado; nenhuma regra de sessão foi alterada. Este registro é evidência fornecida pelo usuário/agente, sem token ou payload real anexado. O endpoint `GET /posts` também foi conferido diretamente nesta sessão e omitiu o campo. Isso cobre a projeção de leitura, não conclui os fluxos de escrita/limpeza, navegador ou ativação.

Preparação de prévia Xano em 19/11/2026: criado localmente `GET /admin/post-image-cleanup-candidates`, com sessão atual, papel admin e conta ativa; lote limitado a dez assets `cleanup_pending` cuja retenção venceu; releitura de contagem de referências por candidato; resposta limitada ao necessário para a prévia. O endpoint não chama Cloudinary e não altera registros. Testes locais de backend/preflight: 19 aprovados; `git diff --check` passou. Ainda não publicado nem validado pelo parser/runtime Xano. O CLI segue indisponível nesta máquina (`uv_os_get_passwd returned ENOMEM`); `2.1.7` permanece aberta e aguarda publicação/verificação no workspace e implementação do executor/registro de resultado.

Atualização relatada pelo usuário em 19/11/2026: agente do Xano criou o endpoint equivalente no grupo Codeboxd e validou a sintaxe XanoScript; ainda aguarda Review/Publish. Nenhuma leitura autenticada no runtime foi registrada. Flags continuam desligadas; `2.1.7` permanece aberta.

Leitura autenticada relatada pelo usuário em 19/11/2026: a rota retornou `contract_version: 1`, `fetched_at` numérico em milissegundos e `[0]` indicando zero candidatos. O preflight local agora aceita timestamps Xano em milissegundos e trata a resposta sem candidatos como `no_candidates` não executável (sem referência de aprovação). Testes preflight/backend: 22 aprovados; diff e validação OpenSpec passaram. Sem candidato elegível não ocorreu limpeza física. Executor e gravação de resultado continuam pendentes.

Continuação local em 19/11/2026: o preflight agora pode buscar a prévia diretamente da rota administrativa usando a variável temporária `CLOUDINARY_CLEANUP_ADMIN_TOKEN` e a opção `--from-xano`, sem imprimir token nem dados de candidatos no resumo. Adaptação de timestamp Xano e modo `no_candidates` permanecem fail-closed. `tests.test_post_image_backend_contracts` + `tests.test_post_image_cleanup_preflight`: 24 testes passaram; diff limpo. A leitura pela ferramenta ainda não foi executada neste ambiente, pois não há sessão admin configurada; não houve escrita ou exclusão. Executor e gravação do resultado permanecem pendentes.

Atualização em 19/11/2026: usuário forneceu as variáveis privadas do Cloudinary; foram gravadas no `.env` local, ignorado pelo Git. A validação confirmou presença das três credenciais sem imprimir valores. `CLOUDINARY_UPLOADS_ENABLED` foi mantida como `false`; nenhum upload ou chamada externa foi executado.

Verificacao Xano em 19/11/2026: GET `/post-image-capabilities` respondeu contrato v1, limite 5 MiB e `uploads_enabled=false`. A leitura confirma que a rota publicada esta ativa e os gates seguem fechados; por desenho, nao revela se os valores privados `CLOUDINARY_API_KEY` e `CLOUDINARY_API_SECRET` estao presentes nem validos. Nenhuma escrita foi feita.

Confirmacao do usuario em 19/11/2026: as chaves privadas do Cloudinary foram conferidas e estao corretas no Xano. Mantida a distincao entre essa confirmacao e uma chamada autenticada de verificacao pelo backend; o endpoint publico de capacidades nao devolve status de credenciais.

Teste autenticado em 19/11/2026: login da conta de validacao fornecida e GET `/auth/me` confirmaram sessao ativa, status `active`, papel `admin`. Com flags desligadas, uma tentativa de reserva com chave aleatoria foi recusada pelo Xano com HTTP 403, antes da criacao de reserva. Nenhuma publicacao ou asset foi criado. Isso confirma autenticacao e gate fechado; nao substitui a matriz integrada com duas contas.

Teste de duas contas em 19/11/2026: ambas autenticaram e `/auth/me` confirmou contas distintas e ativas; a primeira tem papel `admin` e a segunda `member`. Foram somente logins e leituras de sessão; não foram criadas publicações ou imagens. A matriz de propriedade/reserva ainda aguarda a ativação temporária dos gates no Xano.

Atualizacao de configuracao local em 19/11/2026: adicionada `CLOUDINARY_POST_IMAGES_CONTRACT_READY=false` ao `.env` ignorado pelo Git. `CLOUDINARY_UPLOADS_ENABLED` permanece `false`. Isso nao altera as variaveis privadas do Xano; o gate remoto segue sem confirmacao de existencia/configuracao.

Confirmacao do usuario em 19/11/2026: a variavel `CLOUDINARY_POST_IMAGES_CONTRACT_READY` foi adicionada ao ambiente Xano. Seu valor e a presenca das chaves privadas nao podem ser lidos pela rota publica; os gates devem permanecer `false` ate a janela de teste integrado.

Ensaio real Cloudinary em 19/11/2026: PNG sintético enviado, baixado com bytes idênticos e excluído pelo probe isolado; upload/download/destroy retornaram HTTP 200. O probe não chamou Xano e não criou post. A inspeção antes do aceite integrado confirmou que o Xano ainda só enfileira assets (`cleanup_pending`), sem rota/executor para concluir e reconciliar a exclusão no journal. Por isso, nenhum post real de teste foi criado nesta rodada; `2.1.7` e o aceite integrado permanecem abertos.

Rechecagem Xano após o usuário informar desligamento, 19/11/2026: três leituras GET de `/post-image-capabilities` continuaram retornando `uploads_enabled=true`. Portanto, o endpoint ativo ainda não confirmou o desligamento; nenhum teste de escrita foi executado após essa constatação. Conferir as duas flags no workspace/branch atendido por `XANO_SOCIAL_URL` antes de retomar.

Rechecagem apos correcao, 19/11/2026: GET `/post-image-capabilities` retornou `contract_version=1`, `uploads_enabled=false`. O gate remoto voltou a ficar fechado; nenhuma escrita foi feita nesta verificacao.

Ensaio API controlado em 19/11/2026 com duas contas: post sem imagem criado pela conta membro; tentativa de exclusao pela outra conta (admin) recebeu 403; proprietario excluiu o post e consulta posterior nao o encontrou. Relatorio privado sanitizado em `.local/cloudinary-no-image-api-2026-11-19.json`. Nenhum asset Cloudinary criado e nenhuma tarefa 2.1.4/2.1.6 fechada, pois imagem, fila e transacao com journal nao fizeram parte deste caso.

Continuação local da limpeza supervisionada em 19/11/2026: implementados `POST /admin/post-image-cleanup/{id}/claim` e `/result` como contratos Xano locais. Claim exige sessão atual/admin ativo, lock/transação, identidade idêntica à aprovação, retenção vencida e zero referências; muda o journal para `reconciliation_required` antes de qualquer chamada externa. Resultado só marca `deleted` após confirmação; incerteza preserva reconciliação. Adicionado `destroy_cleanup_candidate`, que consulta somente o public_id conhecido, compara cloud/namespace/asset_id/versão/formato/tamanho/dimensões e emite uma chamada assinada Cloudinary sem retry. `tools/post_image_cleanup_executor.py` exige SHA-256 aprovado, releitura autenticada exata, claim por item, e gravação do resultado; claim ambíguo nunca chega ao provedor. Testes com transporte e Xano simulados: 44 passaram nos módulos de upload/destroy, executor, preflight e contratos. Prévia envelhecida, identidade divergente, estado/referências inválidos, legado/URL arbitrária, claim incerto e resultado Cloudinary incerto são cobertos; a execução física permanece bloqueada sem aprovação hash-bound. O usuário publicou os dois endpoints e confirmou que os testes manuais de autenticação/rotas funcionaram. 2.1.7 concluída como preparo supervisionado; nenhum candidato foi destruído porque o Xano retornou lista vazia.

Fechamento de publicação 2.1.9 em 19/11/2026: publicação original dos 13 contratos após backup/prévia exata registrada acima; pull independente confirmou os documentos do bundle. Leituras posteriores verificaram capabilities com uploads desligados, projeções de `/posts` e `/feed` sem `image_asset_record_id`, leitura de candidatos admin e, segundo confirmação do usuário, os endpoints claim/result publicados e acessíveis nos testes seguros. Evidência remota é composta por recibos já registrados e confirmação do usuário; nenhum segredo/token foi incluído. A configuração e flags de upload permanecem fechadas.

Atualização Xano relatada pelo usuário em 19/11/2026: os dois endpoints POST foram publicados no grupo Codeboxd após validação de sintaxe pelo agente Xano. O usuário confirmou que a verificação manual subsequente funcionou. Não foram fornecidos status HTTP ou respostas sanitizadas para registrar os resultados individualmente; portanto, o aceite de runtime permanece como evidência informada, sem recibo independente. A consulta anterior retornou zero candidatos, então não houve claim real, chamada Cloudinary destroy nem alteração de journal. Flags seguem desligadas.

Ensaio integrado parcial em 19/11/2026, após o usuário habilitar os gates Xano: capabilities retornou HTTP 200 com `uploads_enabled=true`; login da conta descartável (member) e criação de imagem/post funcionaram; repetir o POST retornou o mesmo post; a leitura exibiu Cloudinary e ocultou `image_asset_record_id`. A primeira edição recebeu HTTP 429; a tentativa de remover o post de teste não foi confirmada pela ferramenta. Leitura autenticada posterior não encontrou o marcador de teste. A consulta da reserva `id=1` confirmou, porém, estado `attached` e `post_id=82`, enquanto o post não aparece. A lista de candidatos continuou vazia porque o journal não entrou em `cleanup_pending`. Nenhuma exclusão física do Cloudinary foi feita. Falha bloqueadora identificada em 2.1.6/2.2.1: reconciliar o journal do asset de teste após verificar zero referências e corrigir/publicar `/posts/{id}` para enfileirar a imagem na mesma transação da exclusão. Não repetir escrita nem alterar o journal até revisar o endpoint e confirmar a contagem de referências no Xano. O gate local permanece false; o estado remoto foi habilitado pelo usuário e precisa ser restaurado para false após a validação.

Correção do diagnóstico e continuação do ensaio integrado em 19/11/2026: a busca inicial pelo texto marcador foi insuficiente; leitura autenticada confirmou que o post 82 existia e era dono da reserva 1, portanto a exclusão não havia ocorrido naquele ponto. Edição de texto preservou a imagem; leitura seguinte confirmou o novo texto. Substituição real passou para revisão 2; reserva com revisão antiga foi rejeitada com HTTP 400. Remoção explícita manteve o post e colocou a reserva 2 em `cleanup_pending`. Uma segunda substituição criou a reserva 3; DELETE retornou HTTP 429 com Retry-After 20, então não foi repetido automaticamente. Após a espera, leituras autenticadas confirmaram o post ausente e reserva 3 em `cleanup_pending`, demonstrando que o resultado do DELETE era ambíguo apesar do 429. Prévia administrativa autenticada encontrou 2 candidatos de teste elegíveis e foi salva privadamente em `.local/cloudinary-test-cleanup-preview-06018b32073043c2b1faa862f63959db.json`, aprovação `sha256:feab10d8519a4e4021a4052065ed2e25729bad951539db69913f0a6e469ebbf4`. Nenhuma exclusão física foi executada; os dois assets permanecem no journal para aprovação exata do lote. 2.1.4/2.1.5/2.1.6 e 2.2.1 continuam abertas até concluir as demais falhas/concorrência/autoria e limpeza aprovada. Gates Xano continuam `true` neste momento por solicitação do usuário; gate local foi habilitado apenas no processo de teste e `.env` não foi alterado.

Validação local complementar em 19/11/2026: `reflex compile --dry` passou. A inicialização de produção para navegador não abriu uma porta local neste ambiente, inclusive após tentar uma porta alternativa; o processo foi interrompido sem alterar dados. Portanto 2.2.2 continua aberta. Suíte completa: 770 testes, com três falhas fora desta change (expectativa de 25/35 itens de livros em `test_admin`, lista de target_types de reports desatualizada e contagem fixa de endpoints de sessão); os 44 testes focados de imagem/limpeza passaram. Esses três testes não foram alterados por pertencerem a mudanças administrativas paralelas.

Limpeza autorizada em 19/11/2026: o usuário aprovou o lote exato `sha256:feab10d8519a4e4021a4052065ed2e25729bad951539db69913f0a6e469ebbf4`. O executor refez a leitura autenticada, confirmou os mesmos 2 candidatos, reivindicou cada journal em transação, validou cada recurso Cloudinary e executou um único destroy por asset. As duas respostas foram confirmadas e os estados finais ficaram `deleted`; nova leitura retornou zero candidatos elegíveis. Recibo privado sanitizado: `.local/cloudinary-test-cleanup-execution-d5b55288bad548b18e8c1dc26203d89b.json`. O asset anterior à substituição continua sob carência de 24 horas e não foi incluído/apagado. Nenhuma repetição automática ocorreu. Os gates Xano permanecem `true` para a janela de validação; precisam voltar a `false` antes de encerrar a janela. Nenhum segredo foi registrado.

Retomada para fechamento em 19/11/2026: suíte direcionada Cloudinary/limpeza/reservas/fluxo/backend passou em 79 testes; `reflex compile --dry`, `git diff --check` e `openspec validate hospedar-imagens-publicacoes-cloudinary --type change` passaram. Tentativa de abrir servidor Reflex em produção compilou, mas o Windows bloqueou a porta 3000 e a porta alternativa 3001 não aceitou conexão; processo iniciado nesta verificação foi encerrado. Não há ferramenta de navegador conectada nesta sessão. CLI Xano 1.2.0 consultada: não oferece comando `workspace env`; não foi feito push de ambiente para evitar sobrescrever credenciais. Os gates remotos ainda precisam retornar a `false`, e o aceite visual e a matriz completa de integração permanecem abertos. A limpeza do lote aprovado está concluída conforme o recibo sanitizado acima; um asset distinto segue corretamente em retenção de 24h.
