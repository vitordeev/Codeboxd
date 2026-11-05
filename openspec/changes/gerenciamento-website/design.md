> Estado reconciliado em 26/10/2026: 21/34 tarefas concluídas, 13 abertas. Tabela report e endpoints publicados em 13–19/10; interface com fixtures em 22/10. Leituras admin reais de 23/10 constam na change de performance. Faltam critérios completos de autorização, mutações, auditoria e browser real; não arquivar. As seções e rodadas anteriores abaixo preservam o planejamento e sua evolução; o checklist e a evidência datada prevalecem sobre resumos antigos.

## Context

Ver `proposal.md` para a motivação e `specs/` para os contratos observáveis. Revisão em 13/10/2026: a rota `/admin` já apresenta dashboard, e existem páginas/estado para usuários, catálogo e reports, além de `/admin/login`. A sessão confirma o papel por `/auth/me`. Contratos locais Xano existem e foram reconhecidos em dry-run histórico, mas publicação e autorização direta precisam de evidência remota. O catálogo social separa registros persistidos de dados externos. Estado por tarefa: `validation/revisao-2026-10-13.md`.

## Goals / Non-Goals

**Goals:**

- Concluir a validação da área administrativa já implementada localmente, com navegação consistente e módulos por domínio.
- Manter autorização no backend para toda consulta ou mutação, usando a identidade autenticada e o papel confirmado.
- Reutilizar tabelas, identificadores, serviços e estados já existentes quando apropriado.
- Registrar ações de moderação e gerenciamento que alterem o estado de contas ou reports.

**Non-Goals:**

- Criar uma aplicação de mensagens privadas ou um chat.
- Substituir os provedores externos do catálogo ou replicar seus catálogos integralmente no Xano.
- Dar permissão administrativa a contas automaticamente ou alterar a política de atribuição do papel `admin`.
- Excluir automaticamente conteúdo em resposta a um report.

## Decisions

### Retomada local em 03/11/2026 — contexto das confirmações

Nas tarefas 3.2, 4.2, 5.3 e 9.1, fixar token, alvo e campos da confirmação
antes do primeiro yield dos eventos de suspensão, edição e revisão. Revalidar
esse contexto após a autorização e após a escrita: cancelar antes do PUT se
o formulário/sessão mudou e ignorar respostas/erros antigos depois do PUT.
Não redirecionar, limpar sessão nova, fechar outro editor ou recarregar dados
por resposta de uma confirmação anterior. Testes com mudanças controladas
durante os awaits; sem publicação Xano ou conclusão dos critérios remotos.

- **Usar a área `/admin` já existente como ponto de entrada.** Ela já é protegida no carregamento pela sessão Reflex. Cada endpoint administrativo no Xano também verificará o papel, porque ocultar uma rota ou botão no cliente não autoriza a operação. Alternativa considerada: criar um app separado; isso duplicaria autenticação, navegação e configuração sem necessidade atual.
- **Criar `/admin/login` como entrada visual própria e reaproveitar `SessionState`.** O formulário usa o mesmo provedor, token e validação `/auth/me` do login comum. O evento dedicado rejeita e limpa a sessão quando o papel confirmado não é `admin`; `/admin` redireciona visitantes para `/admin/login` e continua bloqueando membros. Alternativa considerada: duplicar credenciais ou endpoints de login para administradores; isso criaria sessões e regras inconsistentes.
- **Separar endpoints administrativos por domínio e manter payloads mínimos.** Dashboard, usuários, catálogo e reports terão contratos próprios, retornando apenas dados necessários às telas. Operações administrativas devem obter o ator de `$auth.id`, não de identificadores enviados pelo cliente. Alternativa considerada: um endpoint genérico de administração; foi rejeitada por concentrar autorização e validação difíceis de revisar.
- **Definir relatórios como registros persistidos com snapshot contextual do alvo.** Guardar tipo/ID do alvo, conteúdo contextual necessário, motivo, denunciante, status e timestamps permite analisar reports mesmo quando o alvo muda ou desaparece. Decisões e transições devem registrar o ator. Um snapshot reduz dependência de um módulo de mensagens que ainda não existe, sem criar conversas ou mensagens.
- **Usar o catálogo existente e identidades externas para prevenir duplicatas.** As telas organizam resultados por `media_type`; correções administrativas devem preservar a identidade local e as referências do provedor. Dados de provedor não devem ser copiados em massa só para alimentar o dashboard.
- **Limitar correções aos campos administrativos estáveis já persistidos.** O levantamento inicial mapeará os campos existentes por tipo e a interface permitirá editar apenas esses campos, sem tentar substituir metadados controlados por provedores externos. Isso mantém o escopo determinístico sem assumir um modelo novo para o catálogo.
- **Calcular indicadores com agregações do backend.** O dashboard usará endpoints agregados paginados ou consultas de contagem no Xano, nunca listas completas de registros no navegador para calcular totais. Se uma fonte falhar, a UI mostrará erro localizado sem inventar valores.
- **Manter suspensão e remoção como ações separadas e auditáveis.** A primeira entrega suspende/reativa conforme `account_status`; conteúdo denunciado não é removido por registrar um report. Qualquer exclusão de conteúdo deve ser uma ação administrativa explícita, autorizada, confirmada e registrada.
- **Usar os estados de conta existentes.** O esquema Xano atual define `active` e `disabled`; suspensão usa `disabled` e reativação retorna para `active`. A política de autenticação já recusa contas `disabled`, então os endpoints de gerenciamento devem preservar esse comportamento.
- **Não assumir moderação de mensagens ao vivo.** O modelo de report aceita `message` como tipo de alvo e conserva snapshot; a interface deve mostrar os campos existentes e indicar quando o alvo original não pode ser aberto. O desenvolvimento de mensageria fica fora desta mudança.

