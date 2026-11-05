## Context

### Execução autorizada em 03/11/2026

Continuação após o pedido explícito de finalizar: ensaio na instância atual
com isolamento por contas descartáveis e prefixo temporário de endpoints,
pois branch/fonte separadas foram recusadas pelo plano. Não há isolamento de
banco: os testes só podem alterar IDs próprios registrados no journal. Publicar
primeiro apenas a tabela/funções aditivas e cópias das rotas sob prefixo novo;
conferir que nenhum contrato preexistente mudou. Ensaiar alternância,
concorrência, privacidade, paginação e restauração de registros de teste antes
do corte. Remover rotas/contas temporárias por identidade exata no encerramento.
Registrar separadamente efeitos sobre dados de teste e migração dos seis itens
existentes. Esta decisão substitui a pendência de escolha do ambiente.

Depois da conferência de leitura, o usuário solicitou a implementação remota.
Usar o acesso administrativo já validado, sem ampliar para outras changes.
Criar contratos Xano locais e ferramentas desta change com saídas privadas
próprias em `.local/conexoes-feed-listas/`, sem reutilizar destinos históricos.
Antes de publicar: export sem env/records, backup privado das tabelas afetadas,
inventário de conflitos e prévia restrita. Ensaiar em branch/fonte isolada se
disponível; verificar recursos antes de qualquer corte. Suspender os escritores
afetados durante migração, comparar snapshot contra drift e manter o bloqueio
até verificar preservação. Novos statuses são derivados por default_key,
Assistido vence, personalizadas e avaliações permanecem intactas. Validar
contratos e índice/lock pela API de prévia antes de assumir sintaxe suportada.
Rollback restaura somente stacks/itens alterados, com journal e IDs originais;
não apagar tabela nova ou dados se surgirem gravações posteriores ao corte.
Ensaios reais usam contas descartáveis criadas pelo signup normal e limpeza
restrita por IDs/journal; não impersonar contas existentes com metadados.
Só concluir aceite quando os critérios tiverem evidências correspondentes.

Ver proposal.md e investigation.md. Ambiente .venv confirmado: Reflex
0.9.11.post1; três skills Reflex disponíveis. O XanoScript do repositório não
comprova o contrato publicado. Nenhuma conexão ao workspace será tentada.

## Goals / Non-Goals

Confirmar mutações e manter exclusividade nas listas padrão. Não modificar
avaliações, nomes de listas, fontes de catálogo ou comportamento personalizado.

## Decisions

- Follow valida resposta `{follower_id, followed_id, following}`. Aceitar o
  registro legado em PUT se os dois IDs corresponderem; DELETE legado sem estado
  será confirmado lendo `/profiles/{actor}`. Não inferir sucesso de `{}`.
- Fixar sessão/conta/contexto durante requisições e impedir sobreposição local.
- Manter posts próprios no feed como hoje, mas falha não autorizativa nessa
  consulta não descarta posts seguidos. `/feed` continua fonte de seguidos;
  likes opcionais não impedem mostrar posts em falhas transitórias.
- Estado separado de lista (`selected_list_status`) é carregado por obra; não
  usar `selected_status` do editor de avaliação como confirmação de lista.
- PUT de status único transacional no Xano; GET por mídia não pagina nem depende
  dos primeiros 100 registros de interações. Nenhuma compensação em duas chamadas
  Python pode garantir integridade; rejeitar esse fallback.
- Atualizar leitura e escrita de TODAS as rotas de listas padrão no Xano para
  usar a relação nova, sem manter cópias concorrentes em user_list_item.
- A função de status mantém a atualização do status de consumo que o atalho
  já realizava, mas preserva os campos de avaliação existentes. O cliente
  aplica completed/planned no controle superior pelo enum confirmado. Nenhum
  estado de lista não equivale a excluir uma avaliação da biblioteca.

## Risks / Trade-offs

Backend ainda antigo → erro explícito nos atalhos até aplicar roteiro manual.
Concorrência entre clientes → serialização por usuário no backend e índice
composto único. Falha de resposta após commit → recarregar GET antes de novo
toggle; PUT com estado desejado é idempotente. Resposta antiga → descartar pelo
contexto e geração. Migração parcial → bloquear publicação até ensaio/restauração.

## Migration Plan

Backup, auditoria, deduplicação e migração manual descritos em xano-changes.md;
publicar backend primeiro, Python depois. Rollback coordenado: restaurar stacks
e snapshot, reverter somente arquivos desta change. Sem execução remota aqui.
Referência Reflex: https://reflex.dev/docs/events/events-overview/ e
https://reflex.dev/docs/state/overview/ (consultadas nesta rodada).
