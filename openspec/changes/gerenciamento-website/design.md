## Context

Ver `proposal.md` para a motivação e `specs/` para os contratos observáveis. O projeto usa Reflex no frontend e Xano para autenticação e dados. A rota `/admin` já tem um placeholder protegido por `AuthState.guard_admin`, e a sessão reconhece o papel `admin`; isso protege a navegação, mas operações de gerenciamento ainda precisam ser verificadas nos endpoints do Xano. O catálogo social separa registros persistidos de dados fornecidos por provedores externos.

## Goals / Non-Goals

**Goals:**

- Evoluir o placeholder administrativo em uma área com navegação consistente e módulos desacoplados por domínio.
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
6. Publicar primeiro as estruturas e endpoints compatíveis, depois a interface. Para rollback, desabilitar a rota administrativa e restaurar endpoints anteriores sem apagar reports ou registros de auditoria.
