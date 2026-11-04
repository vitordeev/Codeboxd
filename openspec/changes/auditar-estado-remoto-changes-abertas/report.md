# Conferência das changes abertas — 03/11/2026

## Resultado

O contrato novo de status das listas ainda não foi implantado no workspace
inspecionado. O feed já consulta posts/seguidores diretamente. Administração e
recuperação possuem estruturas no backend, mas seus critérios de efeito real
continuam sem comprovação completa. Duas flags locais estão desativadas e o
scaffold preexistente falha na validação global.

| Change funcional | Checklist preservado | Resultado da conferência |
| --- | --- | --- |
| corrigir-conexoes-feed-listas | 6/7 | Tabela, função e rotas de status ausentes; follow ainda sem índice composto/transação do roteiro; feed direto presente |
| recuperar-senha-codigo-6-digitos | 8/10 | Resend e referências de configuração presentes; envio aceito, caixa e ciclo real não comprovados |
| gerenciamento-website | 22/34 | Oito operações administrativas presentes, guards e auditoria inspecionados; quatro GETs rejeitaram visitante; faltam critérios autenticados e mutações reais |
| otimizar-performance-app | 14/37 | /library existe, mas flags locais de paginação e identidade de listas estão desativadas; metas e comparações completas seguem abertas |

São **38 tarefas funcionais abertas**. A auditoria documental não encerra esses
critérios. `corrigir-follow-feed-status-filmes` é um scaffold sem proposal,
design, specs ou tasks; não constitui uma entrega concluída 0/0.

## Método e escopo

- Conferidos `git status --short`, `openspec list --json`, checklists, artefatos,
  serviços/estado e evidências das quatro changes e do scaffold. Preservadas
  alterações locais anteriores, sem commit, reset, remoção ou arquivamento.
- Descoberto acesso administrativo local válido, selecionado pelo hostname da
  instância configurada, usando `tools.session_revocation.metadata_config`.
  Isso corrige a limitação de acesso registrada nas rodadas anteriores.
- GET `/api:meta/workspace/<workspace>/multidoc?env=false&records=false` → 200:
  **80 documentos, 54 queries, 39 queries autenticadas** inspecionadas. Export
  ficou somente em memória; não persistido, sem valores de ambiente ou registros.
- GET de grupos e endpoints → 200: grupo social com **40 operações** e
  autenticação com **7**. Sem rotas de media-list-status na listagem social.
- Consultas REST sem login, com 1,2 s entre requisições, sem retry ou redirecionamento
  automático. Usados `.venv`, httpx e as URLs configuradas, sem imprimir valores.
  Execução de rede com permissão fora do ambiente restrito.
- Não executados POST, PUT, PATCH, DELETE, envio de e-mail, login, criação de
  conta, alteração de senha, suspensão, migração ou publicação. O GET legado
  que envia código não foi chamado.

O export mostra contratos do workspace; não substitui comprovação de cada
comportamento publicado. HTTP 401 comprova rejeição do visitante naquela chamada,
não autorização correta para todos os papéis ou ausência de efeitos em mutações.
Diferenças textuais entre export e arquivos locais não foram classificadas como
defeitos, pois o Xano normaliza formatação.

## Conexões, feed e listas

Confirmado no schema e nas listagens:

- Ausente tabela `user_media_list_status`.
- Ausente função `Lists/set_media_list_status`.
- Ausentes GET/PUT `media-list-status/{media_id}`.
- `user_follow` tem PK, UNIQUE `identity_key` e índices separados por follower e
  followed; não possui UNIQUE composto `(follower_id, followed_id)`.
- `post` tem índices individuais user_id/media_id; não possui o composto
  `(user_id, id)` do roteiro.
- PUT follow usa `db.add_or_edit user_follow`; DELETE consulta/remove o registro.
  Não têm a transação/lock e a resposta `following` explícita do roteiro novo.
- GET feed consulta `post` com join `user_follow`, filtro do seguidor e ordem
  decrescente por ID. Não depende de um post próprio do leitor nesse stack.
- As rotas de listas ainda não referenciam a nova fonte de status.
- `user_list.default_key`, UNIQUE correspondente e `Lists/ensure_default_list`
  estão presentes: a implantação histórica de identidade das listas é distinta
  da migração nova, que ainda falta.

**Próximo passo:** seguir backup, ensaio, migração e corte coordenado de
`../corrigir-conexoes-feed-listas/xano-changes.md`. O pedido de conferência
autoriza esta inspeção de leitura; não altera a aplicação manual prevista na
change nem autoriza migração automática. Tarefa 3.2 segue aberta até testes
autenticados de usuário sem posts, seguir/deixar de seguir, exclusividade,
concorrência, preservação de avaliações e limpeza.

## Administração e segurança de sessão

As oito operações administrativas listadas são GET dashboard/users/catalog/reports,
POST catalog e PUT catalog/{id}, users/{id}/status e reports/{id}.
Todas referenciam `Security/require_current_session`, ator de `$auth.id`, conta
ativa e papel admin. Todas as **39 queries autenticadas** referenciam o guard
de sessão; `user.session_version` e a função de verificação estão presentes.

