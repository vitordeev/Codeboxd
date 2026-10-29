# Auditoria técnica e de produto do Codeboxd — 29/10/2026

## Ampliação da auditoria — escopo e autorização

Branch examinada: `develop`; commit `daec853818195558cc6d4d8ebf588ba839b27cd7`. Snapshot inicial: `M reflex.lock/package.json`, `?? docs/planning/` e `?? openspec/changes/auditar-relatos-testes-manuais/`. Todos são trabalho anterior a esta ampliação. O usuário autorizou expressamente a exceção ao AGENTS.md: atualizar somente este arquivo e o backlog, sem criar ou alterar change. A change anterior continua restrita aos seis relatos; não cobre nem autoriza implementar o backlog completo abaixo. Nenhuma funcionalidade foi modificada.

### Arquitetura observada

- `Codeboxd_main/Codeboxd_main.py` registra rotas públicas, conta, obra, biblioteca, comunidade, listas, feed e administração, com eventos on_load. `rxconfig.py` configura o app. `requirements.txt` fixa Reflex 0.9.11.post1, httpx 0.28.1 e python-dotenv 1.2.3; requirements-dev inclui Playwright 1.64.0. Não foram instaladas ou verificadas versões efetivas do ambiente nesta rodada.
- `state/session.py` mantém identidade validada por `/auth/me`, Cookie ou SessionStorage e cache curto de navegação para membro; `state/social.py` concentra descoberta, avaliações, relações, listas e posts; `state/admin.py` mantém estados e guardas administrativos.
- `services/api.py` transporta JSON para grupos Xano configurados por ambiente; `services/uploads.py` transporta multipart; `services/catalog.py` integra TMDB, Kitsu e Open Library, normalização de identidade e cache. Jikan é identidade legada mapeada, não provedor atual de busca. `services/translation.py` oferece tradução opcional com cache local.
- `xano/table/` versiona user/profile/media/interações/listas/itens/follows/posts/likes/comments/report/event_log. Identidades e índices únicos existem, por exemplo em user_follow.identity_key, profile.username e user_list.default_key. `xano/api/` e `xano/function/security/require_current_session.xs` documentam sessão versionada e autorização. Arquivo local não prova contrato publicado.
- Banner grava bytes localmente e persiste URL em profile; post usa transporte multipart. APIs de conteúdo não se confundem com o catálogo legado titulos. Execução canônica é local com .venv, sem Docker; persistência e URL de uploads exigem cuidado operacional conforme openspec/AMBIENTE.md.

### Estado por módulo

“Implementado” indica código/contrato e evidência histórica identificados; não certifica execução atual. “Parcial” pode significar critério de validação ainda aberto, mesmo com código existente.

| Módulo | Estado observado | Evidência e limites |
| --- | --- | --- |
| Cadastro/login/logout/sessão | Implementado | session.py; specs/user-authentication; tests/test_authentication.py e test_session_revocation.py; relatos positivos e histórico, sem reexecução atual |
| Recuperação de senha | Parcial | Change recuperar-senha-codigo-6-digitos 8/10; contrato publicado segundo histórico, envio aceito/recebimento e ciclo completo ainda bloqueados |
| Perfil e edição | Implementado; relatos a verificar | save_profile e _profile_updates; spec user-profile; tests/test_profile_performance.py; CB-MT-002/003 não reproduzidos |
| Catálogo: filmes e séries | Implementado | catalog.py tmdb_item/search_one/detail/availability; specs media-catalog/media-data-integration; disponibilidade externa variável |
| Catálogo: anime e livro | Implementado | kitsu_item/book_item/detail e tests/test_kitsu.py; mapeamento legado explícito, não presumir igualdade de IDs |
| Busca/descoberta | Implementado; validação de performance parcial | specs/media-discovery, tests/test_search_lifecycle.py e test_search_relevance.py; performance 4.4 aberta |
| Avaliações/resenhas/biblioteca | Implementado; escala e jornada parcial | specs/media-interactions; save_interaction, _load_library_page; tests/test_review_identity.py, test_review_submission.py, test_library_pagination.py |
| Listas próprias/públicas | Implementado; performance parcial | Change arquivada corrigir-duplicacao-listas-padrao 11/11, conclusão com API/browser históricos; tests/test_personal_lists.py; relato CB-MT-004 indeterminado |
| Seguir/deixar de seguir | Implementado; falhas relatadas a verificar | follows*.xs, SocialState.follow; specs/social-connections; não há causa remota comprovada para CB-MT-005 |
| Feed/posts/likes/comentários | Implementado; lacuna estática de paginação e validação parcial | _refresh_posts/_request_pages; changes recentes com testes locais e limites; CBX-002 e CB-MT-006 são assuntos relacionados, mas distintos |
| Recomendações e tradução | Implementado no escopo existente | catalog.recommendations, translation.py, spec description-translation; não é recomendação por aprendizado de máquina |
| Administração/dashboard/moderação | Parcial | gerenciamento-website 22/34; telas, contratos, guards e logs existem; completar matriz de autorização, mutações, agregados e browser real |
| Responsividade/acessibilidade | Parcial / cobertura a verificar | Histórico de fixtures em 1440/390px, labels/roles no código; revisão visual mais recente não executada; sem auditoria integral de teclado/leitor de tela |
| Operação/testes | Parcial | tests/ e ferramentas extensas; dependências diretas fixadas; único workflow encontrado prepara OpenSpec, não roda regressão do produto |
| Chat/notificações/ML/hospedagem | Não implementado no escopo examinado / fora da etapa | openspec/PENDENCIAS.md e design administrativo excluem mensageria e ML; não converter em requisitos aprovados |

