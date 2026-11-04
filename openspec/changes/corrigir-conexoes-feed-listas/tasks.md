## 1. Diagnóstico e contrato

Encerramento desta rodada a pedido do usuário, em 03/11/2026, para preparar
o Git: **9/10**. Backend publicado/migrado e limpeza final comprovados; aceite
visual de 3.2 permanece aberto. Ver
[entrega, validações e limites](validation/encerramento-2026-11-03.md).
Sem arquivamento, sincronização de specs ou commit nesta rodada.

- [x] 1.1 Registrar causas confirmadas, hipóteses e mapa completo das chamadas em investigation.md antes de editar Python.
- [x] 1.2 Entregar xano-changes.md com tabelas, índices, migração, stacks ordenados e contratos verificáveis para aplicação manual.

## 2. Python

- [x] 2.1 Corrigir follow com normalização, confirmação e erro; testar respostas válidas, inválidas e sessão alterada com mocks.
- [x] 2.2 Corrigir carga e vazio/erro do feed; testar leitor sem posts e falhas parciais com mocks.
- [x] 2.3 Implementar switch com status confirmado e controles sincronizados; testar alternância, remoção, erro e resposta obsoleta com mocks.

## 3. Validação

- [x] 3.1 Executar testes existentes e novos, compile seco e openspec validate; registrar comandos, resultados e limitações em validation.md.
- [ ] 3.2 Aplicar os passos Xano e validar as três jornadas reais, incluindo usuário novo, concorrência e limpeza. Execução pelo agente autorizada em 03/11/2026, substituindo a dependência manual anterior; manter aberto até aceite comprovado.

## 4. Continuação autorizada em 03/11/2026

Pedido posterior de finalizar autoriza o ensaio na instância atual com contas
descartáveis e rotas temporárias. Isolamento por IDs/prefixo, sem alegação de
banco separado; método e salvaguardas no design. A publicação final continua
dependente de ensaio/rollback e conferência do escopo e do snapshot.

- [x] 4.1 Implementar contratos Xano de follow, status único e todas as projeções/escritas de listas padrão; verificar prévia remota restrita e regressões locais de preservação de avaliação/privacidade.
- [x] 4.2 Preparar backup, planejamento de migração, bloqueio de escritas, journal e rollback restritos; verificar ensaio isolado e rejeição de drift antes de publicar.
- [x] 4.3 Publicar os contratos e migrar somente dados cobertos pelo plano revisado, verificando índices, nenhuma alteração em personalizadas/avaliações e nenhum documento remoto alheio modificado.

Continuação de finalização: ensaio real aprovado em `validation/rehearsal-2026-11-03.json`,
incluindo restauração de fixture com mesmo ID/campos. Corte aprovado em
`validation/cutover-2026-11-03.json`: 6 itens para 5 statuses, 1 conflito;
preservação integral de dados e contratos alheios verificada. Bloqueios
removidos e nenhuma rota temporária restante no export final. **9/10**;
3.2 aguarda aceite nos endpoints definitivos e navegador, com limpeza final.

As contagens históricas 6/7 são preservadas como estado anterior. O checklist
atual passa a 6/10; tarefas novas detalham a execução remota autorizada. Evidências
desta continuação em `validation/implantacao-2026-11-03.md` e resumos sanitizados.

Resultado desta continuação: **7/10**. Contratos locais e prévia exata dos
15 documentos aprovados; 477 testes OK. Backup/plano/pacote de rollback
preparados, mas sem ensaio real/restauração. Branch (500) e fonte isolada (403)
recusadas pelo plano gratuito. Solicitada escolha de outro workspace ou ensaio
com contas descartáveis/rotas temporárias na instância atual. Sem publicação;
3.2/4.2/4.3 permanecem abertas até os critérios reais correspondentes.

## Evidências

03/11/2026: sondagem remota somente de leitura sem login: catálogo 200, feed
401, novo GET `/media-list-status/1` 404, controle inexistente 404. Não comprova
publicação/migração nem etapas parciais; 3.2 segue aberta. Resultados e limites
em [validation.md](validation.md#verificação-remota-somente-de-leitura--03112026).

Diagnóstico prévio em [investigation.md](investigation.md), contrato manual em
[xano-changes.md](xano-changes.md). Testes locais:
`.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_follow_feed_list_status.py -v`
→ 22 testes aprovados; cobrem tarefas 2.1–2.3. Compile seco e validação OpenSpec
aprovados nesta rodada; suíte completa 451 OK e regressão final de social (38),
conteúdo obrigatório (6) e ficha progressiva (8) aprovadas. Ver [validation.md](validation.md). Não equivalem a aceite
remoto. Tarefa 3.2 permanece aberta até aplicação e validação pelo usuário.