## Risks / Trade-offs

- **O papel `admin` pode ser confiável no cliente, mas não no endpoint →** cada endpoint de gerenciamento revalida o ator e seu papel no Xano.
- **Relatórios podem conter texto abusivo ou dados pessoais →** escapar texto na UI, limitar acesso a administradores e persistir somente o contexto necessário à análise.
- **Snapshots podem divergir do conteúdo atual →** mostrar data do report e estado do alvo quando disponível, distinguindo claramente snapshot de conteúdo ao vivo.
- **Agregações podem ficar lentas com o crescimento dos dados →** paginar listas, limitar consultas e usar contagens/agregações do lado do Xano.
- **Catálogo usa formatos de provedores diferentes →** mapear campos editáveis explicitamente por tipo e preservar campos externos que não forem editáveis.
- **Vínculo de reports de mensagem não pode ser validado sem mensageria →** manter `message` como tipo de alvo com snapshot e definir integração ao módulo de mensagens quando ele existir.

## Migration Plan

1. Confirmar no Xano o papel efetivo, campos e operações suportadas para usuários e catálogo; exportar a estrutura atual antes de alterá-la.
2. Adicionar estruturas de reports e auditoria sem remover nem reescrever dados existentes.
3. Criar endpoints administrativos com checagem de papel e paginação; revisar as operações em ambiente de desenvolvimento.
4. Construir as telas por domínio e conectar estados vazios, carregamento e falhas parciais.
5. Validar acesso com admin, membro e visitante, além de revisão de autorização diretamente nos endpoints.
6. Quando a publicação estiver autorizada e o delta revisado, publicar primeiro estruturas/endpoints compatíveis, depois a interface. Para rollback, desabilitar a rota administrativa e restaurar endpoints anteriores sem apagar reports ou auditoria. Esta revisão documental não publica alterações.

## Estado de implementação e validação

Publicação posterior em 13/10/2026 autorizada pelo usuário: tabela report e nove endpoints foram aplicados no Xano, com dry-run posterior sem delta. GETs administrativos rejeitaram visitante/membro. O dashboard passou a aceitar `page`/`per_page` para atividade recente. Admin/desativado, mutações e persistência ainda precisam de evidência; ver `validation/publicacao-admin-2026-10-13.md`. A contagem nessa rodada era 17/34; atual: 21/34.

Estado histórico de 13/10: 17/34 tarefas próprias concluídas. Grupos 2–5 têm contratos locais; integração real continua pendente. Grupos 6–8 têm UI/handlers e testes simulados, com revisão visual e estados ainda abertos. Grupo 9 distingue compilação/dry-run de teste remoto. A demonstração `/admin/demo` não acessa Xano nem substitui a validação integrada.

As referências de `docs/ADMIN_OPERATIONS.md` documentam matriz de operações, concessão manual de admin e rollback. A fonte de anime atual é Kitsu; registros Jikan são legados. A tabela `report` pertence a esta change e não deve ser atribuída à migração social arquivada.

O endpoint de decisão aceita os três estados de destino, mas o contrato local não impõe um grafo de transições terminais. Verificar política e comportamento em 5.3/9.1 antes de afirmar cobertura de transições inválidas. Revisar um report não executa exclusão do conteúdo alvo.

Recuperação de senha, seletor de mídia e upload do feed (H.1–H.7) são histórico anterior em `openspec/HISTORICO.md`. Entrega de e-mail segue pendente; upload real no browser foi validado em 14/10. São assuntos transversais, não tarefas administrativas concluídas.

## Plano de homologação integrada da 9.2 — preparado em 05/11/2026

**Estado: proposta documental, NÃO autorizada para execução.** Somente leituras
de arquivos e validação documental nesta rodada; nenhuma consulta de inventário,
autenticação, fixture, escrita ou teste remoto foi executado. A aprovação deste
plano será a autorização de uma rodada futura, com destino e permissões explícitos.
9.2 permanece aberta, 33/34. Não há autorização para publicar contratos, migrar
dados, conceder admin, fazer push/merge ou arquivar.

### 1. Fontes e lacunas exatas

