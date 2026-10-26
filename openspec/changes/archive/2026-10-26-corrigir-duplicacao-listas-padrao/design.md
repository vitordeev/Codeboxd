## Context

Ver proposal.md e diagnostico.md. Consulta real em 26/10 encontrou 19 listas de 8 proprietários, 16 padrões públicas e zero duplicatas padrão por proprietário. O carregamento local mistura GET /lists/public e GET /lists por ID. A investigação não acessou o navegador da sessão relatada.

## Goals / Non-Goals

**Goals:** apresentar a coleção pessoal corretamente, manter descoberta pública identificada e prevenir criação concorrente de padrões.

**Non-Goals:** executar reset histórico, apagar listas apenas pelo título ou modificar catálogo, interações e integrações TMDB/Kitsu/Open Library; identidade Jikan legada permanece intacta.

## Decisions

- Continuação backend: chave anulável `default_key` em `user_list`, com índice único; valores `<user_id>:planned` e `<user_id>:completed`. Listas personalizadas ficam com chave nula e podem ter títulos iguais. Função compartilhada de preparação consulta por chave, insere quando ausente e, em conflito concorrente, relê a chave sem sobrescrever título, descrição ou privacidade. Cadastro e POST de listas com `default_kind` explícito usam essa função. O app somente usa o novo contrato após ativar `DEFAULT_LIST_IDENTITY_ENABLED`, desabilitado por padrão até publicação e identificação revisada das listas legadas. Migração não identifica listas apenas pelo título.

- Ajuste autorizado do cabeçalho: usar grid com coluna fixa de 44px para avatar à esquerda e coluna flexível para o nome à direita. Nomes longos quebram somente dentro da coluna de texto, sem deslocar o nome para baixo da foto.

- Refinamento autorizado: agrupar as listas públicas pelo ID do proprietário, exibindo um cabeçalho com avatar e nome ligados ao perfil. Consultar perfis em lote somente na descoberta pública; falha ou perfil ausente usa apresentação neutra sem atribuir outro autor e mantém as listas acessíveis. Preservar a ordem de primeira ocorrência dos autores e a ordem das listas de cada autor. Paginação visual limita listas antes de agrupar, mantendo “Mostrar mais”.

- Separar estado e apresentação de listas próprias e descoberta pública, indicando propriedade nesta última. Filtrar somente pelo título foi descartado porque ocultaria listas legítimas de outros usuários sem corrigir a origem da confusão.
- Usar identidade estável de tipo padrão por proprietário no backend, com garantia atômica de unicidade compatível com Xano. Confirmar esquema e contrato publicados antes da alteração; bloqueio apenas em um processo Reflex não protege múltiplas sessões.
- Tornar preparação independente da primeira página; observar conta e credencial durante toda leitura. Cadastro e preparação devem convergir à mesma identidade padrão, sem reservar títulos de listas personalizadas como identificação definitiva.
- Preservar dados existentes: inventariar candidatos legados por dono/título e contexto, sem classificar automaticamente lista personalizada homônima. Há zero duplicatas confirmadas; reconciliação atual deve resultar em nenhuma escrita. Se surgirem conflitos, backup privado, plano revisável e união de itens precedem qualquer remoção; manter privacidade mais restrita e interromper ambiguidades.

## Risks / Trade-offs

- Mudança de navegação → manter descoberta pública acessível em contexto identificado e validar visitante/membro.
- Concorrência e legado sem identidade de tipo → revisar candidatos, testar simultaneidade real e não inferir publicação por testes simulados.
- Listas grandes → verificar paginação completa e seleção sem perda de itens.
- Resultado de outra conta → invalidar estado e rejeitar respostas tardias.

## Migration Plan

Primeiro corrigir separação visual e testar com duas contas. Depois revisar delta remoto mínimo para identidade padrão e criação idempotente, com backup de contratos/esquema e dados afetados antes de publicação. Registrar remoto e navegador separadamente. Não há limpeza de dados justificada pelo diagnóstico atual. Rollback deve restaurar contratos/interface compatíveis sem apagar itens ou repetir migração histórica; preservar backups e evidências. Execução local em `.venv`, sem Docker.
