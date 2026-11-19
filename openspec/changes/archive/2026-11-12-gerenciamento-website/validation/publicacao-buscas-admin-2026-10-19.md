# Publicação das correções de buscas administrativas — 19/10/2026

Escopo autorizado pelo usuário: realizar o item 3 da revisão, publicando e
validando os três GETs corrigidos no checkpoint de 14/10. Tarefas relacionadas:
3.1, 4.1, 5.2 e 9.1–9.2. Pendência transversal P.12.

## Backup, revisão e publicação remota

- `xano workspace pull -d .local/xano-before-admin-search-2026-10-19 -w 147717`
  exportou 77 documentos de estrutura, sem registros nem variáveis de ambiente.
- Os três arquivos remotos foram conferidos contra os locais. O delta remove
  `to_lower` das consultas, explicita metadados/projeção paginada, usa o input
  validado para `per_page` e mantém defaults locais e autorização admin ativo.
- Dry-run limitado confirmou exatamente três atualizações: `admin/catalog GET`,
  `admin/reports GET` e `admin/users GET`. Preview apresentado antes do push.
- O push interativo, confirmado dentro do escopo autorizado, retornou
  **Pushed 3 documents to workspace 147717**. Transação padrão preservada.
- Novo dry-run com os mesmos includes retornou **No changes to push**.
- Não houve importação de registros/variáveis, concessão de papel, alteração de
  contas ou publicação de outros endpoints. Os conflitos Git preexistentes não
  foram resolvidos nem usados como parte da publicação.

```powershell
xano workspace push -d xano -w 147717 --dry-run -i api/codeboxd/admin_users_GET.xs -i api/codeboxd/admin_catalog_GET.xs -i api/codeboxd/admin_reports_GET.xs
```

Para rollback, usar os três contratos do backup, localizados em
`api/codeboxd/admin/{users,catalog,reports}_GET.xs`, com dry-run e revisão antes
de restaurar. Isso restaura o comportamento anterior, inclusive seus defeitos.

## Testes locais e acesso remoto

- `.venv/Scripts/python.exe -m unittest discover -s tests -p test_admin.py -q`:
  **18 testes passaram**. São testes simulados, sem provar as consultas Xano.
- O probe existente foi executado com a primeira conta de teste controlada,
  autenticada e confirmada como membro pelo servidor. Nenhuma conta foi criada.
- Os GETs de usuários, catálogo e reports responderam **401 para visitante** e
  **403 para membro**. O dashboard também teve essa verificação, sem ser publicado.
- [Resultado estruturado](admin-read-after-search-2026-10-19.json): oito checks
  passaram; admin/desativado foram omitidos por falta de tokens. O exit code 1
  significa cobertura incompleta, não falha nos oito checks executados.
- A execução inicial da CLI e do probe no sandbox falhou por restrições locais;
  a repetição com permissão ampliada concluiu backup, publicação e acesso remoto.

## Limitações e retomada

Nenhum token `ADMIN_PROBE_ADMIN_TOKEN` estava configurado. Foi solicitada uma
conta administradora já aprovada ou configuração local do token; nenhum papel
foi concedido automaticamente. Faltam comprovar busca por nome/ID, diferenças
de caixa, vazio, filtros, tipos e paginação como admin, além da interface no
navegador. A publicação está concluída; a validação funcional permanece parcial.
As tarefas 3.1, 4.1, 5.2 e 9.1–9.2 permanecem abertas, com contagem **17/34**.
Não houve nova compilação ou validação de navegador nesta rodada.
