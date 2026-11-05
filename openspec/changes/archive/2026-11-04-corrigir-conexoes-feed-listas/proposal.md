## Why

Retomada de 03/11/2026: após a auditoria remota, o usuário pediu implementar
a migração. Essa autorização substitui a restrição anterior de aplicação
manual nesta entrega: o agente pode preparar, ensaiar e aplicar o contrato
restrito com backup, prévia, rollback e validação. O escopo funcional permanece
o mesmo. Os trechos anteriores abaixo que dizem sem acesso/publicação descrevem
a rodada de 29/10, não limitam esta continuação expressamente autorizada.

Seguir alguns perfis falha, o feed parece depender da primeira publicação e as
listas padrão permitem a mesma obra nos dois estados. Corrigir confirmação das
ações e integridade, sem atribuir ao backend remoto fatos não verificados.

## What Changes

- Seguir/deixar de seguir idempotentes, IDs normalizados, bloqueio durante envio
  e estado confirmado pelo servidor; erros visíveis.
- Feed independente da existência de posts próprios, com erro separado de vazio.
- Listas padrão mutuamente exclusivas por relação única usuário/obra; atalhos
  enviam estado desejado e atualizam botões pela resposta confirmada.
- Entregar mapa de chamadas e roteiro manual Xano, sem acesso/publicação remota.

## Capabilities

### New Capabilities
Nenhuma.

### Modified Capabilities
- `social-connections`: confirmação e idempotência das conexões.
- `social-feed`: carga independente de publicação própria e distinção erro/vazio.
- `user-lists`: exclusividade nas duas listas padrão e confirmação visual.

## Impact

`Codeboxd_main/state/social.py`, `pages/social.py`, `assets/codeboxd.css`, testes com mocks e contratos
descritos em xano-changes.md. **BREAKING**: novos GET/PUT `/media-list-status/{media_id}`
e respostas confirmadas em `/follows/{user_id}` exigem atualização manual Xano
antes do uso. Não haverá fallback para as duas escritas antigas inseguras.
Sem mudança de provedores, avaliações, listas personalizadas, Docker ou deploy.

## Suposições explícitas

- Clicar no status já ativo remove a obra das duas listas padrão (estado nenhum).
  A API recebe o estado desejado, não uma ordem de toggle, para repetição segura.
- Usar `media_id` (identificador interno, não ID TMDB) e abranger os atalhos já
  existentes de filmes/séries/animes/livros, preservando nomes visuais atuais.
- Relação nova `user_media_list_status` com enum `watched|want_to_watch` evita
  apagar nota/review da relação `user_media_interaction`. As listas padrão são
  projeções dessa relação; personalizadas continuam independentes.
- Preservar a compatibilidade do atalho com o status de consumo da biblioteca:
  backend atualiza apenas esse status ao selecionar uma das listas, sem zerar
  nota/review/spoiler. Remover da lista não apaga a interação/avaliação.
- Na limpeza de conflitos, Assistido vence. Identificação de listas por
  `default_key`, nunca só pelo título. Legados sem chave exigem revisão manual.
- `openspec/project.md` ausente: contexto obtido de README, CONTEXTO, HISTORICO,
  PENDENCIAS, specs consolidadas e changes relacionadas. Pasta preexistente
  `corrigir-follow-feed-status-filmes` preservada. Auditoria documental
  `auditar-relatos-testes-manuais` não é autorização nem evidência de correção.
