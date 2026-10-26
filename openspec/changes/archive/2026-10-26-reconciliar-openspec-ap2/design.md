## Context

Em 26/10/2026, os checklists funcionais indicam administração 21/34, performance 14/37 e recuperação 8/10. Há 19 specs consolidadas e 14 diretórios de arquivo anteriores. Os documentos misturam atualizações de 13–24/10.

## Goals / Non-Goals

Estabelecer uma visão atual única, corrigir referências quebradas comprovadas e explicitar datas e camadas de validação. Não concluir funcionalidades por contagem, não alterar evidência bruta histórica nem revalidar serviços externos.

## Decisions

- O checklist com evidência prevalece sobre resumos antigos; tarefa parcial continua aberta.
- Relatórios datados são históricos e permanecem preservados. Documentos centrais recebem visão atual e separação explícita do histórico.
- Arquivos históricos duplicados por tema e datas diferentes são preservados como registros distintos, sem fusão ou exclusão automática.
- Leituras reais de admin registradas na performance não substituem mutações, autorização completa e browser exigidos pela change administrativa.
- A revisão é documental, sem deltas de comportamento, usando `skip_specs: true`.

## Risks / Trade-offs

Validação CLI verifica estrutura, não prova funcionamento nem equivalência semântica integral entre código e specs. Indicar esses limites na evidência final. Manter histórico pode conservar textos com problemas antigos de codificação; corrigir a apresentação atual sem inventar conteúdo histórico.

## Migration Plan

Registrar inventário, reconciliar os centrais, executar verificações documentais e arquivar esta revisão quando concluída. Rollback por diff dos arquivos documentais desta rodada, preservando alterações preexistentes do usuário.