### Requisitos, evidências e divergências

1. As specs consolidadas aprovam cadastro, identidade única, sessão, descoberta dos quatro tipos, status, nota decimal, resenha própria, listas, conexões, feed e interações. Os deltas administrativos aprovam painel, gestão e reports. Ausência de chat não é lacuna de entrega; report `message` usa snapshot sem criar mensageria.
2. Checklists abertos não significam ausência de implementação: os PUTs administrativos já verificam ator ativo/admin, mantêm transação e log. Faltam critérios completos de execução e evidência. Não há prova nesta análise de acesso indevido; CBX-003 é fechamento de validação de segurança, não vulnerabilidade confirmada.
3. Resumos centrais de 27/10 citam três changes funcionais; listagem atual inclui também três entregas locais de feed ainda não arquivadas e auditoria documental. `complete` no CLI mede checklist, não publicação ou aceite real. O design administrativo conserva contagem antiga 21/34 em texto histórico, enquanto tasks/list atuais mostram 22/34; usar checklist/evidência datada, sem apagar história.
4. `docs/planning` é apresentação solicitada; OpenSpec segue fonte das decisões existentes. A ampliação não modifica tasks, specs nem suas contagens, por exceção expressamente autorizada.
5. Defeito estático independente: `_request_pages` compara tamanho com 100, mas feed/posts enviam per_page=20; com 20 registros retornados não solicita página 2. CBX-002 registra o defeito demonstrável pelo controle de fluxo, sem afirmar que explica o feed vazio do testador. Biblioteca com contrato/cursor próprio tem testes específicos e não deve ser tratada como o mesmo defeito.
6. A documentação registra banner corrigido em rodada anterior e testes de URL, enquanto o testador relata falha. Ambos são preservados: não se pode concluir regressão ou invalidar o histórico sem comparar versão e resposta real.
7. Infraestrutura de teste existe; não há base para tarefa genérica “criar testes do projeto”. O workflow Copilot apenas instala/verifica OpenSpec e dispara quando ele próprio muda. CI do produto seria sugestão de processo a aprovar, não requisito documentado ausente.

### Fluxos e riscos sustentados pelas fontes

Há evidência histórica de login/sessão, biblioteca com primeira página real, listas com duas contas, buscas admin com 79 checks, rotação de credenciais e revogação em 39 rotas. São registros anteriores, não verificações executadas agora. Publicações recentes têm 434 testes históricos locais registrados em corrigir-upload-imagem-feed/validation.md; essa entrega não executou browser/upload real. reposicionar-card-obra-feed registra compilação, mas não revisão visual em browser.

Riscos prioritários: recuperação sem entrega real comprovada; continuidade incompleta do feed; fechamento da autorização/mutações administrativas; desempenho e 429 sem orçamento/linha de base de todas as jornadas. Os riscos locais de banner, leituras auxiliares e escrita parcial de quick_add são descritos nos seis relatos abaixo. Não foi demonstrado P0 atual nem reaberta a pendência de segredos resolvida historicamente. Configuração efetiva de cookie/URLs e estado remoto continuam desconhecidos; não inspecionados arquivos privados nem usados tokens reais.

### Cobertura, limitações e decisões

