# Validação do planejamento — 26/10/2026

- Escopo: planejamento vinculado à P.1; não é evidência de credenciais revogadas.
- `git status --short` inicial: sem alterações.
- `openspec list --json`: três changes anteriores, sem cobertura de rotação.
- Proposta, design, delta operational-reliability e nove tarefas de implementação preparados.
- Auditoria de segredos, rotação, testes de integração e invalidação de sessões: não executados; tarefas abertas.
- `openspec status --change proteger-credenciais-expostas`: quatro artefatos de planejamento completos.
- `openspec validate proteger-credenciais-expostas --type change`: aprovado.
- `git status --short` final: somente o novo diretório da change, sem alteração de código ou configuração privada.

## Inventário — 26/10/2026

- `audit_inventory.py`: exit 0; 67 commits, 1.444 blobs alcançáveis, limites em inventory.md.
- `audit_triage.py`: exit 0; cinco identidades distintas, cinco registros com senha e dois campos de token históricos; valores não publicados. Verificação dos artefatos contra segredos/identidades conhecidos aprovada.
- `git check-ignore .env .aws/credentials .local/`: três caminhos cobertos.
- Consulta ao índice dos caminhos privados históricos: não rastreados (exit 1 esperado de `git ls-files --error-unmatch`).
- 1.1 concluída com evidência; nenhuma tarefa de rotação, revogação ou acesso remoto concluída.

## Classificação e verificações remotas — rodada seguinte em 26/10/2026

- `audit_access.py`: seleção inicial do perfil padrão obteve HTTP 403 de outra instância; corrigido para exigir perfil único com instance_origin correspondente ao projeto. Reexecução GET fora do sandbox: exit 0, lista de tabelas 200, três registros correspondentes 200 e member/active; duas identidades sem ID permanecem não verificadas. Sem escrita remota.
- `check_tmdb_credential.py`: GET oficial fora do sandbox, exit 0, token atual igual ao exposto, autenticação 200/success=true; rotation_verified=false.
- Tentativas de rede no sandbox foram bloqueadas; repetidas com escalonamento autorizado. Arquivo CLI tinha múltiplos perfis e não foi alterado. PyYAML não está instalado; nenhuma dependência foi adicionada. A leitura usa formato restrito já existente e falha diante de perfil ambíguo.
- Tarefa 1.2 concluída como classificação e preparação; rotação, revogação e tratamento das contas continuam abertos.
- Após os relatórios desta rodada: `audit_triage.py` aprovou checagem contra valores privados conhecidos; `openspec validate proteger-credenciais-expostas --type change` passou e `git diff --check` não apontou erros. Git continua com alterações somente na pasta da change.

## Verificação após atualização informada do .env — 26/10/2026

- Usuário confirmou acesso ao TMDB e informou atualização do .env.
- Reexecução de `check_tmdb_credential.py`: rede bloqueada no sandbox; consulta GET oficial repetida com escalonamento autorizado, exit 0.
- Resultado: current_matches_exposed=true, atual/exposto HTTP 200 e authenticated=true, rotation_verified=false. O valor efetivamente lido no .env do projeto ainda coincide com o histórico. Nenhum valor exibido.
- Nenhum teste de consumidor com credencial substituta foi executado, pois não há substituição detectada. 2.1/2.2 permanecem abertas; necessário salvar token diferente e revogar o anterior na conta emissora.

### Segunda atualização informada

Usuário informou nova atualização. GET oficial repetido fora do sandbox após falha de rede local: exit 0, current_matches_exposed=true, HTTP 200 para atual/exposto, rotation_verified=false. O valor lido continua idêntico ao histórico; necessário esclarecer se foi alterada a API Key ou o API Read Access Token, sem solicitar valores. Nenhuma tarefa de rotação concluída.

### Atualização posterior: rotação TMDB comprovada

