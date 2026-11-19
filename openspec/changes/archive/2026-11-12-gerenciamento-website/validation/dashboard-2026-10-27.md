# Dashboard: totais e paginação — 27/10/2026

Continuação solicitada após commit da busca administrativa. Git inicialmente
limpo; administração 22/34. Escopo: tarefas 2.2, 2.3 e evidências parciais de 9.1.

## Plano antes da implementação

1. Comparar contrato local/remoto com dry-run restrito e salvar backup privado
   somente do GET /admin/dashboard, sem dados/env. Não publicar nesta preparação.
2. Preparar executor de leitura com login admin manual reaproveitando o formulário
   local existente. Comparar contagens do dashboard com metadados independentes,
   validar paginação de atividade e pendências, continuação e vazios. Rejeitar
   segredos no payload e manter somente contadores/booleanos nos relatórios.
   Não substituir login por metadados nem alterar contas, posts ou reports.
3. Validar consultas extraídas do candidato no interpretador Xano, com tabelas
   fictícias e registros sintéticos, incluindo totais conhecidos, pendentes,
   estados vazios e paginação. Preservar resultados de tentativas anteriores.
4. Registrar testes, resultado real e limitações; preparar delta revisável antes
   de eventual publicação autorizada. Não concluir 2.2/2.3 por simulação.

Execução local `.venv`, sem Docker, sem reiniciar/compilar o app por alterações
de instrumentação. Dados retornados por metadados ficam apenas em memória;
senhas, tokens, conteúdo e identidade das contas não entram nas evidências.
Sem retry de escritas ou criação de fixtures no banco real.

## Inspeção e implementação local

Prévia restrita confirmou um UPDATE em admin/dashboard GET. O remoto não possui
recent_posts_pagination nem pending_reports_pagination. Backup privado salvo em
`.local/admin-dashboard-20261027/before-dashboard-GET.xs`; SHA-256
`bd9a1b19fede0ace0e53b4b9bc31cb9fd52e7f60ade02d1a3e6a9131208ec5e6`.

Preparados `tools/admin_dashboard_remote.py` e cinco testes locais. O executor
reutiliza login manual admin ID 14 e verifica visitante 401; obtém totais
independentes das tabelas por metadados, confere estabilidade antes/depois,
campos mínimos e continuação. Metadados nunca fabricam autenticação. Registra
explicitamente se atividade e pendências reais eram não vazias; não usar vazio
como prova de paginação de uma fila preenchida. Interrompe em 429 sem retry.

Em `admin_dashboard_GET.xs`, pendências agora usam created_at DESC, id DESC.
O desempate mantém ordem determinada para reports com o mesmo timestamp.
O teste `tools/admin_dashboard_fixture.py` extrai as consultas/inputs/resposta
do arquivo de produção, troca apenas tabelas por fictícias e usa timestamps
iguais para verificar esse desempate, totais conhecidos, três páginas e vazio.

Validação local inicial: 38 testes administrativos aprovados (33 anteriores
mais cinco novos). Cobrem contagem errada/booleana, endpoint antigo sem páginas,
payload secreto, fila vazia e percurso paginado com inventário independente.
Não houve publicação, execução de mutações administrativas ou reinício do app.

## Resultado sintético e preparo final

[dashboard-fixture-2026-10-27.json](dashboard-fixture-2026-10-27.json): **4/4
cenários e 12/12 verificações aprovados** no interpretador Xano. Totais conhecidos
(três usuários, dois posts, quatro mídias, três reports pendentes), duas páginas
de atividade, três de pendências e banco fictício vazio. Reports com timestamp
igual aparecem por ID decrescente sem omissões/duplicatas. Campos mínimos e
next_page também foram conferidos. Não equivale a validação do banco real.

Adicionado teste que rejeita inventário de reports incompleto, evitando aceitar
uma fila falsamente vazia. Instrumento pronto para validação real após publicação:

```powershell
.venv/Scripts/python.exe -B -m tools.admin_dashboard_remote --output openspec/changes/gerenciamento-website/validation/dashboard-real-2026-10-27.json
```

Publicação a revisar: somente `api/codeboxd/admin_dashboard_GET.xs`. Não incluir
contas, registros, outras rotas ou env. Após autorização, conferir remoto contra
o backup, publicar interativamente, repetir dry-run sem delta e executar o probe
com login admin manual. Se a fila real estiver vazia, registrar a limitação e
manter aberta sua validação com dados reais não vazios. 22/34 mantido.

Rollback: restaurar somente o endpoint anterior do backup privado após dry-run,
sem importar dados. Isso remove metadados novos de paginação e o desempate,
preservando todas as tabelas e registros.

## Preparação das próximas operações de conta

3.2/3.3 permanecem abertas. Validação planejada deverá usar conta membro
descartável identificada por marcador único, criada somente dentro de um
escopo de teste autorizado. Suspender/reativar por sessão admin legítima,
conferir recusa do token suspenso em leitura/escrita protegidas e verificar
event_log com ator autenticado, estado anterior/novo, horário e motivo marcado.
Não suspender contas existentes nem promover a fixture. Preparar journal privado,
inventário anterior e limpeza restrita da conta/perfil/listas e dos eventos
exatos da fixture antes de executar. Não houve mutação ou criação de conta nesta
rodada; esse roteiro não constitui evidência de funcionamento ou autorização
para alterações incidentais de dados.

## Conferência final antes de publicar

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p 'test_admin*.py' -q`:
  **39 testes aprovados**, incluindo seis do novo executor.
- `openspec validate gerenciamento-website --type change`: aprovado.
- `git diff --check`: aprovado.
- Dry-run final com `--include api/codeboxd/admin_dashboard_GET.xs`: exatamente
  **um UPDATE, admin/dashboard GET**, sem tabelas, registros, env ou outras rotas.

O delta remoto entrega metadados de paginação de atividade e pendências,
parâmetros reports_page/reports_per_page e desempate de reports por ID. Parte
da paginação já existia localmente sem publicação; não contabilizá-la como
implementação nova desta rodada. Não altera os quatro indicadores agregados,
autorização, projeção mínima ou dados persistidos.

Comando restrito preparado para confirmação do usuário:

```powershell
xano workspace push -p default -d xano -w 147717 --include api/codeboxd/admin_dashboard_GET.xs
```

Nenhuma tarefa adicional concluída nesta preparação. A tarefa 9.3 impede
publicação automática; aguardar confirmação específica deste endpoint antes
do push. Não confundir o dry-run ou as fixtures com implantação efetiva.