Inspecionados: instruções da raiz (nenhum AGENTS adicional encontrado na busca), README, contexto/status/pendências/histórico/ambiente OpenSpec, inventário de 19 specs consolidadas e requisitos pertinentes, tasks/propostas/designs relevantes, evidências datadas, rotas, estados, transportes, adaptadores, contratos de sessão/listas/admin e modelos relacionados; testes representativos, dependências, workflow e cinco commits recentes. Busca TODO/FIXME/NotImplemented não trouxe pendência de produção; `pass` encontrado em testes não prova fluxo ausente. Não houve leitura integral de cada arquivo do repositório nem auditoria de segurança exaustiva.

Indisponíveis/não verificados: os dois documentos overview/domain solicitados não existem; instância Xano e provedores não foram consultados; branch remota/deployment efetivo, dados, logs, mailbox, requisitos fora do repositório e execução atual da UI não foram verificados. Nenhum teste foi executado nesta ampliação: a autorização limita escrita a dois documentos, e inicialização/compile/suíte podem produzir arquivos, ler ambiente privado ou acionar ferramentas de restauração. Foram feitas leituras, buscas, comparação de checklists, git log/status e conferência documental; resultados históricos são identificados como históricos.

Decisões da equipe: escolher destinatário de teste elegível para concluir recuperação em rodada própria; priorizar validação administrativa versus jornada social; fornecer versão/passos dos seis relatos; aprovar orçamento de performance; decidir política de transições de reports (contrato aceita três destinos, design registra ausência de grafo terminal). Não presumir novas regras de produto. Sobreposição da capa/sinopse em 390px consta como pendência histórica, candidata à reprodução antes de virar defeito atual confirmado.

### Conferência desta atualização

Preservados os seis IDs CB-MT e suas análises abaixo; a classificação global atual do backlog separa esses relatos de tarefas confirmadas CBX. Apenas os dois Markdown foram editados. Conferência final: 684 hashes comparáveis de outros arquivos permaneceram iguais; a saída inicial foi truncada, portanto essa comparação não comprova todos os arquivos. Git status, branch e HEAD permaneceram iguais ao início. Links locais dos dois documentos válidos; nove IDs CBX detalhados, sem repetição. `git diff --check` passou, com aviso LF/CRLF do arquivo preexistente; por estarem não rastreados, os documentos foram conferidos separadamente. Sem criação de branches, testes, instalações, migrações, serviços externos, commits ou alterações OpenSpec. Registro de atualização: 29/10/2026, ampliação do diagnóstico de seis relatos para visão do produto e vínculos das pendências já aprovadas.

## Auditoria anterior dos seis relatos (preservada)

Registro central: [change documental](../../openspec/changes/auditar-relatos-testes-manuais/proposal.md). Correções não autorizadas nesta rodada. [Backlog e aceite](codeboxd-backlog.md).

## Método e limites

Análise estática de páginas Reflex, estados, transporte e XanoScript versionado. Nenhum dos seis sintomas foi reproduzido nesta sessão em navegador ou API real; não foram executados testes funcionais, simulados ou mutações remotas. Constatação de código não equivale à causa confirmada do incidente. Faltam versão/ambiente testado, contas e perfis envolvidos, passos precisos, horários, logs, HAR e respostas HTTP sanitizadas.

