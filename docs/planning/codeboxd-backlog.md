# Backlog técnico e de produto do Codeboxd — 29/10/2026

## Resumo executivo e classificação atual

A aplicação tem implementações e testes em todos os módulos centrais documentados. Os maiores bloqueios são comprovar entrega da recuperação, corrigir continuidade do feed, fechar validações administrativas e medir jornadas completas. Não há P0 comprovado nesta auditoria. Ver [arquitetura, fontes e limites](codeboxd-auditoria.md).

Esta ampliação foi autorizada como exceção documental: somente os dois arquivos em docs/planning, sem escrita no OpenSpec. CBX-001 a CBX-009 foram reservados após busca sem IDs CBX anteriores em docs/openspec. São índices de acompanhamento: itens ligados a tasks existentes não são novas tarefas ou autorização de escopo duplicado. P/M/G é tamanho qualitativo por incremento, não prazo. Estado representa a parcela descrita, não a change inteira.

**A classificação desta seção prevalece para a fila atual.** CB-MT-001 a 006 conservam IDs, evidências e prioridades provisórias anteriores na seção histórica abaixo, mas todos permanecem “A verificar”, fora da lista de correções confirmadas. O defeito de paginação CBX-002 foi constatado estaticamente e não confirma a causa do relato CB-MT-006. Sugestões de produto/processo também ficam separadas.

## Backlog confirmado

### Contexto para retomada — decisão do usuário em 29/10/2026

Após revisar a auditoria, o usuário solicitou preparar continuidade por tarefa, mas esclareceu que não é necessário criar as changes agora. Decisão desta rodada: preservar este contexto no repositório e enviar a documentação; não criar changes corretivas nem iniciar implementação. A autorização de commit/push desta rodada substitui a restrição anterior somente para publicar a documentação, sem incluir a alteração local preexistente em reflex.lock/package.json.

Na retomada, ler este backlog, a auditoria, AGENTS.md e o estado atual das changes antes de planejar. Para cada ID escolhido, definir um incremento independente e verificável; se o trabalho já estiver coberto por change ativa, vincular/continuar nela em vez de duplicar tarefas. Se houver decisão de extrair uma change pequena, registrar a relação e reconciliar o checklist original antes de implementar. Não criar automaticamente nove changes concorrentes sobre os mesmos contratos.

Mapa de continuidade: CBX-001 → recuperar-senha-codigo-6-digitos; CBX-003/004/005/006/009 → gerenciamento-website; CBX-007/008 → otimizar-performance-app; CBX-002 → revisar cobertura de performance 7.2 e propor correção pequena de paginação se apropriado. Os seis relatos CB-MT continuam separados como hipóteses a reproduzir. Começar preferencialmente pelo CBX-002 ou pela matriz CBX-003, conforme escolha futura do usuário.

Este registro guarda as decisões e referências necessárias para retomar o trabalho; não é transcrição integral do chat. Nenhum teste remoto, dado real ou correção foi autorizado por este pedido de publicação documental.

| ID | Área | Tarefa | Prioridade | Tamanho | Estado | Dependências | Evidência |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CBX-001 | Recuperação | Concluir comprovação de envio e ciclo real | P1 | M | Bloqueada | Destinatário elegível e caixa controlada, autorização própria | recuperar-senha-codigo-6-digitos tasks 3.2/3.4; validation/elegibilidade-resend-2026-10-28.md; P.6 |
| CBX-002 | Feed | Garantir continuidade além da primeira página de 20 | P1 | P | Pendente | Nenhuma para regressão local; integração social depois | social.py _request_pages:601 e _refresh_posts:1441; specs/social-feed; performance 7.2 |
| CBX-003 | Administração | Completar matriz de autorização direta nas APIs | P1 | M | Pendente | Ambiente e identidades sintéticas aprovados em futura rodada | gerenciamento-website tasks 2.1/9.1; specs/admin-dashboard; require_current_session.xs |
| CBX-004 | Administração | Validar suspensão/reativação e trilha persistida | P2 | M | Pendente | CBX-003 | gerenciamento-website tasks 3.2/3.3; admin_users_id_status_PUT.xs |
| CBX-005 | Moderação | Validar revisão de reports sem alterar alvo | P2 | M | Pendente | CBX-003; política de transições a confirmar | gerenciamento-website tasks 5.2–5.4; admin_reports_id_PUT.xs |
| CBX-006 | Catálogo admin | Concluir validação de filtros, páginas e edição | P2 | M | Pendente | CBX-003 | gerenciamento-website tasks 4.1/4.2; admin_catalog*.xs |
| CBX-007 | Desempenho | Completar baseline e comparação da jornada principal | P1 | M | Pendente | Orçamento por cenário; CBX-001 para ciclo de recuperação completo | otimizar-performance-app tasks 1.3–1.5, 3.5, 4.4, 9.x |
| CBX-008 | Biblioteca/listas | Validar escala e isolamento de duas contas | P2 | M | Pendente | Coleções sintéticas aprovadas; CBX-007 fornece orçamento | otimizar-performance-app tasks 6.2–6.4; test_library_pagination.py |
| CBX-009 | Dashboard admin | Completar verificação de agregados e jornada visual | P2 | M | Pendente | CBX-003; CBX-005 para cenário integrado de reports | gerenciamento-website tasks 2.2/2.3/9.2; admin_dashboard_GET.xs |

