# Backlog rastreável — Codeboxd

Atualizado em 28/10/2026. Fonte: [auditoria](codeboxd-auditoria.md).
Change documental: [consolidar-auditoria-backlog](../changes/consolidar-auditoria-backlog/proposal.md).
Não foram encontrados IDs CBX anteriores nos Markdown de docs/OpenSpec; os IDs
existentes P.* e IDs internos das changes continuam preservados.

## Resumo executivo

O produto tem os principais módulos implementados. A conclusão depende de
validar integrações e jornadas já aprovadas, especialmente recuperação por
e-mail e administração, além de medir performance contra metas aprovadas.
Ferramentas sintéticas preparadas não encerram critérios remotos.
Nenhum defeito P0 atual foi comprovado. Não somar os itens desta tabela aos
checklists: CBX agrupa e referencia o trabalho existente.

P1: jornada essencial ou controle de acesso; P2: requisito aprovado sem bloqueio
do primeiro uso; P3: fechamento documental. P/M/G são tamanhos relativos, não prazos.
"Bloqueada" indica dependência externa concreta; não significa ausência do código.

## Backlog priorizado

| ID | Área | Tarefa | Prioridade | Tamanho | Estado | Dependências | Evidência |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CBX-001 | Recuperação | Comprovar envio aceito e ciclo de senha | P1 | M | Bloqueada | Caixa elegível/domínio Resend e participação do titular | recuperação 3.2/3.4; P.6 |
| CBX-002 | Segurança admin | Validar autorização, suspensão e auditoria | P1 | M | Bloqueada | Ambiente/contas controladas autorizados | gerenciamento 2.1/3.2/3.3/9.1 |
| CBX-003 | Dashboard | Corrigir e verificar falhas parciais independentes | P2 | P | Concluída | Merge ainda não autorizado | PR #24, 479 testes e navegador 8/8 na integração temporária |
| CBX-004 | Dashboard | Comprovar totais e paginação no ambiente de desenvolvimento | P2 | M | Bloqueada | Publicação revisada do candidato e login admin autorizado | gerenciamento 2.2/2.3 |
| CBX-005 | Catálogo admin | Validar filtros, busca, páginas e edição íntegra | P2 | M | Pendente | Interpretador e ambiente controlado autorizados | gerenciamento 4.1/4.2/9.1 |
| CBX-006 | Moderação | Validar fila, decisão, auditoria e alvo intacto | P2 | M | Pendente | Interpretador e ambiente controlado autorizados | gerenciamento 5.2/5.3/5.4/9.1 |
| CBX-007 | Interface admin | Completar navegador com dados reais de desenvolvimento | P2 | M | Pendente | CBX-002/004/005/006 | gerenciamento 9.2 |
| CBX-008 | Medição | Completar baseline, diagnóstico de 429 e metas por jornada | P2 | M | Pendente | Aprovação das metas e contas dos cenários | performance 1.3/1.4/1.5 |
| CBX-009 | Performance | Comparar login/catálogo/avaliação/listas | P2 | G | Pendente | CBX-001/008; incrementos abaixo | performance grupos 2–6 |
| CBX-010 | Performance social | Comparar leituras e mutações sociais | P2 | M | Pendente | CBX-008; duas contas controladas | performance 7.1–7.4 |
| CBX-011 | Performance admin | Comparar administração e jornada integrada | P2 | M | Pendente | CBX-007/008/009/010 | performance 8.1–8.4/9.1–9.3 |
| CBX-012 | OpenSpec | Sincronizar e arquivar entrega pronta do feed | P3 | P | Pendente | Revisão da sincronização e limites da entrega | feed 6/6 e delta social-feed |

## Detalhamento dos itens confirmados

### CBX-001 — Entrega de recuperação

- Problema/objetivo: código e integração existem; envio aceito, recebimento e
  ciclo completo ainda não foram comprovados. Fonte: [tasks](../changes/recuperar-senha-codigo-6-digitos/tasks.md)
  e [Resend](../changes/recuperar-senha-codigo-6-digitos/validation/resend-integracao-2026-10-22.md).
- Aceite mínimo: envio aceito; seis dígitos recebidos em caixa controlada;
  alteração/login novo; código reutilizado rejeitado; restauração segura da conta
  e evidências sem código, senha ou token. Não recriar integração já publicada.
- Estimativa de componentes: `tools/password_recovery_remote.py`, endpoints reset
  e formulário de recuperação. Risco: destinatário não elegível e entrega externa.
- Testes: contratos/falhas simuladas e ciclo real opt-in; mocks não fecham o item.

### CBX-002 — Controle administrativo

- Objetivo: comprovar as regras existentes de admin ativo e sessão suspensa,
  com ator derivado de `$auth.id` e auditoria persistida. Fonte:
  [tasks](../changes/gerenciamento-website/tasks.md), IDs 2.1/3.2/3.3.
