# Sessão, cache concorrente e limites — 20/10/2026

## Autorização, escopo e conclusão

Após a tarefa 1.1, o usuário orientou continuar concluindo várias tarefas.
Selecionadas 2.1 (diagnóstico de autenticação), 3.1 (revisão de caches), 3.2
(duplicação de leituras) e 3.3 (cooldown/tentativas nos caminhos diagnosticados).
Motivo e intervenção apresentados durante a rodada; essa orientação atual
autoriza implementação local, testes e registros relacionados. Não houve
publicação remota, alteração de credenciais, servidor, conta ou e-mail real.

Arquivos de produto: state/social.py, state/session.py, services/api.py e
services/catalog.py. Testes: novo test_navigation_concurrency.py e ampliações
de test_session_navigation_performance.py, test_api_rate_limit.py e test_catalog.py.

## 2.1 — Diagnóstico dos fluxos de autenticação

Conferidos session.py, auth_state.py, formulários de login/account/admin,
roteamento, transporte e evidências anteriores. O inventário 1.1 preservado
mapeia os componentes/handlers; este relatório completa o diagnóstico.

| Caminho | Chamadas, bloqueios e destino |
| --- | --- |
| Login de membro | Validação local; POST auth/login; GET auth/me; destino conta. is_loading bloqueia novo envio enquanto pendente. Perfil usa identidade de navegação por 15 s e carrega detalhe antes de referências. |
| Login admin | POST auth/login, GET auth/me, conferência de papel; membro rejeitado no login dedicado. Guards não usam o cache de identidade para conceder administração. |
| Cadastro | Valida configuração, username, senha e confirmação; POST auth/signup e GET auth/me, com destino conforme papel. Nenhuma repetição automática do POST. |
| Sessão | Token cookie ou SessionStorage; auth/me valida identidade e conta desativada. 401/403 podem limpar sessão; falha transitória preserva token, remove papel e invalida reutilização. Cooldown por hash do token evita nova verificação durante prazo. |
| Recuperação | GET reset/request-reset-link envia e-mail: tem efeito colateral apesar do verbo. Confirmação usa POST magic-link-login e POST update_password, sem guardar token intermediário como login. is_loading protege envio pendente, mas antes não bloqueava novo pedido depois de 429. |
| Logout | Limpa sessão; logout_social limpa dados pessoais também. Troca de credencial não herda identidade validada. |

Gargalo identificado: GET de e-mail podia repetir até três vezes se recebesse
429 com espera curta, e novo clique após a falha podia chamar o serviço antes
do prazo. Intervenção aplicada: exclusão explícita desse endpoint do retry e
cooldown local do pedido por hash do e-mail normalizado. Esse bloqueio pertence
à sessão e à última identidade de e-mail limitada; não representa quota global,
limite antiautomação nem substitui controles Xano.

Limite de segurança preservado: `_require_user` tem fallback histórico em
falha transitória, enquanto o endpoint Xano continua responsável por autorizar
gravações. Não se conclui 2.2 nem autorização remota a partir desse diagnóstico.
Primeiro perfil/cache frio e revisitas/cache quente têm evidências históricas
separadas; não foram medidos novamente nesta rodada.

## 3.1 — Revisão e decisões de cache

| Escopo existente | Isolamento, limites e invalidação conferidos | Decisão desta rodada |
| --- | --- | --- |
| Identidade de navegação | 15 s, hash de token e user_id; somente member; guard/admin e mutações validam novamente; expiração, logout, troca de token e 401/403 invalidam | Preservar prazo e autorização; não ampliar cache |
| Leituras sociais | Cache por estado/sessão, token, path, params, data e paginate; 15 s, máximo 32 entradas, cópias profundas; invalidação antes/depois de mutação inclusive falha; geração impede repovoar com leitura antiga | Corrigir janela de consultas simultâneas que ocorria antes de preencher o cache |
| Catálogo público | fetch e Kitsu: 300 s e até 128 entradas por cache/processo; chave inclui URL e argumentos, inclusive credencial quando usada; cópias; respostas inválidas/erros não entram | Preservar contrato, TTL e limite; corrigir interpretação de Retry-After no transporte |
| Biblioteca paginada | /library não entra no cache social; uma página por solicitação, loading impede repetição, prazo monotônico de 429 | Preservar caminho independente e testes existentes |

Limites revisados por inspeção e testes pertinentes, sem contar os caches
históricos como implementação nova. Cache público continua restrito aos
adaptadores públicos; não compartilha resposta privada Xano entre usuários.
Deduplicação pública entre sessões não foi introduzida. Cache de tradução
persistente não mudou; é outro contrato, não o cache de navegação desta tarefa.

## 3.2 — Leituras simultâneas

Antes, duas consultas equivalentes iniciadas com cache vazio faziam duas
requisições. Agora compartilham uma tarefa de leitura enquanto pendente.
Teste controlado confirmou **2 consumidores → 1 chamada**, com resultado e cache
em cópias independentes. Expiração segue em 15 s; não há prazo novo de cache.