- Usuário informou nova atualização do .env. Consulta GET oficial repetida após bloqueio de rede no sandbox, com escalonamento autorizado: current_matches_exposed=false, novo HTTP 200/authenticated=true, exposto HTTP 401/authenticated=false e rotation_verified=true.
- Ampliado check_tmdb_credential.py com GET movie/popular e tv/popular usando o novo token: ambos HTTP 200, has_results=true. Reexecução exit 0, sem exibir tokens ou conteúdo dos catálogos. Resultado em tmdb-check.json.
- 2.2 concluída para C.01; nenhum outro segredo de serviço teve exposição confirmada nesta cobertura. Contas/tokens de usuário são tratados separadamente na tarefa 2.3, ainda aberta.
- 2.1 permanece aberta para recarga e validação de consumidores em execução. Não houve reinício, compilação ou verificação de navegador nesta rodada.

## Continuação autorizada: execução, contas e prevenção

- `.venv/Scripts/python.exe -m reflex compile --dry`: exit 0, compilação aprovada. Nenhum listener Reflex anterior identificado. Aplicação iniciada em produção/porta única 3030 com logs privados; primeira exportação falhou por timeout de prerender, repetição sem alteração de código passou. Listener observado PID 13172.
- `check_reloaded_browser.py`: Edge headless real, home 200, fileiras Agora nos cinemas, Filmes muito bem avaliados, No radar: próximos filmes e Séries muito bem avaliadas com 20 cards cada; reloaded-browser.json, passed=true.
- `rotate_test_accounts.py` em prévia remota: quatro logins de membro válidos, quinta senha rejeitada 403 e dois tokens históricos 401; account-preview.json.
- `--apply`: primeira tentativa alterou A.01, depois encontrou 429. Retomada com espaçamento de dois segundos e preservação dos substitutos/trocas aprovadas concluiu A.03/A.04/A.05. account-rotation.json comprova as quatro senhas novas e identidades 200, senhas antigas 403. A.02 continua 403 sem alteração. Evidência anterior preservada em account-rotation-attempt-1.json.
- Os quatro testes explícitos de sessão anterior à troca retornaram 200. 2.3 aberta; não houve alteração de schema, autenticação, status de conta ou política de tokens. Dois tokens históricos guardados nos JSON retornam 401, o que não equivale a invalidar toda sessão anterior.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_staged_secrets.py -q`: quatro testes aprovados; fixtures sintéticas, sem rede.
- `tools/check_staged_secrets.py --all-index`: exit 0, 818 arquivos, sem achados; execução padrão sem git add: zero alterações preparadas, sucesso sem alegar cobertura dos não rastreados.
- `verify_change_files.py`: revisão adicional dos arquivos modificados/não rastreados aprovada; working-tree-secret-check.json. Nenhum git add, commit ou push realizado.
- `git check-ignore`: .env, .aws/credentials, .xano/credentials.yaml e substitutos em .local cobertos. Exemplos de configuração com placeholders permanecem públicos; nenhuma cópia privada apagada.
- `audit_triage.py`: checagem dos artefatos também contra novas senhas privadas, além dos segredos históricos e atuais, aprovada. Não publica identidades ou valores.
- Pendência de política de sessões apresentada ao usuário por pergunta assíncrona; nenhuma resposta presumida. Estado reconciliado em status.md e documentos centrais, mantendo a change ativa.
- Validação final: 32 arquivos novos/modificados revisados sem achados, checagem de privacidade dos relatórios aprovada e `openspec validate proteger-credenciais-expostas --type change` aprovado. `git diff --check` sem erro. A geração Reflex alterou apenas finais de linha em reflex.lock/package.json; CRLF restaurado conforme core.autocrlf=true, sem mudança semântica ou de dependência.

## Fechamento da tarefa 2.3

A dependência revogar-sessoes-apos-troca-senha foi criada após autorização para concluir a revogação: implementação e publicação verificadas por export, 39 rotas protegidas, nenhuma alteração de documento alheio e 29 checks de API real aprovados. Browser real aprovou rejeição de sessão legada, novo login e biblioteca autenticada; suíte completa 392 testes OK.

Leitura paginada dos metadados confirmou que A.02 não existe mais; não foi removida nesta rodada. Quatro contas existentes mantêm senhas novas e login válido; a política rejeita tokens anteriores, inclusive na API social direta e no reset, sem afetar outra conta. Evidências concretas estão em ../2026-10-26-revogar-sessoes-apos-troca-senha/validation.md e respectivos JSON sanitizados. A limitação de sessões apontada anteriormente foi resolvida; 9/9 tarefas concluídas. Commit/push ficam manuais, conforme manual-git.md da dependência.