Fontes: AGENTS.md, documentação central OpenSpec/AMBIENTE/PENDENCIAS,
docs/ADMIN_OPERATIONS.md, proposal/design/tasks e quatro delta specs desta change,
[matriz de 05/11](validation/matriz-9-2-2026-11-05.md),
[relatório complementar](validation/continuacao-9-2-2026-11-05.md), contratos
locais xano/api/codeboxd e xano/api/authentication, executores/testes administrativos.
Os contratos locais guiam o plano; serão comparados ao destino aprovado antes de
escrever, pois arquivo local não comprova publicação ou ausência de drift.

Já comprovados e a aproveitar: 68 cenários com APIs fictícias, 44 revalidados
após corrigir feedback dos modais, três regressões do sincronismo, Reports real
renderizado em 1440/390 e 119 checks de API reais históricos em 04/11. Não repetir
essas baterias inteiras. A repetição abaixo se justifica pelo novo acoplamento
UI → Xano → leitura independente → UI após recarga, não por aumentar contagens.

Pendências integradas:

- Formulário real /admin/login com admin, membro, inválidas e sessão existente;
  acesso direto como visitante/membro/conta suspensa, redirecionamentos e ausência
  de dados restritos. O login seguro do executor não substitui esse formulário.
- Busca/detalhes de conta; cancelar sem PUT; suspender e reativar uma conta de
  teste, com UI, persistência, bloqueio de capacidades e auditoria reais.
- Edição dos quatro tipos, campos inválidos, rascunho após falha, feedback nos
  diálogos e preservação de identidade; criação/deduplicação pelo formulário
  Adicionar obra ainda não homologada de ponta a ponta.
- Reports: contexto/snapshot, cancelamento, decisão obrigatória, pendente → em
  análise → resolvido e pendente → rejeitado, persistência/auditoria e integridade
  do alvo. Não assumir que é permitido voltar a pending para restaurar fixtures.
- Filtros, vazio e segunda página reais pela UI, mantendo per_page=25; a API
  histórica com per_page=1 e a renderização de Reports atual não cobrem isso.
- Erro/retry por seção com dados reais: falha injetada somente no proxy local,
  seguida de nova leitura real. Não derrubar fonte real nem provocar 429.
- Verificações visuais após cada ação em 1440x900 e 390x900: loading encerrado,
  conteúdo da operação atual, controles acessíveis e mensagens dentro do modal.

### 2. Recursos existentes e grau de certeza

| Recurso | Evidência disponível | Pode ser reutilizado? |
| --- | --- | --- |
| Admin aprovado | Login/role ativo confirmados em 05/11; ferramentas históricas fixam ID 14 | Candidato apenas a ator, após novo login seguro e confirmação de identidade; nunca alvo nem promoção automática |
| Workspace | Histórico aponta perfil default, workspace 147717 | Destino candidato, não autorização; URL/grupo/branch/data source devem ser confirmados |
| Isolamento Xano | Em 03/11, branch e fonte isolada foram recusadas pelo plano gratuito | Disponibilidade atual NÃO verificada; priorizar ambiente separado, não presumir que o plano mudou |
| Fixtures remotas de 04/11 | Evidência registra remoção e integridade de 11 tabelas; diretório privado .local/admin-acceptance-20261104 ausente nesta máquina | Nenhuma fixture remota conhecida e autorizada para reuso; não confundir ausência do journal com inventário remoto vazio |
| Quatro reports vistos em 05/11 | Leitura/renderização real aprovada | Dados existentes apenas para leitura; NÃO autorizar decisões sobre eles |
| IDs 101/201/301 das APIs fictícias | Testes locais, em memória | Nunca usar como IDs remotos: podem coincidir com registros reais |
| Estado local | Branch task/admin-acceptance-9-2-20261105; alterações preexistentes preservadas | .venv, sem Docker; frontend/porta/log próprios, sem reiniciar instância habitual |

Não houve inventário remoto nesta preparação. A disponibilidade efetiva de contas,
quota, políticas de referência/exclusão e ambiente isolado é uma dependência do
pré-voo futuro; não uma afirmação de existência atual.

### 3. Isolamento e conjunto de dados proposto

Preferência: workspace/ambiente de homologação separado com contratos compatíveis,
sem copiar dados pessoais de produção. Criar/ativar esse ambiente ou publicar nele
é escopo separado, não efeito implícito da aprovação de testes.

Alternativa: namespace lógico novo no workspace compartilhado, somente se o
usuário aprovar nominalmente esse destino e os efeitos temporários em contagens,
fila e catálogo. Esse namespace NÃO é isolamento de banco, quota ou visibilidade;
obras/posts podem aparecer a outras pessoas. Se isso for inaceitável, não usar o
workspace compartilhado. Não introduzir flags de produto para ocultar dados.

Cada execução recebe run_id aleatório e exclusivo, por exemplo cbh9_<12hex>.
usernames respeitam limite de 30 e regex existentes; nomes/títulos/descrições
contêm o marcador. Domínio de e-mail example.invalid e senhas aleatórias privadas;
sem recuperação/e-mail/Resend nesta homologação. Uma execução interrompida não
gera novo lote silenciosamente: primeiro reconciliar os IDs já criados.

