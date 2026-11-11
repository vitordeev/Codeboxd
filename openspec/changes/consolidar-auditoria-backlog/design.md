## Context

Ver proposal.md. Base de implementação da rodada: develop `da30b39`; referências
remotas atualizadas por fetch, main remoto `fce53ae`. A aplicação usa Reflex e
Xano; TMDB, Kitsu, Open Library e DeepL, com identidades Jikan legadas. Nenhum
provedor será trocado nesta documentação.

## Goals / Non-Goals

**Goals:** conhecimento versionável, requisitos rastreáveis e revisão dos PRs.
**Non-Goals:** declarar aceite remoto por mocks, conceder privilégios, publicar,
aprovar metas numéricas sem a equipe ou integrar definitivamente branches.

## Decisions

- Usar `openspec/planning/` conforme AGENTS.md, preservando os documentos centrais.
  Alternativa `docs/planning/` foi descartada pela convenção explícita do projeto.
- CBX identifica acompanhamento; os IDs das changes continuam sendo a fonte de
  aceite. Não somar as duas listas nem redefinir requisitos.
- Evidência local, interpretador, API publicada e navegador serão separadas.
- Registrar cinco worktrees independentes; limite de três implementadores
  concorrentes exige duas ondas. Modelos herdados são identificados como tal,
  sem simular troca ou afirmar o custo efetivo da conta.

## Risks / Trade-offs

- Documentação histórica pode estar superada → citar data, evidência e limite.
- Ferramenta preparada pode parecer validação executada → declarar a camada.
- Todos os PRs incluem o feed preexistente → registrar o commit comum e rever
  a base antes do merge; não descartar trabalho anterior.

## Migration Plan

Somente arquivos documentais novos na integração temporária. Rollback consiste
em reverter seu commit, preservando as fontes e os cinco PRs. Sem migração de dados.
