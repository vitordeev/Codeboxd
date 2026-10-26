# Identidade estável das listas padrão — 26/10/2026

> Plano e evolução da publicação preservados. Execução final, cobertura de navegador e limpeza concluídas em [conclusao.md](conclusao.md).

## Preparação e escopo

Backup privado em `.local/default-list-integrity/deployment/`: 79 documentos sem ambiente/records, 19 listas e 8 vínculos com obras. Exportação e leitura reais confirmam três GUIDs existentes no delta. Dry-run remoto aprovado para tabela user_list (campo anulável e índice único), função Lists/ensure_default_list e endpoints signup/list creation; nenhum delete, segredo ou record no multidoc.

Chave `default_key` = `<dono>:planned` ou `<dono>:completed`, nula nas personalizadas. Função compartilhada não atualiza dados quando encontra a chave e relê após conflito de inserção. Cadastro chama a função dentro da transação já existente. POST normal continua criando lista personalizada; tipo padrão deve ser explícito e deriva o dono da sessão.

## Plano revisado para listas legadas

O backup contém exatamente um par por proprietário, com título **e descrição originais**. Revisão individual dos IDs do snapshot: 24/25 (dono 6), 26/27 (7), 28/29 (8), 30/31 (9), 32/33 (11), 34/35 (12), 36/37 (14), 43/44 (18). Em cada par, primeira lista é planned e segunda completed. Essas 16 atribuições são limitadas aos IDs e ao hash do snapshot; a ferramenta interrompe se houver ambiguidade ou mudança desde o backup. Não é uma regra geral de classificação por título. As três listas personalizadas ficam com chave nula.

Backfill altera somente default_key. Deve comprovar mesmos IDs, títulos, descrições, visibilidades, timestamps e oito vínculos após a operação. Nenhuma exclusão ou união de registros é necessária: não há duplicatas confirmadas.

## Publicação e rollback

Publicação exige preview aprovado do mesmo hash e snapshot inalterado. Após aplicar, exportar novamente e conferir que documentos alheios não mudaram. Aplicação só habilita DEFAULT_LIST_IDENTITY_ENABLED após backfill e validação real; flag desabilitada por padrão em .env.example.

Rollback sem apagar dados: desabilitar flag e restaurar os blocos signup/list creation do baseline com importação parcial sem records/env/delete. Manter campo anulável, índice e função inativos preserva dados e evita remoção de esquema. Se necessário, reverter somente as 16 chaves nos IDs do journal para null, mediante nova comparação dos registros e backup. Nunca repetir o reset histórico.

## Validação planejada

Continuação executada: publicação aprovada e exportação posterior com zero documentos alheios alterados; backfill de 16 chaves comprovou preservação das 19 listas e 8 vínculos. Evidências em backend-publication.json e backend-backfill.json. `DEFAULT_LIST_IDENTITY_ENABLED=true` configurado privadamente e app normal recompilado/recarregado em produção na porta 3030.

API real: 18 checks aprovados em default-lists-remote.json, incluindo cadastro com duas chaves, três solicitações concorrentes retornando um ID, padrão renomeado e privado preservado, duas listas personalizadas homônimas com chave nula, tipo inválido/visitante rejeitados, isolamento e rejeição de mutação entre contas. Nenhuma senha alterada ou e-mail enviado. Primeira rodada sofreu 429 após a corrida já aprovada; interrompida sem retry, conta descartável limpa e preservação original verificada. Segunda rodada foi iniciada explicitamente com pausas de 3,5s e passou.

Suíte completa: 411 testes aprovados, também após habilitar a configuração real. Fixtures legadas agora isolam a feature explicitamente; testes do novo contrato habilitam a feature. Expectativas de chamadas da simulação biblioteca/listas foram atualizadas para refletir a coleção pessoal sem diretório público (3 chamadas/7 listas pequenas, 7 chamadas/252 listas grandes, revisita sem chamadas). Compilação dry-run e build normal aprovados. Validação de navegador real com duas contas e limpeza final em andamento.

Uma conta descartável explícita verificará cadastro e corrida de preparação: remover somente uma lista padrão vazia dessa conta de teste e fazer solicitações concorrentes para o mesmo tipo; exigir um ID persistido. Comparar isolamento com conta controlada existente. Limpeza limitada aos registros criados nessa conta e na lista de teste; journal privado e verificação posterior. Nenhuma senha será alterada e nenhum e-mail será enviado. Essa conta existe exclusivamente para verificar os critérios de cadastro/concorrência desta change, não como efeito incidental de outro script.

Testes locais da identidade: reaproveitar listas renomeadas/privadas, não confundir personalizada homônima, ler página adicional, rejeitar resposta de outra conta e falha sem retry automático. Seis testes do planejador de reconciliação cobrem união de obras, privacidade mais restrita, metadados divergentes, conflito de dono, ausência de duplicatas e snapshot inválido.

Fontes consultadas: [schema/índices XanoScript](https://docs.xano.com/xanoscript/db), [operações de banco](https://docs.xano.com/xanoscript/function-reference/database-operations), [try/catch](https://docs.xano.com/xanoscript/function-reference/utility-functions), [atualização parcial de record por ID](https://docs.xano.com/xano-features/metadata-api/instance_api/update_a_specific_record_by_id).