**Pacote completo proposto (teto de efeitos, não criação nesta rodada):**

| Símbolo | Quantidade | Papel/finalidade |
| --- | ---: | --- |
| A | 1 existente | admin ativo fornecido pelo usuário; somente ator, não alterado |
| R, B e U01–U24 | 26 novas contas no total | Todos member; R denuncia/cria post e testa negação; B alterna active/disabled e retorna a active em cada largura; 24 contas completam paginação de usuários |
| Perfis/listas iniciais | 26 perfis e 52 listas esperadas | Efeitos do signup atual, duas listas padrão por conta; conferir IDs retornados/relações, não alterar originais |
| M[tipo,01–26] | 104 obras no total | 26 por movie/series/book/anime; duas por tipo para editar em larguras distintas e lote para segunda página |
| P | 1 publicação nova | Criada por R, texto fictício, sem imagem/upload; alvo de reports com integridade verificável |
| Qm01–Qm26 | 26 reports de mensagem | Snapshot sintético, sem mensageria; mesmo tipo/motivo dá mais de 25 resultados mesmo no filtro |
| Qp1/Qp2 e Qt1/Qt2 | 4 reports adicionais | Dois sobre P e dois sobre obras do lote; um conjunto por largura |
| event_log | Crescimento esperado, contado ao executar | Auditoria append-only das ações; todos os eventos da rodada serão preservados |

São até **239 registros de domínio** (26 user + 26 profile + 52 listas + 104 media
+ 30 reports + 1 post), além da auditoria. O número é estimativa do contrato atual,
não prova dos efeitos do destino. Relações inesperadas interrompem o setup.

Para manter esse teto: seed de **96 obras** (24 por tipo) via Metadata API
autorizada; criar **8 pela UI** (uma por tipo/largura) e repetir a mesma identidade
para comprovar deduplicação sem criar outras oito. Só paginar após atingir 26
por tipo. Não reduzir per_page, reescrever consultas no proxy ou contar registros
reais como parte do lote necessário.

Seed de edição pode usar external_source=test, identity_key exclusivo do run_id,
como no ensaio histórico. Isso NÃO passa no formulário de criação: POST
admin/catalog exige tmdb numérico, kitsu/jikan numérico ou openlibrary OL<dígitos>W.
As oito criações usarão identidades sintéticas de formato válido, enumeradas no
manifesto, sem consultar provedores. Não existe garantia de namespace reservado
nesses provedores. Confirmar ausência da identity_key no workspace imediatamente
antes do POST e impedir reuso/edição de um registro retornado fora do manifesto.
Em ambiente compartilhado, esse risco precisa de aprovação expressa; o destino
isolado é preferível. Cancelar o editor aberto na deduplicação; não salvar outro
título sobre o registro existente.

Cada largura usa dois Qm diferentes e seus Qp/Qt. Assim não se precisa reverter
um report terminal para pending, operação que o endpoint de decisão não oferece.
Outros 22 Qm permanecem pendentes para paginação até a limpeza. Não criar moderator
nem outro admin; papel moderator não é necessário ao requisito administrativo.

### 4. Matriz de operações permitidas APÓS aprovação

Bases auth/social e Metadata são as do destino confirmado, nunca inferidas do
perfil global. Todos os IDs abaixo são símbolos resolvidos pelo manifesto da
rodada, jamais números literais do histórico. Verificar UI e persistência é
obrigatório; HTTP 200 isolado não satisfaz nenhum cenário.

#### Autenticação e leituras

| ID/funcionalidade | Endpoint e método | Conta/permissão | Alvo descartável | Alteração Xano | Resultado UI | Verificação persistência | Restauração/limpeza | Riscos/dependências |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 Login/negação/redireção | POST auth /auth/login; GET auth /auth/me; rotas locais /admin/login e /admin | A admin; R member; visitante; B disabled no momento próprio | Credenciais de R/B; uma tentativa inválida só em B | Emissão de sessão é efeito de autenticação; não alterar papel/senha | Admin entra; sessão existente retorna; membro/visitante/disabled sem dados restritos; erro genérico | Papel/status confirmado pelo servidor, cookie/session storage e log de chamadas restritas | Encerrar apenas contextos de teste; tokens em memória descartados | Login POST não é leitura pura; limite de tentativas/lockout do destino deve ser confirmado; nunca testar senha inválida de A |
| L2 Usuários/filtros/página 2/vazio | GET social /admin/users: search, user_id, role, account_status, page, per_page=25 | A | R/B/U, busca pelo marcador ou ID de B; vazio por termo único | Nenhuma | Totais/páginas coerentes, detalhes sem segredos | GET independente e IDs do manifesto; segunda página sem repetição/omissão | Nenhuma mudança a reverter | Formulário exige termo; não presumir que só abrir Usuários faz consulta |
| L3 Catálogo por tipo | GET social /admin/catalog: media_type, search, page, per_page=25 | A | 26 obras por tipo, busca pelo marcador | Nenhuma | Quatro seções, título/tipo correto, vazio e página 2 | Comparar IDs/identidades em duas páginas e consulta independente | Nenhuma | Criar os oito itens UI antes de exigir 26 por tipo; Ver todas reinicia critérios |
| L4 Fila/snapshot/filtros | GET social /admin/reports: status, target_type, reason, page, per_page=25 | A | Qm/Qp/Qt; marker nos dados mas não há filtro textual de reports | Nenhuma | Snapshot de mensagem sem alvo ao vivo, decisões/status, vazio por combinação conhecida, página 2 | IDs esperados, total, status/tipo/motivo; comparar snapshot salvo | Abrir snapshot/cancelar não modifica report | 26 Qm garantem segunda página; dados alheios podem aparecer em workspace compartilhado, jamais se tornam alvos |
| L5 Auditoria/integridade | GET Metadata /table/{table_id}/content e /content/{id} | Credencial Metadata de leitura autorizada | Eventos relacionados aos IDs do manifesto; antes/depois dos alvos | Nenhuma | Feedback/status/decisão da UI correspondem ao backend; sem inventar tela de auditoria | Ator $auth.id, horário, previous/new status, decisão/motivo; hash do alvo | Preservar os eventos | Não há endpoint UI de histórico integral; comparar na Metadata API, sem exportar segredos |

