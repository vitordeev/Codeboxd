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
