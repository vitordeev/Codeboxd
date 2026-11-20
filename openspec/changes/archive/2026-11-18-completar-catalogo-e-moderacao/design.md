## Context

Ver `proposal.md`. A change arquivada solicita `per_page=35` no cliente e o GET administrativo aceita ate 100; o limite nao cria registros ausentes. O ultimo registro historico de catalogo consultado encontrou poucos itens persistidos, mas nao prova a contagem atual. Os provedores existentes sao TMDB para filmes/series e Kitsu para animes; o TMDB depende de `TMDB_READ_TOKEN` e Kitsu nao exige chave.

Reports guardam snapshots e decisao; a atualizacao atual nao remove alvo. Posts possuem DELETE de proprietario com cascade de comentarios/likes e fila de limpeza de imagem. Obras sao referenciadas por interacoes, listas e publicacoes, portanto hard delete arriscaria perder ou quebrar dados de usuarios.

## Goals / Non-Goals

**Goals:**

- Mostrar ate 35 resultados nas categorias, complementando series, animes e livros com consultas externas somente de leitura e sem rotulo de cadastro.
- Dar a equipe uma decisao de remocao contextual por report de post/obra/comentario/avaliacao, com justificativa, confirmacao e auditoria.
- Retirar obras moderadas do catalogo e de novas selecoes sem destruir referencias historicas.

**Non-Goals:**

- Gravar resultados externos, mostrar status de cadastro, importar obras em lote, ou criar registros ficticios.
- Executar importacao ou exclusao em producao nesta sessao; o acesso ao workspace Xano nao esta disponivel.
- Nao remover mensagens ou perfis por esta acao; preservar o status da biblioteca ao moderar uma avaliacao.

## Decisions

1. **Resultados externos somente de leitura.** Series, animes e livros podem completar visualmente a primeira pagina com provedores existentes. Identidades ja persistidas sao deduplicadas; resultados externos nao recebem um marcador de cadastro, controles de edicao ou gravacao. Filmes continuam mostrando somente registros persistidos. A navegacao por categoria usa a barra lateral, sem segunda fileira de abas no topo.

2. **Remocao contextual sob endpoint especifico.** A tela exibe a acao especifica para reports `post`, `media`, `comment` e `review`; o modal exige justificativa e confirmacao final. O novo POST administrativo valida sessao, role, status pendente/em analise, tipo e identidade do alvo sob lock, executa remocao e finalizacao do report/auditoria em transacao.

3. **Post apagado com o caminho de limpeza ja existente.** A transacao remove comentarios, curtidas e post e mantem snapshot/report. Depois da transacao, encaminha a imagem para `PostImages/queue_cleanup`, como no DELETE de proprietario, com identificacao do dono original. Nao remover assets compartilhados diretamente.

4. **Comentario e avaliacao removidos pelo alvo exato.** Comentario: excluir somente a linha `comment`, sem apagar o post. Avaliacao: limpar `rating`, `review` e `spoiler` da interacao mantendo `status` e a relacao com a biblioteca.

5. **Obra removida por flag, nao por DELETE.** Adicionar `moderation_hidden` ao registro de media. Filtrar obras ocultas na leitura publica e impedir novas interacoes, inclusoes em listas e associacoes de post; preserva interacoes, listas, publicacoes e relatarios historicos. O catalogo admin ainda lista a obra com status removido para consulta.

6. **Auditoria independente do status do report.** A mesma transacao salva o report como resolvido, grava a justificativa/revisor/horario e cria evento `admin_report_target_removed` com report, tipo/ID do alvo e decisao. A evidencia reportada continua consultavel pelo snapshot.

## Risks / Trade-offs

- [TMDB token ausente, Kitsu indisponivel ou poucas respostas elegiveis] -> mostrar limite real e resultado parcial; nunca alegar 35 persistidos sem contar a API.
- [Provedor externo indisponivel ou com poucos resultados] -> manter os resultados ja recebidos e os registros persistidos; resultados externos nunca sao gravados.
- [Nova flag nao publicada no Xano] -> mudanca de schema e rotas fica em preflight local; UI so pode assumir aceite integrado apos publicacao manual e verificacao.
- [Falha em cascade de post ou limpeza externa] -> transacao para DB, cleanup pos-commit e evento auditavel; preservar report/snapshot.
- [Consulta publica esquecer o filtro de ocultacao] -> checklist e testes de contrato cobrem feed de catalogo e endpoints de novas interacoes/listas.

## Migration Plan

1. Adicionar campo `media.moderation_hidden` com default `false`, confirmar/backfill `false` nos registros existentes e fazer preflight local dos endpoints Xano afetados.
2. Implementar telas/estado e contratos locais; testar resultados externos de leitura, deduplicacao, falha parcial e remocao por tipo/permissao.
3. Revisar o bundle Xano e o plano de rollback sem publicar. Publicacao exige workspace Xano disponivel; nao executar este passo aqui.
4. Rollback local: reverter arquivos desta change. Se publicada, primeiro desativar a acao de remocao; flag default false mantem catalogo existente, reverter filtros e endpoint depois. Nao apagar historico de eventos, reports nem refs.

## Open Questions

Nenhuma para a implementacao local. Quantidade exibida depende dos resultados atuais dos provedores e do catalogo; aceite remoto permanece separado.