#### Escritas de provisionamento e aceitação

| ID/funcionalidade | Endpoint e método | Conta/permissão | Alvo descartável | Alteração Xano | Resultado UI | Verificação persistência | Restauração/limpeza | Riscos/dependências |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 Contas | POST auth /auth/signup | Cadastro normal, sem promoção | 26 identidades novas do run_id | user/member + profile + duas listas padrão por conta | Contas permitem login normal; membro não vira admin | Registrar IDs e relações em journal; confirmar role/status | C1/C2 abaixo; nunca tocar A | Tentativa pode persistir apesar de timeout; reconciliar identidade exata antes de qualquer repetição |
| P2 Obras para edição/paginação | POST Metadata /table/{media_table_id}/content/bulk | Metadata de escrita limitada ao lote | 96 entradas enumeradas, sem IDs forçados | Cria apenas media sintética | L3 encontra registros pelo marcador | IDs retornados, identity_key/run_id e contagem por tipo | C1, IDs criados e verificados | Nunca importar schema, sobrescrever IDs, usar allow_id_field=true ou executar staging/deploy de scripts antigos |
| P3 Publicação e reports | POST social /posts; POST social /reports | R member ativo | P e 30 Q próprios; message aceita target_id textual e snapshot.body obrigatório | Publicação nova; reports pending/snapshots | Fila/snapshot/relacionamento visíveis | Releitura de P/media/report; para post/media snapshot vem do servidor, não do payload do cliente | C1/C2; conservar reports revisados | Descrição escrita obrigatória; tipos message/post/media; não criar mensagens reais; sem upload |
| E1 Cancelar conta | Nenhum PUT esperado; somente validações/GET já permitidos | A | B | Nenhuma | Diálogo fecha e status fica intacto | Zero PUT no transporte + status/auditoria sem alteração | Nada | Capturar antes/depois; abrir diálogo não é autorização para enviar |
| E2 Suspender/reativar | PUT social /admin/users/{B}/status, account_status e reason com run_id | A ativo | Somente B | active→disabled→active e dois event_log por largura | Erro/sucesso inline, status atualizado; B perde acesso protegido ao suspender | GET conta + GET de capacidade protegida de B (ex.: /interactions), relogin apropriado e auditoria | Deixar B active ao fim do cenário; C1/C2 depois; manter todos os eventos | Não suspender A/R; 401/403 no membro pode limpar sessão e exigir novo login após reativação |
| E3 Editar/validar/cancelar obra | PUT social /admin/catalog/{M}; cancelar/erro de validação local sem PUT | A ativo | Duas obras enumeradas por tipo, uma por largura | Só title/description/year/cover_url suportados | Rascunho preservado no inválido/503, erro dentro do modal, sucesso após salvar | Recarregar UI e reler registro completo; id/identity_key/fonte/external_id/media_type intactos | Restauração apenas da própria fixture ou C1; não restaurar banco inteiro | PUT catálogo não promete evento de auditoria no contrato; não inventar essa evidência |
| E4 Criar/deduplicar | POST social /admin/catalog, duas chamadas com a mesma identidade por tipo/largura | A ativo | Oito identidades sintéticas permitidas, inicialmente ausentes | Primeiro POST cria; segundo created=false e mesma obra sem alterar campos | Registro aparece; repetição abre o existente, sem duplicata; cancelar editor | Metadata por identity_key + retorno created/item.id + UI; nenhum PUT no cancelamento | C1 por IDs, salvo referências retidas | Se retornar registro fora do manifesto, PARAR sem editar/remover; source=test é inválido nesse endpoint |
| E5 Cancelar/decidir reports | PUT social /admin/reports/{Q}, status e decision; cancelar/nota vazia sem PUT | A ativo | Por largura: Qm1 reviewing→resolved; Qm2 rejected; Qp resolved; Qt rejected | Atualiza revisor/decisão/horário e acrescenta eventos | Nota obrigatória, diálogo legível, status/decisão persistem após recarga e filtro | Releitura do report e event_log, snapshot e alvo comparados antes/depois | Reter oito Q revisados e seus eventos em C2; sem rollback terminal artificial | Alvo não pode ser apagado/editado por revisar; ator vem da sessão, não do payload |
| E6 Negação de escritas | PUTs E2/E3/E5 e POST E4 contra fixtures declaradas | Visitante/R member; B suspenso conforme contrato | Somente os mesmos alvos descartáveis | Esperado: nenhuma | Nenhum acesso/ação indevida | 401/403 esperados + releitura independente + zero evento de sucesso; correlação do tráfego | Se bug produzir efeito, conter apenas a fixture e parar; preservar logs | São tentativas de escrita e EXIGEM aprovação, mesmo esperando rejeição; não testar sobre ID real |
| E7 Erro e retry acoplados | Proxy retorna 503 antes de encaminhar um GET de L2/L3/L4 ou PUT E2/E3/E5; próxima ação manual segue ao endpoint real | A, identidade preservada | Somente requests da execução/fixtures | Requisição bloqueada: zero escrita remota; retry confirmado: efeito declarado | Erro inline, dados/rascunho preservados; recuperação após nova tentativa | Provar blocked_before_upstream=true; depois ler Xano e UI | Nenhuma reversão pelo erro injetado; efeitos do retry seguem C1/C2 | Não repetir mutação automaticamente; timeout após encaminhar exige reconciliação, não retry cego; não simular 429 derrubando serviço |

