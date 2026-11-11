## Context

Origem protegida: configuração privada atual, workspace 147717, branch v1/live.
Um perfil e um workspace acessíveis foram observados. O usuário escolheu
homologação e autorizou prepará-la; o piloto administrativo continua separado.
CLI instalado @xano/cli 1.2.0. Sandbox pessoal é provisionado por GET /sandbox/me,
portanto esse GET não é leitura pura. Fonte: implementação instalada e CLI oficial.

## Goals / Non-Goals

Preparar contratos e validar isolamento para homologação administrativa remota.
Sem copiar contas, senhas, uploads, env ou registros; sem Docker, mudanças em
produção, compras de plano, reset de sandbox existente ou mutações do piloto.
Não construir uma réplica integral das funcionalidades externas do aplicativo.

## Decisions

- Preferir sandbox pessoal Xano vazio, cuja criação isolada está no escopo do
  pedido atual. Primeiro gerar/revisar pacote local. Depois obter sandbox sem
  reset; se já contiver conteúdo, parar. Se negar plano/licença, registrar erro
  sanitizado e não tentar contornar comprando plano ou usando live como fallback.
- Alternativa futura: workspace/instância de homologação separados; requer
  disponibilidade/identificação e aprovação própria, sem apagar o workspace atual.
- Continuação autorizada da preparação: após recusa do sandbox, tentar uma única
  criação de workspace vazio `codeboxd-homologacao-admin`, sem duplicar nome já
  existente. A aprovação do pedido de preparar ambiente isolado cobre essa
  obtenção de recurso vazio, não publicação/seed ou mudança de plano. Se recusado,
  parar; se timeout/erro incerto, reconciliar por GET antes de qualquer nova ação.
- Pacote local allowlist: 13 tabelas Codeboxd (exclui titulos legado), funções de
  sessão/listas/log, dois grupos, três rotas auth, oito admin e três rotas de
  apoio (posts POST, reports POST, interactions GET). Totais verificados ao gerar.
- Remover somente atributos GUID e canonical de documento que não devem ser
  herdados. Não reescrever código de negócio ou identidade de conteúdo. Excluir
  workspace/AI/addon legado, e-mail/reset, tasks/triggers, dados e env. Bloquear
  transporte HTTP externo/util.send_email e padrões de segredos literais.
- Gerar bundle/manifesto em diretório privado exclusivo, sem sobrescrever uma
  preparação anterior; publicar em OpenSpec apenas resumo sem código/segredos.
- Configuração de homologação em arquivo privado próprio e exemplos com
  placeholders. Nada altera .env atual ou perfil padrão do CLI. Identificar
  public origin distinto para sandbox; para workspace, host+ID devem diferir da origem.
- Antes de publicar, comprovar alvo vazio e produzir dry-run sem records/env/
  delete/truncate. Mostrar prévia; publicação remota continua exigindo aprovação
  específica. Não criar admin/fixtures até destino e contratos estarem verificados.

## Risks / Trade-offs

- Plano pode recusar sandbox/workspace adicional: não inferir elegibilidade por
  documentação de preço ou comandos help; distinguir recusa real de preparação local.
- Sandbox pessoal pode estar em uso: descoberta nunca autoriza reset ou sobrescrita.
- Bundle local pode divergir de contratos publicados: comparar estrutura necessária
  antes do aceite; manifesto não comprova compatibilidade do provedor sozinho.
- Código de apoio auth/me gera auditoria ao ser chamado: testes posteriores devem
  preservar eventos; ausência de envio externo não significa ausência de auditoria.
- API base gerada no destino pode mudar: não usar canonical original nem URLs
  herdadas; validar origens/grupos após publicação, com sessão sintética própria.

## Migration Plan

Planejar, gerar pacote e testes locais; descobrir/criar somente recurso isolado;
conferir destino e ausência de conteúdo; gerar prévia; publicar só após aprovação;
verificar estrutura vazia e configurar ambiente separado; retornar ao piloto
administrativo com sua própria autorização A2–A4. Se houver recusa externa, manter
tarefas remotas abertas e informar opções reais. Sem rollback destrutivo automático.
