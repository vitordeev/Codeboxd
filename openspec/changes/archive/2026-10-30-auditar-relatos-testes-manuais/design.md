# Design

## Context
Consultar proposal.md. O relatório não identifica versão, conta, navegador, tempos ou respostas HTTP.

## Goals / Non-Goals
Rastrear seis problemas por IDs estáveis e critérios verificáveis; implementação depende de autorização posterior.

## Decisions
Usar docs/planning como apresentação solicitada e esta change como registro central no OpenSpec. Referenciar código por arquivo, função e linha. Não duplicar specs nem encerrar pendências históricas. Priorizar integridade das conexões antes da validação integrada do feed.

## Risks / Trade-offs
Código Xano local pode divergir do publicado → tratar contrato local como evidência estática, sem afirmar execução remota. Ausência de reprodução → manter os seis relatos abertos, mesmo quando há fragilidades confirmadas no código.

## Migration Plan
Sem migração ou implantação. Reversão documental por revisão dos arquivos novos, preservando trabalho alheio.