- Aceite: visitante/membro/admin desativado rejeitados por chamada direta;
  suspensão impede operação protegida; reativação funciona; evento identifica
  ator/alvo/estado anterior/novo/horário/motivo. Sem inventar proibição de autossuspensão.
- Estimativa: status PUT, guard de sessão, `admin_account_fixture.py` e executor
  controlado existente. Risco: cenário real altera conta; exigir descartável e restauração.
- Testes: fixture extraída, API direta e inspeção de evento; o PR #21 prepara
  12 cenários, mas não executou Xano. Não há prova atual de corrupção concorrente.

### CBX-003 — Falha parcial do dashboard

- Defeito comprovado: validação global interrompia métricas e listas válidas;
  booleanos/frações eram aceitos como totais. Fonte: `state/admin.py` e
  [spec](../changes/gerenciamento-website/specs/admin-dashboard/spec.md).
- Aceite: inválidos mostram indisponibilidade, zero válido continua zero,
  fontes restantes permanecem legíveis; erro não vira vazio; nova resposta
  remove erros anteriores e não apresenta dados antigos como atualizados.
- Estimativa: estado/página admin, testes parciais e harness de navegador.
  Testes: métricas ausentes/bool/negativas/NaN, lista inválida independente,
  HTTP 503, recuperação, desktop/celular e detalhes das métricas sem erro.
- Risco: acessar chave ausente no mapa reativo; revisão exige chaves ou fallback.
- Entrega: commits do PR #24, incluindo correção das chaves e harness. Seis
  testes novos e oito cenários de navegador integrados passaram. Concluída no
  escopo local verificado; não integrada à main nem publicada na instância normal.

### CBX-004 — Indicadores e filas do dashboard

- Requisito: gerenciamento 2.2/2.3. [Candidato e limites](../changes/gerenciamento-website/validation/dashboard-2026-10-27.md).
  Endpoint candidato e ferramentas já existem; não contabilizar como implementação ausente.
- Aceite: totais conferidos contra inventário independente; apenas pendentes;
  páginas sem repetição/omissão, desempate por ID e vazio correto, sem segredos.
- Estimativa: `admin_dashboard_GET.xs`, fixture e probe existentes.
  Testes: interpretador sintético, dry-run/publicação restrita autorizada e leituras
  autenticadas; cenário realmente vazio não comprova continuação preenchida.
- Dependência externa: remoto mais recente documentado ainda não tem os dois
  metadados de paginação candidatos. Conferir novamente antes de publicar.

### CBX-005 — Catálogo administrativo

- Requisito: gerenciamento 4.1/4.2 e spec de catálogo admin; endpoints já existem.
- Aceite: quatro tipos isolados, busca/vazio/páginas; edição altera apenas campos
  permitidos, preserva identidade externa/local e não muda dados em falha.
- Estimativa: GET/PUT catálogo e `admin_catalog_fixture.py`; PR #23 prepara
  21 cenários. Testes: executar contratos extraídos, edição válida/inválida,
  consultas com símbolos/caixa e títulos iguais, depois API real autorizada.
- Risco: `~` e agrupamento são candidatos a reprodução, não defeito confirmado.
  Não alterar busca nem criar nova regra de identidade sem evidência.

### CBX-006 — Moderação

- Requisito: gerenciamento 5.2/5.3/5.4; implementação presente.
- Aceite: filtros status/tipo/motivo combináveis e paginados; decisão explícita
  grava ator/estado anterior/novo/horário; criação/revisão não altera o alvo.
