# Implementação e preparação da implantação — 03/11/2026

## Autorização e limites

Após conferir o estado remoto, o usuário solicitou implementar. Proposal,
design e tasks foram atualizados antes de editar os contratos. A execução
remota passa a estar autorizada com backup, prévia, ensaio e rollback, sem
ampliar o escopo para outras changes. Preservado o histórico da rodada manual.

O plano gratuito recusou os dois recursos de isolamento previstos: branch e
fonte de dados. Foi solicitada decisão entre ensaio com contas descartáveis e
rotas temporárias na instância atual ou outro workspace. A publicação depende
dessa decisão e do ensaio correspondente; não houve corte ou migração live.

## Contratos locais implementados

15 documentos Xano, com GUIDs existentes preservados e cinco novos documentos:

- `user_media_list_status`, com enum e índice único usuário/obra, mais índice de projeção.
- Funções `Lists/set_media_list_status` e `Lists/default_list_status`.
- GET/PUT `/media-list-status/{media_id}`, com sessão verificada e status anulável.
- PUT/DELETE follow transacionais com lock do ator, confirmação de estado,
  filtro por par e remoção de todas as conexões residuais ao deixar de seguir.
- Índice composto único de follow e índice user_id/id do post.
- Feed mantém consulta direta dos seguidos e passa a per_page padrão 20.
- GET privado/público, POST de item, DELETE condicional de item e DELETE de lista
  padrão delegam à fonte nova. Personalizadas preservam a lógica anterior.
- Identidade por default_key validada contra o proprietário; título homônimo
  não converte uma personalizada em padrão. Privacidade e guards preexistentes
  permanecem antes do acesso aos itens.
- Organização altera somente status/updated_at da interação existente; não
  sobrescreve rating/review/spoiler. Remover da lista não remove a avaliação.

Arquivos em `xano/table`, `xano/function/Lists` e `xano/api/codeboxd`.
Nenhuma alteração nova no Reflex, CSS, flags, provedores ou rotas frontend.

## Backup e plano revisável

Backup privado em `.local/conexoes-feed-listas/deployment-2026-11-03/`, ignorado
pelo Git, sem valores de ambiente nos exports de contratos. Foram preservadas
as tabelas user, profile, user_follow, post, user_list, user_list_item,
user_media_interaction, media, comment e post_like. Nenhum valor pessoal ou
credencial foi copiado para esta evidência.

Inventário: 8 usuários, 11 perfis, 14 follows, 10 posts, 20 listas, 12 itens,
22 interações, 23 obras, 6 comentários e 4 likes. O plano migraria **6 itens
padrão para 5 relações**, com **1 conflito resolvido a favor de Assistido**.
Seis itens fora dessas listas ficam preservados, inclusive três itens órfãos
antigos de uma lista inexistente. Três follows com referência órfã também ficam
preservados; não há pares duplicados ou chaves não canônicas a corrigir neste
snapshot. Não foram inventados usuários ou listas para reparar órfãos históricos.

Ferramentas locais:

- `tools/list_status_contracts.py`: monta o candidato restrito sem env/records;
  inclui gerador idempotente dos desvios nos contratos existentes.
- `tools/list_status_migration.py`: plano determinístico, precedência de Assistido,
  validação de referências das padrão, preservação integral dos demais registros
  e recusa de backup diferente do plano.
- `tools/list_status_deployment.py`: prévia com verificação de drift e escopo
  exato; prepara pacote privado de rollback. Não possui comando de publicação.

Rollback preparado: **10 contratos originais** e **6 itens padrão com IDs e
campos originais**; lista dos cinco objetos novos para revisão posterior.
Exige escritores bloqueados e não permite assumir rollback automático seguro
depois de liberar escritas. Pacote preparado, **restauração real ainda não
ensaiada**; não é uma alegação de ferramenta de corte live concluída.

## Prévia remota e recursos de teste

- Prévia inicial de 14 documentos → HTTP 200, sem warnings/parse errors.
- Prévia final de 15 documentos, incluindo feed → **aprovada** com escopo
  exato: 1 tabela nova, 2 tabelas alteradas, 2 funções novas, 2 rotas novas,
  8 rotas alteradas. Nenhuma exclusão, env ou record no payload.
- Candidato SHA-256:
  `41983d2019da959aa2e92026d809d1574f835e14a17481857402f9e185193294`.
- Hash e operações sanitizadas em [preview-2026-11-03.json](preview-2026-11-03.json).
- POST branch de teste → HTTP **500**, `Branch creation is restricted to paid accounts.`
- POST fonte de dados de teste → HTTP **403**, `Not supported. Please upgrade your Xano instance.`
- Não houve aprovação/rejeição automática de segurança: as recusas são limitações
  de funcionalidade retornadas pelo Xano. Nenhum desses recursos foi criado
  segundo as respostas; fonte live e branch ativa não foram substituídas.

## Validação local

- `.venv/Scripts/python.exe -B -m tools.list_status_migration`
  → plano com 5 statuses/6 itens/1 conflito; zero escritas remotas.
- `.venv/Scripts/python.exe -B -m tools.list_status_deployment prepare-rollback`
  → 10 contratos/6 itens para restauração; zero escritas remotas.
- `.venv/Scripts/python.exe -B -m tools.list_status_deployment preview`
  → passed=true, published=false, escopo exato e backup sem drift.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p 'test_list_status*.py' -v`
  → **13 testes OK**. Cobrem conflito, homônimo, preservação de avaliações e
  metadados privados, chave vazia/cruzada, referências inválidas nas padrão,
  251 itens, plano repetido, drift, follow legado e pacote restrito de rollback.
- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_session_revocation.py -q`
  → **4 testes OK**. A contagem passou de 40 para 42 rotas locais autenticadas
  devido aos dois endpoints novos, ambos com guard antes de qualquer ação.
- Primeira suíte completa → 475 testes, uma falha na contagem antiga de 40
  endpoints; contagem corrigida para 42, sem retirar a verificação de guard.
- Suíte final, após ajustar a contagem e adicionar cobertura do pacote de
  rollback → **477 testes OK**, 28,614 s. Os 13 testes de plano/deployment e
  quatro de revogação estão contidos nesse total, não são somados a ele.
- `openspec validate corrigir-conexoes-feed-listas --type change` → válida.
- `git diff --check` → sem erros de whitespace, avisos LF/CRLF. Backup privado
  confirmado ignorado por `git check-ignore`. Tarefa 4.1 concluída; **7/10**.

Sem benchmark, navegador autenticado, publicação, backfill, limpeza de dados
existentes, e-mail, reinício, Docker ou commit nesta rodada. Testes de plano e
pacote não substituem ensaio de transação/lock/rollback no Xano.

## Próximo passo dependente de decisão

Escolher o ambiente de ensaio. Depois: validar candidato/rollback nesse
ambiente, preparar bloqueio de todos os escritores envolvidos, conferir drift,
aplicar somente os dados/contratos do plano, verificar preservação e liberar
escritas. Não encerrar 3.2/4.2/4.3 antes das evidências reais exigidas.

Referências consultadas:
https://docs.xano.com/the-function-stack/functions/database-requests/get-record
e https://docs.xano.com/the-function-stack/functions/database-requests/database-transaction.