As recusas E6 não repetem a bateria API histórica como entrega nova: a evidência
nova é o fluxo integrado e sua ausência de efeito. Não enviar actor_user_id nem
reviewer_user_id como identidade real. Nenhuma operação de publicação/migração,
rotação de senha ou DELETE sobre conteúdo original integra esta matriz.

### 5. Manifesto, auditoria e limpeza

Antes de criar: registrar intent com run_id, destino completo (workspace, branch,
data source, grupos), contas/identidades previstas e limites. Guardar em
.local/admin-homologacao/<run_id>/, novo diretório, com baseline e hashes; nunca
usar diretórios históricos ou artefatos arquivados como destino de escrita.
Após cada resposta: acrescentar tabela, ID retornado, vínculo de dono, identidade,
hash dos campos e fase. Nunca autorizar exclusão por prefixo/LIKE isoladamente.

Antes de cada mutação: interseção entre IDs/identidades aprovados e o manifesto;
comparar conteúdo atual/dono/run_id, não confiar só no nome da tela. Bloquear
qualquer alvo original e A. POST novo só passa para identidade prevista e após
teste de ausência; após timeout, reconciliar pela identidade antes de continuar.
O manifesto de recursos não contém senha/token. Credenciais descartáveis, se
precisarem sobreviver a interrupção, em armazenamento privado restrito separado;
tokens só em memória, login A pelo formulário local seguro.

Usar o menor privilégio Metadata disponível. Não presumir que o provedor suporta
ACL por tabela/linha: limites por lote/ID também precisam ser impostos pelas
guardas do executor e revisados pelo operador. Um token administrativo amplo
não constitui, por si só, autorização para atuar fora do manifesto.

Snapshot de preservação: hashes por ID de registros originais e contagens,
comparados depois excluindo apenas os efeitos próprios declarados. Não salvar
senhas/hashes de senha ou respostas integrais de user no relatório. Hash completo
em memória pode provar identidade do registro sem exportar seu conteúdo. Em
workspace compartilhado, atividade externa pode produzir drift: investigar,
nunca restaurar/deletar alterações de terceiros para forçar igualdade.

**C1 — remoção limitada (somente com aprovação específica):** Metadata API
POST /table/{table_id}/content/bulk/delete com row_ids explícitos. É destrutiva,
apesar de usar POST; não está autorizada nesta preparação. Rever referências e
políticas de cascata antes de cada lote. Excluir somente Q não revisados sem
eventos associados, P/obras próprias sem referências externas, relações/listas,
perfis e contas que não sejam necessários para preservar auditoria. Exigir
success_total e releitura; exclusão parcial interrompe a limpeza. Nunca apagar
event_log. Não chamar a limpeza antiga como atalho.

**C2 — retenção auditável proposta:** manter todos os eventos da rodada, os oito
Q revisados, o denunciante R e o alvo B (mais seus dois profiles e quatro listas
iniciais), para conservar referências e contexto da auditoria de conta. Ao
finalizar, desativar somente R/B com A e motivo run_id, acrescentando auditoria;
remover credenciais descartáveis do armazenamento de trabalho conforme política
aprovada. São até 16 registros de domínio retidos (duas contas + dois profiles +
quatro listas + oito Q), além dos logs. As contagens/fila finais
mudam por essa retenção: não prometer retorno global exato ao baseline. Reports
retidos estão resolved/rejected e conservam snapshot mesmo se P/media próprios
forem removidos. A permanece intocado.