- Estimativa: reports GET/PUT/POST e `admin_moderation_fixture.py` (PR #20).
  Testes: 22 cenários preparados, auditoria adulterada/tempo inválido, conteúdo
  intacto e API controlada. O gerador não cobre autenticação HTTP nem criação.
- Riscos: concorrência/auditoria anterior e desempate ainda precisam de prova;
  não inventar grafo terminal ou funcionalidade de mensagens.

### CBX-007 — Interface administrativa real

- Fonte: gerenciamento 9.2. Aceite: dashboard, usuários, quatro tipos e reports
  em desktop/celular com dados de desenvolvimento autorizados, vazio, carregamento,
  erro parcial e confirmações; sem exposição de campos secretos ou overflow.
- Estimativa: páginas/estado admin e harness `admin_layout_browser.py`.
  Testes fictícios 1440/390px são preparação; não substituir a camada real.
- Dependências: CBX-002/004/005/006. Risco: mutações exigem fixtures/limpeza exatas.

### CBX-008 — Baseline e metas

- Fonte: performance 1.3/1.4/1.5. Aceite: pelo menos cinco amostras por cenário
  frio/aquecido e viewport, mediana/pior amostra/chamadas por serviço; origem,
  sequência e Retry-After do 429; orçamentos aprovados antes da comparação.
- Estimativa: `performance_probe.py` e executores existentes. PR #22 captura
  Retry-After sanitizado; seu MockTransport não comprova quota/reprodução real.
- Testes: rede simulada adversária para instrumentação; medições reais separadas.
  Risco: medições podem gerar 429; respeitar espera, orçamento e interrupção.

### CBX-009 — Jornadas de login, catálogo, avaliações e listas

- Fonte: performance 2.3/2.4/3.5/4.4/5.3/5.4/6.2–6.4.
- Incrementos independentes após CBX-008: (a) login/cadastro/recuperação e navegação,
  (b) catálogo/fichas nos quatro tipos, (c) avaliação/edição/envio único,
  (d) biblioteca/listas pequenas e grandes, incluindo privadas e duas contas.
- Aceite de cada incremento: cinco amostras, orçamento aprovado, dados/ordem
  preservados, rascunho em falha e confirmação persistida; testes/compile/browser.
- Estimativa: executores existentes e serviços/estado envolvidos apenas quando
  o gargalo for comprovado. CBX-001 bloqueia somente recuperação, não os demais
  incrementos. Risco: não transformar medição em refatoração ampla sem evidência.

### CBX-010 — Jornada social

- Fonte: performance 7.1–7.4. Incrementos: leituras perfil/comunidade/feed, depois
  seguir/post/upload/curtida/comentário e gestão do próprio conteúdo.
- Aceite: comparar chamadas/tempo contra CBX-008 em dois viewports, duas contas,
  estados frios/aquecidos, sem N+1, vazamento, omissões ou duplicações; envio único,
  rascunho em falha e limpeza somente de fixtures autorizadas.
- Estimativa: `state/social.py`, transportes e executores sociais existentes.
  Os caches e a correção recente do feed já entregues não são trabalho novo.

### CBX-011 — Administração e consolidação de performance

- Fonte: performance 8.1–8.4/9.1–9.3. Aceite: comparar leituras e mutações
  administrativas contra metas aprovadas; executar jornada integrada e cenário
  habitual/429 controlado, preservando autorização/auditoria/dados e registrando
  regressões, limitações e resultados por camada.
- Estimativa: executores e documentação existentes. Dependências CBX-007/008/009/010;
  comparações independentes podem começar antes, fechamento exige o conjunto.
- Riscos: quotas, contaminação entre contas, comparação entre bases diferentes.
  Não aumentar plano nem aprovar metas arbitrárias como atalho.

### CBX-012 — Fechamento documental do feed

- Fonte: [tasks 6/6 no branch do PR #24](https://github.com/vitordeev/Codeboxd/blob/codex/agente-1/openspec/changes/corrigir-publicacoes-foto-interacoes/tasks.md) e
  delta `social-feed`, ainda diferente da spec principal na base examinada.
- Aceite: sincronizar requisitos sem perder cenários, validar spec/change,
  preservar evidências e arquivar a entrega com seus limites locais explícitos.
- Estimativa: spec principal, diretório da change e índices OpenSpec.
  Testes: comparação semântica, validação OpenSpec e links após movimentação.
  Não confundir arquivamento com publicação ou merge autorizado dos PRs.

## Ordem recomendada

1. Resolver dependências externas de CBX-001/002 e confirmar autorização do
   interpretador; enquanto isso, revisar CBX-003 e os validadores preparados.
2. Validar CBX-004/005/006 independentemente, então CBX-007.
3. Definir baseline/metas em CBX-008; executar os incrementos de CBX-009/010
   e finalizar CBX-011. CBX-012 pode tramitar independentemente.

As dependências são de fechamento e não impedem testes locais seguros.
Nenhum ciclo entre IDs foi introduzido.

## A verificar e sugestões — não são tarefas aprovadas

- Ordenação empatada de catálogo/reports e auditoria concorrente: reproduzir
  antes de declarar bug ou escolher alteração de contrato.
- P.7 `/likes` ausente no último registro: reconsultar apenas com autorização;
  compatibilidade legada já foi implementada, não presumir quebra atual.
- Sobreposição de capa de livro em 390px: registro histórico em PENDENCIAS;
  confirmar no navegador atual antes de abrir correção específica.
- Backup de uploads: verificar existência/integridade da cópia privada. Não
  inferir ausência de backup porque o conteúdo não está no Git.
- CI de testes da aplicação: o workflow localizado prepara Copilot/OpenSpec;
  ampliar automação é sugestão técnica, não requisito funcional ausente.
- Lock integral de dependências, divisão de SocialState e hospedagem são decisões
  de evolução; não impor infraestrutura, Docker ou redesign nesta conclusão.

## Decisões da equipe

Qual caixa/domínio Resend será usado? Interpretador sintético está autorizado?
Quais contas/fixtures reais podem ser usadas e restauradas? Quais metas de cada
jornada devem ser aprovadas? Quando integrar os cinco PRs e o feed comum?
Produção/hospedagem continuam decisões separadas.

## Registro de atualização

- 28/10/2026: criado inventário CBX-001–012 com relação aos IDs existentes,
  separação de hipóteses e critérios de aceite. Sem exclusão ou reabertura de
  entregas históricas. Estado inicial dos PRs e validação conjunta no
  [relatório](../changes/consolidar-auditoria-backlog/revisao-multiagente.md).
