# Arquivamento autorizado — 26/10/2026

O usuário solicitou verificar e arquivar as changes concluídas. Esta change tem 9/9 tarefas, quatro artefatos completos, evidência sanitizada de rotação TMDB, senhas e revogação pela dependência concluída, além de validação OpenSpec aprovada. As outras três changes funcionais têm tarefas abertas e permanecem ativas.

Antes de mover a pasta, foram sincronizados os três requisitos ADDED de operational-reliability com a spec principal, preservando Purpose e requisitos anteriores. A comparação integral confirmou que não resta delta por aplicar. O destino previsto é changes/archive/2026-10-26-proteger-credenciais-expostas; não havia diretório de destino existente.

Artefatos de implementação e evidências anteriores são preservados. Ajustes de localização em links entre changes são parte do arquivamento e não alteram seus resultados. Os comandos de validação datados nos relatórios e scripts dentro desta pasta são históricos: não reexecutá-los diretamente após mover a change, pois dependem da localização e podem sobrescrever evidências. Novas investigações/alterações exigem change ativa e novos destinos de resultados. O scanner permanente tools/check_staged_secrets.py permanece disponível independentemente do arquivo.

Esta rodada não executa novamente testes remotos, não altera credenciais, não inicia Docker e não faz git add, commit ou push. Evidências anteriores de 392 testes locais, 29 checks remotos e navegador foram conferidas como registros da implementação; não são novas execuções desta rodada. Resultado final de validação documental em openspec/VALIDACAO.md.

Arquivamento concluído pelo CLI com --yes --skip-specs após merge e comparação dos deltas; validação permaneceu habilitada. Ao final, 22 itens ativos/specs e 17 arquivados aprovados. Os 41 artefatos anteriores das duas entregas foram conferidos contra o conteúdo versionado (CRLF normalizado), com apenas três links Markdown entre pastas ajustados. Há um link pré-existente para log ausente na change administrativa ativa, fora do escopo; não há link quebrado nesta entrega arquivada.