Lidos AGENTS.md, README.md, openspec/README.md, CONTEXTO.md, PENDENCIAS.md e HISTORICO.md; consultados contratos de perfil, conexões, feed e listas, planejamento/evidências de performance e histórico de correções. `docs/project-overview.md` e `docs/domain-model.md` não existem, inclusive na busca pelos nomes; contexto e modelo disponíveis no OpenSpec e xano/table foram usados como referência, sem criar substitutos especulativos. Skill reflex-docs consultada, com [documentação oficial de eventos](https://reflex.dev/docs/events/events-overview/).

Estado inicial: branch `develop`; única alteração rastreada preexistente: `reflex.lock/package.json`. Nenhuma troca de branch ou alteração desse arquivo. Nenhum Docker, commit, PR, publicação ou reinício.

## CB-MT-001 — Home lenta

**Status:** não reproduzido; indícios estáticos e medição histórica. **Prioridade:** P1.

**Esperado:** conteúdo principal progressivo e navegação utilizável, com tempo medido e falhas parciais explícitas. **Observado pelo testador:** carregamento lento, sem duração informada.

**Evidências:** `Codeboxd_main/state/social.py:666`, `_home_updates`, dispara validação de sessão, catálogo Xano, populares e coleções em paralelo e publica resultados progressivos. `visit:463` mantém busy até finalizar o carregador. `_load_home_collections:717` limita concorrência por provedor; série popular ainda consulta destaques após a busca. Há otimizações existentes: não atribuir o problema a execução inteiramente sequencial nem à ausência de cache.

`openspec/changes/otimizar-performance-app/validation/home-publica-rede-2026-10-23.json`, primeira amostra histórica: principal 809,641 ms, total 5930,25 ms, 22 requisições; explicitamente sem navegador e sem Xano medidos. Não é medição atual nem prova da latência relatada.

**Causa provável:** espera de provedores/últimas coleções e custo de carga inicial; cache frio, imagens e serialização precisam ser medidos. Não confirmada. **Arquivos:** state/social.py, services/catalog.py, services/api.py, pages/social.py, assets/codeboxd.css e rotas em Codeboxd_main/Codeboxd_main.py. **Dependências:** change ativa de performance; sem dependência funcional com seguir.

## CB-MT-002 — Username duplicado sem mensagem

**Status:** sintoma não reproduzido; perda de mensagem específica confirmada por leitura. **Prioridade:** P1.

**Esperado:** rejeitar duplicata e mostrar nome indisponível, preservando formulário e identidade anterior. **Observado:** não salva e não informa.

**Evidências:** `xano/api/codeboxd/profile_PUT.xs` verifica duplicata tanto em profile quanto em user, permite manter o próprio nome e devolve inputerror com mensagem específica. `services/api.py`, `request`, descarta corpo de erro e converte 400/422 em “Confira os dados informados.” `state/social.py:1384`, save_profile, captura APIError via `_failure:555`, que escreve notice. `pages/social.py:444` renderiza notice no editor e o shell também possui aviso. Portanto há caminho explícito de mensagem; silêncio total não está explicado apenas pela conversão genérica.

**Causa provável:** perda de especificidade do transporte contribui para feedback ruim. Para silêncio, verificar validação HTML (pattern/min/max), editor aberto, evento efetivamente enviado, status/corpo remoto e possíveis diferenças da versão em execução. **Arquivos:** os quatro acima; `xano/table/` para unicidade. **Dependências:** confirmar contrato publicado; não alterar login/cadastro nem expor corpos arbitrários do backend.

## CB-MT-003 — Banner não carrega

**Status:** não reproduzido; dependência de armazenamento local confirmada. **Prioridade:** P2.

**Esperado:** após upload válido, banner visível no perfil próprio e público e após recarga. **Observado:** imagem não carrega corretamente; etapa exata desconhecida.

**Evidências:** `state/social.py:1397`, upload_profile_banner, valida assinatura/tamanho, grava em rx.get_upload_dir()/profiles/<id>, monta URL com Endpoint.UPLOAD.get_url e envia somente banner_url ao PUT /profile. Em APIError remove o arquivo. `pages/social.py:435` usa a URL diretamente em img. `profile_PUT.xs` armazena texto; não armazena os bytes do banner no Xano. Não confundir com upload multipart de publicações, cuja correção tem change própria.

**Causa provável:** URL pública do backend incorreta/inacessível ou arquivo ausente no servidor que atende a imagem. HTTP, redirecionamento, mixed content, volume/instância e resposta efetiva precisam ser verificados. Erros de filesystem anteriores ao try também não recebem tratamento APIError; não há prova de que ocorreram. **Arquivos:** state/social.py, pages/social.py, rxconfig.py, xano/api/codeboxd/profile_PUT.xs; diretório runtime de uploads. **Dependências:** configuração efetiva de URL e persistência local; sem exigir Docker ou hospedagem nesta etapa.

## CB-MT-004 — Primeiro filtro de adicionar às listas

**Status:** informações insuficientes; não reproduzido. **Prioridade:** P2 provisória (elevar se houver escrita em destino errado).

**Esperado:** ação afetar exclusivamente o destino selecionado, com feedback e sem duplicar. **Observado:** “primeiro filtro” incorreto, sem identificar controle, valor ou resultado.

**Evidências:** `pages/social.py:341` tem primeiro atalho “Quero ver / ler”, que chama quick_add('planned',0,...); não é um filtro. Há também seletor de destino em :351. `state/social.py:1150`, quick_add, primeiro faz PUT /interactions e depois POST /lists/<id>/items, sem transação entre eles; uma falha no segundo pode deixar alteração parcial. Isso é risco constatado, não ocorrência confirmada. `select_media_list:2059` só aceita IDs existentes e não permite voltar ao placeholder vazio; verificar se esse é o sintoma. `open_media_lists:2064` filtra destinos pelo proprietário.

**Causa:** indeterminada até identificar controle e passos. **Arquivos:** pages/social.py, state/social.py, xano/api/codeboxd (listas, itens, interações). **Dependências:** respeitar identidade default_key e separação de listas próprias/públicas entregues na change arquivada corrigir-duplicacao-listas-padrao; não reabrir histórico como autorização.

## CB-MT-005 — Falha ao seguir alguns usuários

**Status:** não reproduzido; variação por alvo sem dados suficientes. **Prioridade:** P1, primeira investigação social.

**Esperado:** seguir alvo existente, sem auto-seguimento/duplicata; refletir confirmação e erro útil. **Observado:** alguns perfis funcionam, outros falham.

**Evidências:** `state/social.py:1430`, follow, decide PUT/DELETE por following_ids, atualiza somente após resposta e captura APIError. Não há trava de requisição concorrente. `load_community:1276` limpa IDs e tenta recuperar seguindo do perfil próprio, tolerando 404. `profiles_user_id_GET.xs` exige registro profile; `profiles_GET.xs` lista profiles. `follows_user_id_PUT.xs` valida sessão/ator ativo, existência de user alvo e auto-seguimento, e faz upsert de user_follow por identity_key. O alvo é validado em user, não somente em profile. A regra local não explica seletividade sem examinar os registros/respostas envolvidos.

**Hipóteses a verificar:** profile órfão ou IDs inconsistentes, estado following_ids incompleto após falha de leitura, dados legados de identidade e cliques concorrentes; erros 401/403/404/429 também devem ser distinguidos. Nenhuma hipótese confirmada no remoto. **Arquivos:** state/social.py, services/api.py, profiles*_GET.xs, follows_user_id_PUT.xs e DELETE.xs, xano/table/user_follow.xs. **Dependências:** CB-MT-006 consome essas relações. Manter deixar de seguir como regressão obrigatória, sem alterar sua regra sem necessidade.

## CB-MT-006 — Feed aparece após publicação própria

**Status:** não reproduzido; caminhos de carga diferentes confirmados. **Prioridade:** P1.

**Esperado:** conta sem posts próprios vê posts existentes de seguidos ao abrir feed; não precisa publicar para inicializar. **Observado:** seguir/deixar de seguir/seguir não trouxe conteúdo; publicar trouxe.

**Evidências:** `xano/api/codeboxd/feed_GET.xs` faz join post.user_id = user_follow.followed_id e filtra follower_id autenticado; não exige post do leitor. `state/social.py:1483`, load_feed, zera posts e aguarda `_load_reference:645` (catálogo e perfis completos) antes de `_refresh_posts:1441`. Uma falha dessas referências impede a consulta do feed. `_refresh_posts` só monta posts após GET /feed, GET /posts próprios e GET /likes; apenas 404 de likes é tolerado. Assim uma leitura auxiliar pode impedir exibição de dados válidos. `save_post:1566` chama diretamente `_refresh_posts` após sucesso, sem repetir a carga de referências. Isso é compatível com recuperação por nova tentativa após falha inicial, não prova causal.

`_call:563` usa cache de 15 segundos por token e parâmetros, invalidado antes e depois de mutações, inclusive follows. `follow` não recarrega posts diretamente. Portanto “cache nunca invalidado” não é diagnóstico sustentado. Há ainda risco independente: `_request_pages:601` testa tamanho de página fixo 100, mas /feed e /posts são pedidos com per_page=20; pode omitir continuação. Não explica sozinho o feed inicial vazio.

**Causa provável:** falha transitória/auxiliar na carga inicial ou relações não persistidas corretamente; ordem de chamadas e respostas reais decidirá entre elas. **Arquivos:** state/social.py, services/api.py, feed_GET.xs, posts_GET.xs, follows*.xs, profiles*.xs. **Dependências:** validar CB-MT-005 primeiro com duas contas, depois isolar leitura/renderização; publicação própria não é requisito do contrato local.

## Reconciliação com trabalho existente

`openspec list --json` nesta sessão: performance 14/37, gerenciamento-website 22/34, recuperação 8/10; corrigir-publicacoes-foto-interacoes 6/6, corrigir-upload-imagem-feed 4/4, reposicionar-card-obra-feed 3/3 ainda em changes/. “Complete” do checklist não comprova versão implantada. Nenhuma change existente cobre esta auditoria documental como entrega própria. Não alteradas contagens históricas nem criadas changes corretivas.

Login, cadastro e deixar de seguir: aprovados apenas pelo testador. Não revalidados tecnicamente aqui; preservar e incluir na regressão futura. Não há evidência para P0, indisponibilidade geral ou perda de dados. As propostas e critérios futuros estão no backlog.
