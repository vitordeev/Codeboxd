# Retomada da administração — 13/10/2026

Trabalho vinculado às tarefas 2.1, 3.1 e preparação de 9.1. A change continua com
17/34 tarefas concluídas. Nenhuma tarefa remota foi encerrada nesta rodada.

## Correções locais

- Os oito contratos `xano/api/codeboxd/admin_*.xs` agora exigem explicitamente
  `$actor.account_status == "active"`, além de ator existente e papel `admin`.
  Antes, um estado diferente de `disabled`, inclusive ausente ou desconhecido,
  satisfazia a condição de estado. Ator continua derivado de `$auth.id`.
- `admin_users_GET.xs` permite busca vazia/omitida para a carga inicial da tela.
  Quando `user_id > 0`, somente esse ID é consultado; busca textual não amplia o
  resultado. Filtros de papel/estado e paginação continuam aplicados.
- Adicionado [admin_read_probe.py](admin_read_probe.py): GET apenas, sem criar
  contas, conceder papéis, suspender usuários ou escrever registros remotos.
  Tokens opcionais ficam em variáveis de ambiente; saída não inclui URL,
  credenciais nem corpo das respostas. Sem tokens, cenários autenticados ficam
  explicitamente não executados. HTTP 404 não conta como acesso negado aprovado.

Referência de autorização: [preconditions no Xano](https://www.xano.com/learn/precondition/).

## Evidências desta execução

| Camada | Verificação | Resultado e limite |
| --- | --- | --- |
| Local/simulada | `.venv\Scripts\python.exe -m unittest discover -s tests -q` | 113 testes passaram; não executam contratos Xano remotamente |
| Local | `python -m py_compile` do probe | Passou; não é teste de autorização |
| Local | `git diff --check -- xano openspec` | Passou |
| Remota, dry-run geral | Push preview do workspace 147717 | 1 tabela nova, 1 tabela alterada, 10 endpoints novos, 2 alterados; inclui mudanças fora desta entrega |
| Remota, dry-run limitado | Includes abaixo, depois das correções | 10 de 78 arquivos: 1 tabela nova e 9 endpoints novos; nenhuma atualização de objeto existente |
| Remota, GET visitante | Quatro rotas administrativas | Todas HTTP 404; endpoints indisponíveis, autorização não comprovada |
| Remota, GET autenticado | Admin, membro e desativado | Não executado: tokens específicos não fornecidos ao probe |
| Navegador | Smoke desktop/celular | Não executado |

A primeira tentativa de GET no sandbox encontrou erro de rede. A execução fora
do sandbox chegou ao Xano e produziu os HTTP 404 registrados em
[admin-read-results-2026-10-13.json](admin-read-results-2026-10-13.json).

## Delta revisado para publicação

```powershell
xano workspace push -d xano -w 147717 --dry-run -i 'table/report.xs' -i 'api/codeboxd/admin_*.xs' -i 'api/codeboxd/reports_POST.xs'
```

Preview aprovado pelo CLI:

- CREATE tabela `report`.
- CREATE GET `/admin/dashboard`, `/admin/users`, `/admin/catalog`, `/admin/reports`.
- CREATE POST `/admin/catalog` e `/reports`.
- CREATE PUT `/admin/catalog/{id}`, `/admin/users/{id}/status`, `/admin/reports/{id}`.

O delta limitado não inclui `/likes`, `media GET`, `profile PUT` ou tabela
`profile`, detectados pelo preview geral. Sem `--records`, `--env`, `--delete`,
`--truncate` ou desativação de transação. Nenhuma publicação foi executada.

Publicação remota submetida à confirmação do usuário após apresentação do delta.
Após autorização: publicar somente os includes revisados, repetir o preview,
validar admin/membro/visitante/desativado e prosseguir com contagens, filtros,
mutação controlada, restauração e auditoria. Nunca marcar 2.1/3.1/9.1 apenas pelo
dry-run ou pela aprovação da suíte simulada.