Se houver outros event_log com ator fixture, cascata desconhecida ou referências
de terceiros: NÃO excluir os usuários/alvos envolvidos. Emitir lista de resíduos,
conter somente contas de teste se autorizado e pedir decisão; a retenção extra
não deve ser absorvida silenciosamente no teto. Sem aprovação de C1/C2, não iniciar
seed que depois exija uma limpeza não autorizada. No destino isolado, retenção
integral também é uma opção explícita do proprietário; não destruir o ambiente
para apagar auditoria. Exportar logs não autoriza removê-los da origem.

### 6. Adequação dos executores antes de executar

| Ferramenta atual | Reaproveitamento | Bloqueio/adequação necessária |
| --- | --- | --- |
| admin_browser_sync.py | Resposta da operação, conteúdo esperado, loading encerrado e captura estável | Reusar sem refazer seus três testes salvo mudança real; sem esperas fixas como prova |
| admin_browser_real.py | Caminhos novos e validação de renderização | Proxy atual só GET; --reports-only já comprovado. Não habilitar PUT/POST genéricos: implementar allowlist por método/rota/ator/ID/identidade antes dos fluxos de escrita |
| admin_acceptance_browser.py | Passos/asserts dos 68 cenários locais | Fixture e IDs locais não podem ser convertidos em alvos remotos; substituir por manifesto/dados lidos do destino |
| admin_acceptance_remote.py | Ideias de checks de persistência/identidade/auditoria | NÃO executar como está: cria dados, apaga event_log no finally, usa diretório histórico e ID 14; --browser-output também não fornece a configuração atual necessária ao BrowserProbe |
| list_status_live.Run | Referência de journal e respostas bulk/delete | NÃO executar como plano admin: hardcode x-data-source=live, caminhos antigos, staging/deploy e limpeza não adequada à retenção atual |
| admin_reads_remote.py / admin_dashboard_remote.py | Login seguro, consultas/contratos históricos | Autorização hardcoded no ID 14 precisa corresponder ao ator nominal aprovado; não presumir validade para outro destino ou conceder privilégios |

Essas adequações são trabalho futuro de executor, com testes locais de guardas e
cancelamento antes de pedir qualquer escrita no destino. Nenhuma implementação
de executor foi feita nesta rodada. Não há comando único existente seguro para
todos esses fluxos; o runbook abaixo é executável por UI + verificador de leitura
após cumprir os pré-requisitos, e pode orientar a futura automação. Não apresentar
comando de ferramenta ainda inexistente como pronto para uso.

### 7. Sequência executável após aprovação

1. **Pré-voo só leitura:** confirmar destino/isolamento, ator A, contratos e
   permissões Metadata, políticas de cascata, quota, per_page=25 e espaço para
   lote/retidos. Inventariar recursos disponíveis sem PII; conferir journals
   antigos e ausência das identidades novas. Registrar decisão de reutilização:
   somente fixture comprovadamente própria e explicitamente adicionada ao novo
   manifesto; caso contrário criar novo lote. Nova aprovação se destino/custos
   diferirem do aceito. Nenhum seed durante esse pré-voo sem liberação.
2. **Ensaio local das guardas:** sem Xano, comprovar que ID estrangeiro, identidade
   existente, destino live não aprovado, ausência de manifesto e exclusão de
   auditoria são bloqueados; cancelamento gera zero PUT/POST. Não reexecutar a
   bateria local de 68 inteira se apenas o adaptador/guardas mudarem.
3. **Baseline e provisionamento:** A autentica; provisionar P1/P2/P3 com R/B
   conhecidos; registrar todos os efeitos. Concluir os oito cadastros E4 na UI
   em 1440/390 e seus oito testes de reutilização. Verificar 26 contas, 26 obras
   por tipo e 26 mensagens no filtro. Seed parcial: parar/reconciliar, sem criar
   lote adicional e sem iniciar testes que dependem de contagem incompleta.
4. **Autorização:** L1 e E6 no lote; uma credencial inválida só de B, contextos
   separados, nenhuma senha no chat. Recusa inesperada ou escrita indevida:
   interromper antes de seguir aos cenários positivos.
5. **Leituras/filtros:** L2–L4, página 1/2 e retorno em cada largura. Não clicar
   ações em linhas fora da allowlist. Reports existentes e métricas de outras
   pessoas são leitura privada; não usar como alvos nem publicar capturas deles.
6. **Conta:** em cada largura, cancelar E1 e provar ausência de efeitos; E2
   suspende B, verifica recusa real de capacidade protegida e reativa B; reler e
   recarregar UI, conferir evento e estado anterior/novo. B ativo antes da próxima
   largura; R permanece ativo para os reports até a limpeza.
