# Revisão do backend administrativo — 19/10/2026

## Ambiente e comparação

Workspace confirmado pelo usuário: `147717`, Pedro's Workspace, perfil chamado
`default`. O perfil global marcado como padrão aponta para `151345`, por isso
todos os comandos de metadados desta revisão selecionam perfil e workspace.

O esquema foi obtido com `xano workspace pull -p default -w 147717 -d
.local/admin-remote-2026-10-19`, sem `--records` ou `--env`. Foram exportados
77 documentos, preservados localmente em pasta ignorada pelo Git.

O remoto já possui tabela `report`, oito endpoints administrativos e criação de
reports. A informação anterior de que esses endpoints aguardavam publicação estava
desatualizada. O remoto exige papel admin e estado de conta `active` e possui uma
correção de prioridade do filtro `user_id` que faltava no repositório.

## Alterações locais

- Oito endpoints administrativos passam a exigir explicitamente estado `active`,
  preservando a regra já publicada em vez de relaxá-la para qualquer valor
  diferente de `disabled`.
- `GET /admin/users` preserva a precedência do identificador presente no remoto:
  com `user_id > 0`, não mistura outras contas encontradas por texto. Define
  defaults explícitos para consulta vazia e permite busca somente por ID.
- `GET /admin/dashboard` recebeu o bloco `input` ausente localmente e paginação
  independente para atividade e reports. Mantém as duas listas usadas pela UI
  e acrescenta metadados de paginação, sem alterar os campos dos indicadores.

Nenhuma alteração foi publicada nesta rodada. Nenhum usuário foi promovido,
suspenso ou reativado; nenhum conteúdo ou report foi criado ou modificado.

## Verificações realizadas

- `python -B -m unittest discover -s tests -p test_admin.py -q`, via `.venv`:
  18 testes aprovados. São testes locais com serviços simulados.
- Consultas reais via `backend_read_probe.py`: visitante recebeu 401 nas quatro
  rotas de leitura; a primeira conta de membro recebeu 403 nas quatro rotas.
  A segunda conta recebeu 403 em dashboard/usuários e 429 em catálogo/reports.
  Os retornos 429 são limite de requisições e não comprovam autorização.
- [Resultados sem credenciais](backend-read-results-2026-10-19.json).
- O dry-run amplo identificou erro local no dashboard (`Missing block: input`)
  e operações `DROP_FIELD` para três campos de recuperação de senha em `user`:
  `password_reset_attempts`, `password_reset_requested_at`, `password_reset_format`.
  Esses campos estão no esquema remoto e não devem ser removidos nesta entrega.
- Após as correções, o dry-run limitado aos dois endpoints abaixo passou sem
  erros críticos nem operações destrutivas:

```powershell
xano workspace push -p default -w 147717 -d xano --dry-run --include 'api/codeboxd/admin_dashboard_GET.xs' --include 'api/codeboxd/admin_users_GET.xs'
```

Prévia observada: `API Endpoints ~2 updated`; somente `admin/dashboard GET` e
`admin/users GET`. As demais alterações de autenticação, tabelas, feed e perfil
estão excluídas dessa prévia. A cópia remota contém as versões anteriores para
preparação de rollback; não importá-la inteira nem incluir registros.

## O que falta para concluir o passo 3

A consulta posterior, somente leitura, confirmou que a conta indicada pelo usuário
(ID 14) já possui papel `admin` e estado `active`. Nenhuma permissão foi alterada.
Ainda falta viabilizar uma sessão autenticada dessa conta para os testes, sem
colocar senha ou tokens no chat ou documentos. Validar então indicadores contra contagens conhecidas,
paginação/filtros/vazios, rejeição de mutações por membro/visitante, suspensão de
uma conta de teste com sessão existente, auditoria, edição de catálogo preservando
identidade e fluxo de reports/snapshots sem alterar o conteúdo alvo.

A publicação dos dois endpoints é uma ação separada que depende de aprovação
sobre a prévia acima. Dry-run não equivale a publicação nem a validação funcional
autorizada. As tarefas 2.1–5.5 e 9.1 não foram marcadas como concluídas com base
apenas nesta evidência parcial. A interface completa pertence ao próximo passo.
