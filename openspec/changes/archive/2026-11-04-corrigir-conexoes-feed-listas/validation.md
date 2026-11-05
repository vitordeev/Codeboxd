# Evidências locais — 29/10/2026

## Verificação remota somente de leitura — 03/11/2026

Após o usuário informar que não sabe se o roteiro foi aplicado, foram feitas
quatro consultas GET sem autenticação à base social configurada no `.env`.
Valores de configuração, credenciais e conteúdos não foram impressos nem
copiados para este relatório. Nenhuma conexão administrativa ao workspace,
escrita, login, migração ou publicação foi executada.

| Consulta | HTTP | Observação |
| --- | --- | --- |
| `/media?per_page=1` | 200 | JSON lista; controle de conectividade |
| `/feed` | 401 | ERROR_CODE_UNAUTHORIZED; exige autenticação |
| `/media-list-status/1` | 404 | ERROR_CODE_NOT_FOUND |
| rota de controle inexistente | 404 | ERROR_CODE_NOT_FOUND |

Execução via `.venv/Scripts/python.exe -B -`, httpx, timeout 15 s,
follow_redirects=false, espaçamento 1,2 s, sem retries nem tokens.
A primeira tentativa restrita falhou com ConnectError; a repetição com
permissão de rede concluiu as quatro consultas, código 0.

O 404 do endpoint novo é compatível com rota ausente, mas sem autenticação e
sem inspecionar o schema publicado não distingue definitivamente ausência da
rota de rejeição contextual/registro ausente. O 401 do feed não comprova seu
join, os índices ou a independência de posts próprios. Não há evidência de
migração completa, e não foi possível confirmar etapas parciais.

Tarefa 3.2 permanece aberta (**6/7**). Próximo passo: conferir no editor Xano
GET/PUT `/media-list-status/{media_id}`, tabela `user_media_list_status`, função
de escrita e projeções das listas, seguindo o roteiro de backup/migração.
O escopo existente exige aplicação manual; esta verificação não o altera.

Os registros abaixo preservam o estado da rodada de 29/10, anterior a esta consulta.

## Estado e limites

Implementação Python pronta para o contrato proposto. **Xano não alterado**;
task 3.2 aberta. Não houve acesso ao workspace, publicação de endpoints,
criação/limpeza de dados reais, teste autenticado remoto, teste em navegador,
reinício de servidor, commit, sincronização ou arquivamento. Sem Docker.
O arquivo project.md solicitado está ausente; contexto substituto registrado
na proposta/investigação. Pasta preexistente corrigir-follow-feed-status-filmes
preservada, assim como demais changes e auditoria do outro colaborador.

## Comandos e resultados

- `.venv/Scripts/python.exe -c "import importlib.metadata; print(importlib.metadata.version('reflex'))"`
  → Reflex 0.9.11.post1; ambiente existente, sem instalação.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests`
  → **451 testes OK**, após adaptar consumidores dos eventos follow/quick_add
  para async generators. Primeira execução intermediária: 434 testes, três
  erros de harness antigo (await em async generator); corrigidos e repetida a
  suíte completa. Não foram falhas remotas. Mensagens de indisponibilidade de
  restore/logs 429 são cenários simulados da suíte, não ações reais de restauração.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_follow_feed_list_status.py -v`
  → primeiro 17 OK; após ampliar cobertura e pequenos ajustes finais, **22 OK**.
  Os conjuntos se sobrepõem: não somar 451+22 como testes distintos da suíte.
- `.venv/Scripts/reflex.exe compile --dry` → aprovado, 20,419 s na primeira
  compilação desta rodada; recompilação após ajustes finais também aprovada,
  91,941 s. Sem iniciar servidor.
- Regressão dos testes existentes após ajustes finais de status:
  `unittest discover -s tests -p test_social.py` → 38 OK;
  `... -p test_required_submission_content.py` → 6 OK;
  `... -p test_media_progressive.py` → 8 OK. Todos com `.venv/Scripts/python.exe -B -m`.
- `openspec validate corrigir-conexoes-feed-listas --type change` → válida.
- `git diff --check` → código 0; aviso de normalização LF/CRLF no teste editado,
  sem erro de whitespace. Sem edição de reflex.lock/package.json.

## Cobertura nova (mocks, não backend)

Follow/unfollow/refollow com IDs string/int; confirmação do estado efetivo;
registro legado e DELETE confirmado por leitura; resposta malformada; alvo
inválido/self; 409/429/503; bloqueio concorrente; troca de conta.

Conta sem posts lendo posts históricos dos seguidos; falhas de /posts, /likes
e referências sem descartar feed; erro versus vazio e retry; autorização
não mascarada; resposta de carga anterior no mesmo caminho descartada;
refresh bem-sucedido limpa erro anterior.

Status GET validando IDs/enum; switch planned/completed/nenhum; botões e itens
do estado local sincronizados; controle superior de consumo atualizado pelo
status confirmado; nota/review preservadas; falha PUT mantém confirmação GET;
endpoint ausente não aciona escritas legadas; bloqueio de sobreposição; resposta
de outra obra e leitura antiga descartadas; troca de conta antes da escrita;
reconciliação após timeout pós-commit; picker padrão recarrega estado e
personalizada homônima não depende do endpoint novo; bindings aria-pressed e
erro/retry da tela conferidos por componentes Python. Isso não comprova layout
ou interação em navegador nem transações/índices reais no Xano.

## Arquivos desta entrega

- `Codeboxd_main/state/social.py`: confirmação de conexões, carga tolerante a
  falhas auxiliares do feed, status único de listas, contexto e concorrência.
- `Codeboxd_main/pages/social.py`: pending, seleção acessível e erro/vazio/retry.
- `assets/codeboxd.css`: destaque do status confirmado e estado disabled.
- `tests/test_follow_feed_list_status.py`: 22 regressões com mocks.
- `tests/test_social.py`, `tests/test_required_submission_content.py`: adaptar
  chamadas aos eventos e verificar organização sem apagar avaliações.
- `openspec/README.md`: referência da entrega e dependência manual.
- Nesta change: .openspec.yaml, proposal.md, design.md, tasks.md,
  specs/social-connections/spec.md, specs/social-feed/spec.md,
  specs/user-lists/spec.md, investigation.md, xano-changes.md, validation.md.

## Aceite ainda externo

Aplicar [xano-changes.md](xano-changes.md): backup, deduplicação/índice de follow,
stacks idempotentes, feed direto, migração status único, projeções de TODAS as
entradas de listas padrão e testes reais da seção 7. Somente então registrar
aceite remoto e concluir 3.2. Nenhuma causa específica dos incidentes remotos
foi confirmada; as causas Python são constatações do código reproduzidas por mocks.