7. **Catálogo:** E3 em quatro tipos/duas larguras: cancelar, inválido, 503 antes
   do envio, nova confirmação, GET independente, recarga e identidade preservada.
   Campos complementares de provedores não editáveis permanecem intactos.
8. **Moderação:** para cada largura, usar os Q designados em E5, abrir snapshot,
   cancelar, testar nota vazia, confirmar estados, filtrar destino e recarregar.
   Comparar P/media antes/depois de revisar, não com o estado anterior a uma
   edição legítima de catálogo. Auditoria L5 é append-only.
9. **Erros e recuperação:** E7, uma seção por vez; requests bloqueados só no
   proxy local, sem mexer no servidor real. Ler depois do retry. Uma resposta
   503 injetada não prova falha real de fornecedor; manter essa distinção.
10. **Conferência e limpeza:** coletar evidências, C1/C2 com preview de IDs/tabelas
    e dependências do manifesto, preservar auditoria, conferir resíduos previstos,
    original hashes e sessões/contextos encerrados. Não rollback global, não
    apagar linhas de auditoria para obter digest idêntico.
11. **Aceite:** consolidar aprovado/reprovado/bloqueado/não executado, indicando
    API real, UI real e erro local. Só recomendar fechar 9.2 após todos os
    obrigatórios acima comprovados e resíduos reconciliados. Sem autoarquivo.

Ritmo inicial proposto: chamadas remotas seriais, intervalo mínimo de 3,1 s,
sem testes de carga; teto de 500 requests remotos na rodada, com pré-estimativa no
manifesto (inclui setup/verificação/limpeza). Se insuficiente, parar e renegociar.
Esse intervalo vem do ensaio anterior, não de garantia de quota. Respeitar
Retry-After integral, inclusive data HTTP, e políticas efetivas. 429 persistente,
timeout ambíguo em escrita, contrato divergente, vazamento ou ID fora do manifesto
interrompem a fase; nunca replay automático de mutação. Reservar janela com baixa
concorrência; tempo não medido, piso só de espera pode chegar a ~26 min no teto.

### 8. Evidências e critério de encerramento

Por cenário e largura: identificador/esperado/observado/status, destino/run_id,
IDs privados, marcador de correlação, registro sanitizado de método/rota/status,
releitura independente e resultado da recarga. Para cancelar: zero chamadas de
escrita e hash/eventos inalterados. Para salvar: um efeito confirmado, estado
persistido e feedback dentro do modal; para suspensão/decisão, evento com ator,
horário, anterior/novo e motivo/decisão. Para report: alvo e snapshot preservados.
Para deduplicação: mesmo ID e nenhum item adicional. Para paginação: 25+1 ou
outra distribuição coerente com o lote, sem reduzir o page size nem duplicar IDs.

Capturas reais e diagnósticos integrais ficam privados em .local, sem tokens,
senhas ou headers Authorization. Publicar em validation só matriz sanitizada,
contagens/hashes apropriados e referências; não copiar dados pessoais de filas
compartilhadas. Registrar também os erros e tentativas incompletas, sem sobrescrever.
Guardar diff de preservação de originais e inventário final de retenção/limpeza.
No final, validar OpenSpec e conferir Git/lockfiles; não confundir validação de
documentos, API histórica ou pass automático com aceite visual integrado.

### 9. Autorizações a obter antes da execução

- **A0 Destino:** ambiente/workspace/branch/data source nominados e acesso
  de leitura. Preferência por homologação isolada; se indisponível, decidir
  explicitamente se admite os efeitos visíveis/contagens no compartilhado.
- **A1 Ator e janela:** conta admin existente para login seguro, janela de baixa
  concorrência e aprovação das tentativas inválidas somente em B; sem promoção,
  troca de senha, alteração do perfil de A ou acesso a credenciais pelo chat.
- **A2 Setup:** até 26 contas member e efeitos de signup, 96 obras seed + oito
  criadas pela UI (104 no total), 30 reports, um post e auditoria. Credencial
  Metadata limitada ao destino/tabelas/lote para seed e verificação. Aprovar o
  uso de identidades sintéticas de formato de provedor, sem tocar originais.
- **A3 Operações:** E1–E7 apenas sobre o manifesto, incluindo tentativas negativas
  de escrita, duas larguras, erros locais antes do upstream, releituras e teto
  de requests. Rejeitar qualquer permissão genérica de editar contas/obras reais.
- **A4 Limpeza e retenção:** C1 com row_ids próprios e C2 preservando eventos,
  oito reports revisados, R/B desativados, dois profiles e quatro listas; aprovar
  esses 16 registros de domínio retidos, além da auditoria.
  Se não aceitar retenção, reformular o isolamento antes do seed; não apagar
  história para satisfazer limpeza total. Cascatas/referências desconhecidas
  exigem decisão adicional, não exclusão automática.

Uma aprovação parcial autoriza só as fases explicitamente selecionadas. O pedido
atual autoriza somente preparar/documentar; A0–A4 continuam pendentes. Não abrir
janela de login, consultar dados do Xano nem executar os testes deste plano até
o usuário aprovar o escopo de homologação.