PUT de status de conta e PUT de revisão têm transação e gravação `event_log`
com ator autenticado, estado anterior/novo e motivo/decisão. A revisão não tem
remoção automática de post, comentário, obra ou perfil no contrato inspecionado.
Isso comprova presença da lógica, não persistência/atomicidade em ensaio real.

**Próximo passo:** ensaios com admin e membros controlados: filtros/paginação,
contagens conhecidas, suspensão/reativação e bloqueio de sessão suspensa,
auditoria persistida, edição preservando identidade e integridade dos alvos de
reports. Navegador real ainda necessário. Não promover usuários automaticamente.

## Recuperação de senha

As três rotas de reset estão presentes. A solicitação referencia
`api.resend.com`, `RESEND_API_KEY`, `RESEND_FROM` e verificação do resultado/ID
de entrega. Consumo do código e atualização da senha usam transações; há
referências de propósito password_reset e versão de sessão nos respectivos fluxos.
Valores das variáveis e registros de recuperação não foram consultados.

**Próximo passo:** caixa elegível e controlada; comprovar envio aceito, chegada
do código, troca de senha, novo login, rejeição de reutilização e restauração.
Sem esses ensaios, nem integração presente nem resposta genérica comprovam
entrega. Mantidas abertas 3.2/3.4. Não reexecutados scripts históricos com saída
datada nem sobrescritas evidências anteriores.

## Performance e configuração local

GET `/library` está no workspace e exige autenticação. Após importar o app em
um processo Python novo, os valores efetivos foram:

| Flag | Valor efetivo |
| --- | --- |
| LIBRARY_PAGINATION_ENABLED | false |
| DEFAULT_LIST_IDENTITY_ENABLED | false |
| COOKIE_SECURE | false |

As duas primeiras não estão definidas no `.env` inspecionado nem no ambiente
efetivo desse processo; o código assume false. A biblioteca segue o caminho
legado, e a preparação das listas não usa o modo novo por chave estável. Isso
diverge de registros históricos de ativação. Não comprova os valores herdados
por um servidor que já estivesse rodando. COOKIE_SECURE=false é compatível com
HTTP local; hospedagem/HTTPS não fazem parte desta etapa.

**Próximo passo:** conferir/validar os contratos antes de habilitar flags; não
ligá-las automaticamente por presença de arquivos ou schemas. Completar as
23 tarefas de performance contra metas aprovadas, com cinco amostras comparáveis,
desktop/celular, contas adequadas e distinção entre métricas Python/API/browser.
Esta auditoria não executou benchmarks nem comprovou eliminação de 429.

## Resultados HTTP sem autenticação

| GET | HTTP |
| --- | --- |
| social /media?per_page=1 | 200, conferência anterior desta sessão |
| social /feed | 401, conferência anterior desta sessão |
| social /admin/dashboard | 401 |
| social /admin/users | 401 |
| social /admin/catalog?media_type=movie | 401 |
| social /admin/reports | 401 |
| social /library | 401 |
| social /lists | 401 |
| social /profiles | 200 |
| social /lists/public?per_page=1 | 200 |
| social /media-list-status/1 | 404, repetido na conferência atual |
| auth /auth/me | 401 |

Corpos de usuários, perfis, listas e obras não foram impressos ou persistidos.

## Validação local e documental

- `.venv/Scripts/python.exe -m pip check` → **No broken requirements found**,
  executado nesta conferência.
- `openspec validate --all --json --no-interactive` antes desta change →
  **23/24 válidos**: 19/19 specs e 4/5 changes. Única falha:
  `corrigir-follow-feed-status-filmes`, sem deltas/artefatos. Não foi ocultada
  adicionando skip_specs a um scaffold sem escopo.
- Evidência anterior desta mesma sessão, com código inalterado desde então:
  **464 testes OK**, incluindo 47 administrativos; compile seco aprovado em
  21,625 s. Não executados novamente só para esta documentação.
  Referência: `../gerenciamento-website/validation/confirmacoes-contexto-2026-11-03.md`.
- Após a consolidação: `openspec validate auditar-estado-remoto-changes-abertas
  --type change` → válida. Validação global → **24/25 válidos**, 19/19 specs e
  5/6 changes, incluindo esta auditoria. A única falha continua sendo o scaffold
  `corrigir-follow-feed-status-filmes`.
- `git diff --check` → sem erros, apenas avisos LF/CRLF em arquivos já alterados.
  Verificação local de links e referências → todos existentes; padrões de token
  ausentes nos Markdown desta change (verificação heurística).
- Contagens dos quatro checklists reconferidas por script → preservadas em
  6/7, 8/10, 22/34 e 14/37. Auditoria documental concluída **3/3**.

## Limites finais

Conferência das changes e contratos, sem auditoria exaustiva de segurança,
integridade de todos os registros ou teste de todas as jornadas. Não houve
navegador autenticado, leitura de caixa de e-mail ou teste com papéis de membro,
admin e suspenso nesta rodada. Nenhum critério funcional foi marcado concluído.
Sem alterações no produto, nas flags ou no Xano; sem Docker ou reinício.
