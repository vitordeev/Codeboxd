## Context

O ambiente `venv` executa a suíte, mas `.venv` não possui dependências. `.env`, `.local/`, `.web`, estados, caches e uploads aparecem no índice. O commit que inclui `.env` está em `origin/main` conforme as referências locais. Nenhum valor secreto será incluído nos relatórios.

## Goals / Non-Goals

**Goals:** corrigir defeitos locais comprovados e registrar verificações reproduzíveis.

**Non-Goals:** reescrever histórico compartilhado, rotacionar chaves sem procedimento externo, publicar endpoints, criar domínio ou encerrar validações administrativas/remotas sem evidência.

## Decisions

- `.gitignore` protege ambientes, segredos, arquivos gerados e uploads. Remoção do índice usa operação cached; arquivos locais são preservados. Não remover fontes, assets ou lockfiles mantidos intencionalmente.
- `.venv` será o ambiente canônico, conforme a skill de setup. `venv` permanece como cópia de compatibilidade, sem exclusão. Fixar versões das dependências diretas às já verificadas no ambiente existente.
- Mensagens usam texto Unicode real. Não alterar política de autorização/status do transporte.
- Banner usa URL string do endpoint de upload configurado no servidor. `rx.get_upload_url()` retorna Var de frontend e não deve ser usado no payload de backend. Testar URL concreta, persistência de arquivo e limpeza após rejeição da API.
- Por decisão explícita do usuário, execução local com `.venv`, sem adicionar ou utilizar Docker. Ajustes de Dockerfile/Compose feitos nesta rodada foram revertidos; o scaffolding anterior foi preservado.

## Risks / Trade-offs

- Retirar arquivos do índice não apaga histórico → chaves publicadas precisam de rotação e avaliação do histórico em procedimento separado.
- Documentos históricos → atualizar apenas contexto atual, preservando evidências e arquivos arquivados.

## Migration Plan

Instalar `.venv`; remover arquivos ignorados apenas do índice; executar testes/compilação; manter execução local. Rollback preserva os arquivos locais; Docker foi retirado desta etapa.