A chave de compartilhamento combina nonce aleatório do estado, geração de
invalidação e digest da consulta. Páginas, params, tokens, estados e gerações
distintos não compartilham tarefa. A tabela de tarefas é transitória no processo
e removida em sucesso/erro; nenhum asyncio.Task entra no estado serializado.
Cancelamento de um consumidor não cancela os demais. Erros são propagados,
não armazenados; tentativa posterior consulta o serviço. Mutações nunca são
compartilhadas ou repetidas automaticamente por esse mecanismo.

Também fixado o token do início da consulta por todas as páginas do lote.
Troca antes do início da tarefa impede o envio; troca durante a leitura descarta
o resultado e impede a próxima página com token de outra conta. O cliente
recebe erro de sessão alterada (409 local), sem limpar uma sessão nova válida.
Não é garantia geral contra respostas atrasadas em todo loader do app: 3.4
continua aberta, especialmente para renderização de outras fichas/rotas.

Risco/limite: coordenação em memória por processo, não entre workers. Cancelar
o último consumidor pode deixar a leitura terminar até o timeout do transporte;
ao terminar, a entrada é removida. Não se persiste nem distribui tarefa assíncrona.
Esse escopo é compatível com a execução local atual; não promete deduplicação
distribuída e não introduz infraestrutura.

## 3.3 — Retry-After e efeitos colaterais

- Transporte Xano mantém no máximo três tentativas para leitura segura com
  espera curta (até 3 s); POST/PUT/PATCH/DELETE não repetem. GET de e-mail
  é explicitamente excluído da repetição, inclusive Retry-After de 1 s.
- Pedido de e-mail registra hash normalizado e prazo monotônico após 429;
  novo clique da mesma identidade não envia chamada antes do prazo e pode
  tentar novamente depois sem login/logout. A mensagem é genérica.
- Catálogo antes convertia Retry-After com float e, numa data HTTP válida,
  caía em espera de 0,5 s. Agora usa o parser comum: aceita número/data HTTP,
  arredonda para cima e usa 30 s para cabeçalho ausente/inválido/não finito.
  Se a espera superar 5 s, encerra a requisição atual sem tentar cedo.
- Backoff de 503 sem Retry-After segue 0,5 s e 1 s, no máximo três tentativas.
  Sessão/auth e biblioteca mantêm os cooldowns já implementados e testados.

Não se aplicou cooldown global ao Xano ou a todos os provedores. O escopo real
da quota continua desconhecido (1.4 aberta). Retornar erro de catálogo quando
o prazo é longo não bloqueia consultas manuais futuras no backend; é limite
de retry dessa requisição, não uma nova política de quota global.

## Validação executada

Ambiente `.venv`, Reflex 0.9.11.post1 já instalado, sem instalar dependências.
Skills reflex-docs e reflex-process-management consultadas; documentação de
[backend vars](https://reflex.dev/docs/vars/base-vars/) confirma a necessidade
de manter valores serializáveis no estado persistido. Tasks ficam fora dele.

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests -q
.venv/Scripts/python.exe -m reflex compile --dry
```

Resultado final: **244 testes aprovados** e **compilação Reflex aprovada**.
Foram adicionados 13 testes: 8 concorrência, 2 transporte Xano, 1 cooldown do
pedido de e-mail e 2 catálogo. A suíte anterior desta rodada tinha 231 testes,
incluindo os dois do inventário. A primeira execução intermediária tinha 241;
a final inclui a troca antes do início da tarefa e os dois casos de catálogo.

| Critério | Evidência local |
| --- | --- |
| Reutilização/expiração/cópias | test_social e test_home_performance, mais teste de cópias entre consumidores |
| Concorrência e redução | test_navigation_concurrency: duas leituras → uma chamada |
| Páginas, tokens e sessões separados | Quatro consultas distintas → quatro chamadas; leitura antiga rejeitada |
| Erro e cancelamento | Erro compartilhado não entra no cache, retry posterior funciona; cancelar um consumidor preserva outro |
| Invalidação e falha de escrita | Testes de geração existentes e nova mutação falha durante leitura; requisição posterior não compartilha geração antiga |
| Credencial alterada | Troca antes da tarefa: zero envios; durante primeira página: sem segunda página e sem cache |
| Cooldown e recuperação | Sessão e pedido de e-mail sem nova chamada antes da expiração, retomada depois; biblioteca com testes existentes |
| Retry-After | Número/data HTTP/ausente/inválido/NaN/inf; prazo longo não repete; prazo curto repete com espera; mutações e e-mail não repetem |

Logs de testes contêm falhas de provedor intencionalmente simuladas e avisos
asyncio de tempo associados ao relógio monotônico mockado. Não representam
latência real ou falha da suíte. Não usar esses tempos como benchmark.

Sem navegador, validação remota, e-mail real, reinício do app ou Docker.
A instância já aberta, se houver, precisa de reinício para usar o código novo;
compilação não comprova atualização de um processo em execução. Não se encerram
1.3/1.4, 2.2–2.4, 3.4/3.5, 6.2/6.4 ou integração geral.

## Rollback

Reverter apenas os trechos desta rodada nos quatro arquivos de produto e nos
testes relacionados; remover o novo teste de concorrência e esta evidência;
reabrir 2.1/3.1/3.2/3.3 e reconciliar os registros centrais. Preservar o
inventário anterior e toda evidência histórica. Sem migração ou dados remotos.
