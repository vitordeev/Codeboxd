# Design

## Context

Após fetch, origin/develop está em `29d0456` e origin/main em `faa655f`:
develop não tem commits exclusivos e main tem 23 commits adicionais, incluindo
as PRs #33/#34. UI e Cloudinary partem de main; outras worktrees conservam
cópias anteriores não commitadas. Ver proposal.md para o objetivo.

## Goals / Non-Goals

Salvar conteúdo versionável e atualizar develop sem perda de histórico ou
trabalho local. Não concluir artificialmente changes funcionais, alterar
provedores/contratos ou ativar configurações. Reflex, Xano, TMDB, Kitsu e Open
Library permanecem nas configurações existentes; Jikan continua legado.

## Decisions

1. Criar inventário privado com hashes e cópia dos arquivos alterados antes de
   staging/commits. Comparar com objetos Git alcançáveis pelo remoto; conteúdo
   já publicado não precisa ser commitado novamente. Diferenças de EOL serão
   distinguidas de mudanças de conteúdo; nunca restaurar arquivos do usuário.
2. Commitar UI e Cloudinary em suas branches, com paths explícitos, diff revisado
   e scanner de segredos. Se restar trabalho antigo não publicado, salvar em
   checkpoint separado com origem documentada, sem promover WIP automaticamente.
3. Usar `integration/salvar-develop-20261111`, base origin/main, pois contém
   origin/develop. Merge das frentes novas nessa worktree; resolver documentação
   comum mantendo evidências Cloudinary e progresso atual da UI. Não editar código
   diretamente em develop e não misturar alterações antigas por sobreposição.
4. Preservar os checklists funcionais e testar o conjunto integrado na .venv,
   sem Docker nem APIs de escrita. Validar OpenSpec e compilar Reflex conforme
   skill; testes anteriores de navegador têm sua camada/escopo preservados.
5. Push normal das branches de checkpoint/integração e avanço remoto develop
   somente após verificação. Se o remoto avançar, buscar e reconciliar; jamais
   usar force push. Conferir `ls-remote` e então fast-forward da worktree develop
   se continuar limpa. Credenciais e arquivos ignorados não são parte do envio.

## Risks / Trade-offs

- Cópias antigas parecem alterações novas → comparar blobs com histórico remoto antes de decidir o checkpoint.
- README/PENDENCIAS e o planejamento UI se sobrepõem → reconciliar ambos e preservar os commits de origem para auditoria.
- Artefatos privados em worktrees → staging explícito, scanner permanente e verificação contra valores privados sem imprimi-los.
- Mudança concorrente em develop → push sem force e nova comparação após fetch.
- WIP de performance já tem checkpoint remoto → verificar cobertura antes de reaplicar; qualquer novidade sem aceite segue em branch própria.

## Migration Plan

Inventário → commits por frente → integração → testes/compile/OpenSpec → push
dos checkpoints → push develop → confirmação remota e fast-forward local.
Se testes falharem, corrigir somente a integração coberta ou manter o lote
sem promoção. Rollback futuro usa novos commits revertendo o lote autorizado;
não envolve reset remoto, exclusão de branches ou limpeza de dados.