Links-base de evidência: [recuperação](../../openspec/changes/recuperar-senha-codigo-6-digitos/tasks.md), [administração](../../openspec/changes/gerenciamento-website/tasks.md), [performance](../../openspec/changes/otimizar-performance-app/tasks.md), [specs consolidadas](../../openspec/specs/). Contagens verificadas: 8/10, 22/34 e 14/37 respectivamente. Não encerrar tasks amplas por entregar apenas um incremento deste backlog.

## Detalhamento das tarefas confirmadas

### CBX-001 — Recuperação com entrega comprovada

Problema/objetivo: recuperação implementada, mas sem chegada real e ciclo completo aceitos. Requisito aprovado: change recuperar-senha-codigo-6-digitos; não se trata de criar recuperação. Escopo mínimo: concluir 3.4 (envio aceito) e depois 3.2 (recebimento/uso), em duas verificações separadas. Aceite: caixa controlada recebe código; troca permite novo login, senha anterior e reuso são rejeitados; registrar restauração segura e resultados por camada. Estado Bloqueada sustentado pela evidência de 28/10 sobre elegibilidade do destinatário, não por alegação de falha atual do serviço. Componentes estimados: state/session.py, pages/account.py, reset/*.xs e tools/password_recovery_remote.py. Riscos/testes sugeridos: cooldown, tentativas e isolamento; mocks antes de qualquer teste real expressamente autorizado. Não iniciar serviços/envios nesta auditoria.

### CBX-002 — Continuidade do feed

Problema/objetivo: _refresh_posts solicita per_page=20, mas _request_pages só continua se len==page*100. A página cheia de 20 termina sem ler a seguinte; garantir acesso aos posts disponíveis previstos em “Display followed user activity”. Escopo mínimo: tornar continuação coerente com tamanho solicitado, preservando token, ordem, identidade e guardas; sem impor desenho de paginação antecipadamente. Aceite: casos 0, 19, 20, 21 e 41 posts, todos acessíveis sem duplicação; parâmetros/token preservados e troca de sessão aborta leitura obsoleta; falha na continuação informa erro/permite recuperação sem mistura entre contas. Componentes estimados: state/social.py, testes de feed/paginação, feed_GET.xs e posts_GET.xs se o contrato exigir ajuste. Risco: corrigir automaticamente todos os leitores pode aumentar chamadas; verificar orçamento. Teste sugerido: transporte inteiramente simulado com páginas de 20 e 100. Vínculo: performance 7.2; qualquer implementação precisa revisar cobertura da change ativa ou propor change pequena após autorização. Não confundir com CB-MT-006 vazio inicial.

### CBX-003 — Matriz de autorização administrativa

Problema/objetivo: critérios completos de 2.1/9.1 ainda abertos; o código contém guards, não há bypass comprovado. Escopo mínimo: uma matriz por endpoint e papel, começando por leituras, depois negativas de mutação sem efeitos; lacunas demonstradas viram correções próprias. Aceite: visitante, membro, admin ativo, admin desativado, token revogado e credencial de reset têm respostas esperadas diretamente na API; nenhuma rejeição devolve dados protegidos nem grava; ator não é controlado por payload. Componentes estimados: xano/api/codeboxd/admin_*.xs, função de sessão, tests/test_admin.py/test_session_revocation.py e tools/admin_reads_remote.py. Dependência operacional: ambiente isolado e identidades sintéticas autorizadas. Risco: scripts históricos podem acessar contas reais; revisar antes de executar. Testes sugeridos: mocks/contratos, depois ambiente controlado autorizado; sem conceder admin automaticamente.

### CBX-004 — Suspensão e auditoria

Problema/objetivo: tasks 3.2/3.3 abertas apesar de endpoint/UI existentes. Escopo mínimo: ciclo active→disabled→active com trilha, usando usuário sintético em futura execução isolada. Aceite: estado persistido, sessão suspensa rejeitada em operações protegidas, outra conta preservada; log contém ator autenticado, alvo, status anterior/novo e motivo; cancelamento na UI não grava. Componentes estimados: admin.py, pages/admin.py, admin_users_id_status_PUT.xs, event_log e testes admin. Dependência CBX-003; risco de bloquear conta real ou deixar estado residual, exigindo plano de restauração em rodada própria. Testes sugeridos: negativos locais e integração isolada; não repetir busca de usuários já concluída como se estivesse ausente.

### CBX-005 — Reports

Problema/objetivo: fila/transições/integridade têm código, mas aceite completo de 5.2–5.4 não encerrado. Escopo mínimo: validar filtros/páginas; em incremento seguinte, decisões com trilha e alvo preservado. Aceite: filtros por tipo/status/motivo coerentes, vazio distinto de erro; decisão guarda ator autenticado e status anterior; nenhum fluxo altera/exclui alvo; snapshot permanece legível se alvo não está disponível. Transições inválidas só podem ser definidas após decisão sobre grafo permitido; não inventar restrições terminais. Componentes estimados: admin.py, pages/admin.py, admin_reports*.xs, report/event_log e tests/test_admin.py. Dependência CBX-003; cenário de política depende da equipe. Riscos: texto sensível e decisões concorrentes; testes sugeridos com snapshots fictícios e falhas controladas. Não criar mensageria.

### CBX-006 — Catálogo administrativo

Problema/objetivo: 4.1/4.2 aguardam critérios integrais, sem ausência de endpoints. Escopo mínimo: validar leitura/paginação por quatro tipos; depois edição dos campos já autorizados. Aceite: filtros/consulta respeitam tipo e continuidade; edição válida persiste sem mudar IDs/referências; erro preserva registro; identidade externa duplicada reutiliza/rejeita conforme contrato existente. Componentes estimados: admin.py, pages/admin.py, admin_catalog*.xs, media e testes admin. Dependência CBX-003. Risco: alterar catálogo real ou confundir legado titulos; testes sugeridos em dados sintéticos, sem importar massa externa. Prevenção de duplicatas 4.3 já concluída é regressão, não nova entrega.

### CBX-007 — Desempenho da jornada

Problema/objetivo: otimizações e comparações pontuais existem, faltam critérios completos de baseline/metas/429 e navegador. Escopo mínimo por incrementos: (a) baseline/budget de Home→busca→ficha; (b) sessão/biblioteca/social; (c) comparação integrada. M é por incremento; o conjunto não é uma única implementação pequena. Aceite: pelo menos cinco amostras frias/quentes por cenário em desktop/celular, mediana/pior caso/contagens por serviço, endpoint sanitizado e Retry-After em 429, orçamento aprovado e comparação antes/depois; registrar limites e separar handlers, remoto e browser. Componentes estimados: tools/performance_*, services/catalog.py/api.py e state/social.py/session.py somente se intervenção for demonstrada. Dependência de orçamento; ciclo completo de recuperação depende CBX-001, mas medição pública pode começar sem ela. Riscos: rate limit e instrumentos que reiniciam app; revisar ferramentas e autorizar execução própria. Não declarar a Home regressiva só pelo relato nem refazer 4.1–4.3 concluídas.

### CBX-008 — Biblioteca e listas em escala

Problema/objetivo: validação real documentada tem primeira página pequena e não fecha continuação/duas contas/coleções grandes em 6.2–6.4. Escopo mínimo: leitura de biblioteca paginada; depois listas e mutações autorizadas, sem duplicar entrega funcional arquivada 11/11. Aceite: todos os itens acessíveis, ordem e totais coerentes, listas próprias privadas isoladas, descoberta pública sem vazamento; duas contas independentes, erro/retry preservam contexto; mutação não duplica e reflete confirmação. Componentes estimados: _load_library_page/load_lists, library_GET.xs, lists*.xs e tests/test_library_pagination.py/test_personal_lists.py. Dependência CBX-007 para comparação de tempo, não para testes de integridade. Riscos: carga excessiva e limpeza de fixtures; testes sugeridos: coleções sintéticas grandes em mocks antes do ambiente controlado. Default_key e separação própria/pública são regressões obrigatórias.

### CBX-009 — Dashboard e visual administrativo

Problema/objetivo: agregados, pendências e jornada visual ainda têm critérios abertos em 2.2/2.3/9.2. Escopo mínimo: comprovar contagens conhecidas e paginação; depois navegar no browser em desktop/celular com vazio/falha parcial. Aceite: totais correspondem aos dados sintéticos, fontes que falham ficam indisponíveis sem zero inventado; atividades/reports abrem contexto correto; páginas continuam acessíveis, sem vazamento de segredos e com navegação legível a 1440/390px. Componentes estimados: AdminState.load_dashboard, pages/admin.py, admin_dashboard_GET.xs e tests/test_admin_dashboard_remote.py. Dependência CBX-003, CBX-005 só para fechamento integrado de reports. Risco: validar UI com fixtures e atribuir resultado ao remoto; separar evidências. Busca admin 3.1 com 79 checks é entrega preservada, não pendência nova.

## Ordem inicial recomendada

1. Escolher CBX-002 para primeiro incremento pequeno, com regressão local sintética; em paralelo de planejamento, resolver elegibilidade de CBX-001, sem enviar e-mail nesta etapa.
2. Completar CBX-003 antes de executar mutações administrativas de CBX-004/005/006. As leituras existentes já têm evidências parciais; ampliar só onde faltam critérios.
3. Medir o recorte público de CBX-007, depois biblioteca/social e CBX-008. CBX-009 pode validar métricas após autorização sem aguardar todas as mutações, mas aceite integrado de reports espera CBX-005.

Sem ciclos: orçamento precede comparação, matriz de acesso precede mutações, relações de follow precedem aceite integrado do relato de feed. O restante segue prioridade e disponibilidade, sem tratar ausência de acesso como defeito de produto.

## A verificar e sugestões — fora das tarefas confirmadas

| Referência | Natureza | Evidência / próximo esclarecimento |
| --- | --- | --- |
| CB-MT-001 | Relato/hipótese | Home lenta; medir versão/ambiente. Relacionado CBX-007, sem criar segunda tarefa de otimização |
| CB-MT-002 | Relato + constatação estática | Mensagem específica descartada no transporte; silêncio total não explicado. Confirmar HTTP e evento antes de decidir correção |
| CB-MT-003 / P.3 | Relato/hipótese | Banner local; comparar URL/arquivo/versão com teste histórico, sem declarar armazenamento remoto ausente como requisito |
| CB-MT-004 | Informação insuficiente | Identificar primeiro controle, esperado e observado; risco de quick_add parcial ainda não reproduzido |
| CB-MT-005 | Relato/hipótese | Identificar dois alvos divergentes e relação persistida; não há seletividade explicada no remoto |
| CB-MT-006 | Relato/hipótese | Falha auxiliar ou relação é hipótese; CBX-002 comprova outro defeito de continuidade, não vazio inicial |
| P.7 | Contrato remoto a verificar | Último /likes registrado ausente, mas fallback existe; não publicar rota automaticamente nem afirmar endpoint inexistente hoje |
| Capa/sinopse 390px | Candidato a revisão | PENDENCIAS registra pendência visual histórica; reproduzir na versão atual antes de confirmar regressão |
| CI do produto | Sugestão de processo P3, tamanho P | Workflow atual apenas prepara OpenSpec; equipe decide se aprova execução automática de testes offline |
| Acessibilidade integral | Sugestão de validação | Há labels/roles e responsividade parcial; acordar critério/escopo antes de gerar requisitos de conformidade |
| P.9 modularização | Dívida condicional | Estado/página social extensos; sem refatoração aprovada nem defeito por tamanho apenas |
| P.11 scripts históricos | Cuidado operacional | Rever destinos/portas/efeitos antes de reutilizar; não executar restauração/publicação incidentalmente |

Entregas preservadas, fora da fila: P.1/P.2/P.4/P.5/P.8/P.13, listas padrão 11/11, meias estrelas e DeepL arquivados. Chat, notificações, ML, hospedagem/domínio e Docker continuam fora da etapa; não são tarefas aprovadas. Nenhum requisito encontrado foi rotulado “não implementado” apenas por busca inicial negativa.

## Decisões objetivas da equipe

- Qual caixa controlada será elegível para concluir CBX-001 em rodada com autorização específica?
- Priorizar primeiro CBX-002 (continuidade social) ou CBX-003 (fechamento de acesso administrativo)?
- Qual versão e sequência reproduzem cada relato CB-MT, principalmente o primeiro controle de listas?
- Quais tempos/chamadas são aceitáveis por jornada e quais volumes sintéticos representam uso esperado?
- Reports podem sair de resolvido/rejeitado? Aprovar política antes de transformar essa dúvida em regra de backend.

## Registro e verificações — 29/10/2026

Ampliada auditoria de seis relatos para produto inteiro no alcance estático descrito; adicionados nove índices CBX rastreáveis, estimativas, aceite e dependências. Preservados integralmente os IDs e conteúdo anteriores abaixo, com classificação atual esclarecida acima. Nenhuma task OpenSpec ou decisão histórica foi alterada. Itens concluídos não foram reabertos por contagem antiga em prosa.

Executados apenas leitura/busca, git status/branch/rev-parse/log, listagem OpenSpec e revisão documental. Não executados testes, compile, browser, chamadas Xano ou instalação. Conferência final: 684 hashes comparáveis fora dos dois documentos iguais (snapshot inicial truncado, sem cobertura total), estados Git/branch/HEAD preservados; links locais e nove IDs CBX únicos conferidos sem criar artefatos. `git diff --check` passou com aviso de LF/CRLF no arquivo preexistente; documentos não rastreados conferidos separadamente. Não há dependências circulares identificadas. Próximo passo: escolher um item, fazer Explore → Propose quando necessário → revisão → Apply → Verify → sincronização/Archive quando autorizados e critérios atendidos; tarefas já cobertas continuam na change existente. Esta auditoria termina no planejamento.

## Backlog anterior dos relatos manuais (preservado)

Fonte e evidências por ID: [auditoria](codeboxd-auditoria.md). Registro OpenSpec: [auditar-relatos-testes-manuais](../../openspec/changes/auditar-relatos-testes-manuais/tasks.md). Todos os bugs permanecem abertos; nenhum reproduzido tecnicamente nesta sessão. IDs deste lote não substituem os IDs históricos de openspec/PENDENCIAS.md.

P1 = alto impacto na jornada; P2 = impacto localizado ou relato que precisa de precisão. Prioridades provisórias, sem P0 comprovado.

| Ordem | ID / problema | Prioridade | Situação / dependência | Proposta de change futura (não criada) |
| --- | --- | --- | --- | --- |
| 1 | CB-MT-005 Seguir falha por alvo | P1 | Não reproduzido; base das relações do feed | corrigir-consistencia-seguir-usuarios |
| 2 | CB-MT-006 Feed exige publicação aparente | P1 | Não reproduzido; validar vínculo do item 005 antes do aceite integrado | corrigir-carga-inicial-feed |
| 3 | CB-MT-002 Nome duplicado sem feedback | P1 | Não reproduzido; perda da mensagem específica constatada | informar-username-indisponivel |
| 4 | CB-MT-001 Home lenta | P1 | Não reproduzido; comparar com performance existente | reduzir-espera-home-medida |
| 5 | CB-MT-003 Banner não carrega | P2 | Não reproduzido; URL/arquivo local | corrigir-entrega-banner-perfil |
| 6 | CB-MT-004 Primeiro filtro de listas | P2 provisória | Informação insuficiente; identificar controle antes de definir correção | corrigir-controle-inclusao-listas |

## Critérios e escopo das propostas

### CB-MT-005
Investigar matriz de alvos que funcionam/falham, comparar profile.user_id/user.id e resposta do PUT; corrigir somente divergência demonstrada. Aceite: duas contas, relação única persistida, interface e reabertura coerentes; auto-seguimento negado, alvo inexistente tratado, sessão inválida negada, cliques repetidos sem duplicação; deixar de seguir continua funcionando. Registrar HTTP e estado antes/depois sem tokens. Nenhuma reparação massiva de dados sem inventário e plano separado.

### CB-MT-006
Isolar dependências auxiliares da leitura principal caso a reprodução confirme bloqueio; tratar vazio e erro separadamente. Aceite: conta A sem publicação segue B com post existente e vê conteúdo no primeiro acesso e após recarga; unfollow remove e novo follow restaura sem A publicar. Induzir falhas de perfis, catálogo, posts próprios e likes e verificar feedback/recuperação; testar 21+ posts para continuação sem omissões/duplicatas; preservar autorização, curtidas, edição e comentários das changes recentes. Pode ser investigado em paralelo com 005, mas aceite integrado depende de relações confiáveis.

### CB-MT-002
Mapear conflito de username por contrato seguro e explícito; não exibir indiscriminadamente corpo remoto. Aceite: nome ocupado em profile e legado user rejeitado com aviso visível; dados anteriores preservados, rascunho utilizável; nome atual permitido, nome livre salvo; validação HTML e backend distinguíveis, sessão inválida tratada. Login/cadastro devem continuar funcionando, sem mudar suas regras.

### CB-MT-001
Medir primeiro conteúdo, página utilizável e conclusão, cache frio/quente, desktop/celular, quantidade de chamadas e imagens. Definir orçamento antes de corrigir. Aceite: comparação antes/depois no mesmo cenário, meta acordada atendida, conteúdo progressivo preservado, falha lenta de um provedor não apaga demais fileiras, sem aumento de 429 ou regressão de busca. Antes de criar esta proposta, reconciliar com tarefas 4.x e 9.x de otimizar-performance-app: preferir continuar o escopo existente se suficiente; não duplicar otimizações nem usar a amostra histórica como aceite atual.

### CB-MT-003
Capturar URL gerada, status GET, content-type e presença do arquivo sem registrar dados privados. Aceite: PNG/JPEG/WEBP/GIF válido até 5 MB carrega no próprio perfil e em outra conta após recarga e reinício local; entrada inválida e falha de persistência apresentam erro; outro usuário não pode substituir banner; frontend não fica com imagem quebrada silenciosa. Escolher intervenção de URL/armazenamento apenas após diagnóstico, sem ampliar para infraestrutura ou Docker.

### CB-MT-004
Obter nome do controle, sequência, destino esperado e resultado antes de criar a change corretiva. Se for atalho planned, verificar escrita parcial entre interação e item; se for seletor, verificar primeira opção, placeholder e destino. Aceite: primeira e demais opções funcionam por mouse/teclado em desktop/celular; placeholder não envia; somente listas próprias aparecem, homônimas respeitam ID/default_key; falha tem aviso, repetição não duplica, mídia correta persistida e estado final consistente. Se houver escrita em lista errada ou perda, elevar prioridade antes de seguir a fila.

## Sequência de execução após autorização

1. Recolher versão/ambiente e evidência sanitizada do testador, identificar controle de listas e dois perfis divergentes; reproduzir sem inferir sucesso remoto do código local.
2. Confirmar persistência/autorização de follow e então executar cenário integrado do feed sem posts próprios. Criar uma change pequena por correção comprovada, com planejamento antes de código.
3. Corrigir feedback de username; medir e tratar Home coordenando change de performance.
4. Tratar entrega do banner e controle de listas conforme reprodução, ajustando prioridade ao impacto constatado.
5. Em cada change, registrar testes locais/simulados, remoto e navegador separadamente; regressão de login, cadastro, unfollow e funcionalidades tocadas. Não marcar critério sem evidência. Sem Docker; usar .venv e skill de processos se for necessário executar Reflex.

Esta fila é proposta, não autorização de implementação. Sem changes corretivas criadas, commits, PRs ou alterações de produto nesta rodada.
