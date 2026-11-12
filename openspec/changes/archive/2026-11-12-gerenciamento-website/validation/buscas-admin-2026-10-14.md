# Correção das buscas administrativas — 14/10/2026

Tarefas relacionadas: 3.1, 4.1, 5.2 e 9.1–9.2. Em resposta ao relato, o usuário
esclareceu que os erros são no painel administrativo. A verificação pública
anterior não cobre esse problema.

## Causa confirmada em logs reais

Leitura de `request_history` pela Metadata API, com `include_output=true`:

- `/admin/users`: HTTP 400, `Invalid filter: to_lower`, parâmetro `search`.
- `/admin/catalog`: HTTP 400, mesmo erro de filtro.
- `/admin/reports`: HTTP 500, `Unable to locate var: reports.items`.
- `/admin/dashboard`: chamadas recentes com HTTP 200.

Os logs completos contêm cabeçalhos privados e permanecem ignorados em `.local/`.
Nenhuma senha, token ou informação pessoal foi copiada para esta evidência.

## Alterações salvas localmente

Arquivos: `xano/api/codeboxd/admin_users_GET.xs`, `admin_catalog_GET.xs` e
`admin_reports_GET.xs`.

- Removido `to_lower` das expressões de consulta. Mantido o operador nativo
  de busca parcial `~`, os filtros de tipo/status/papel e a consulta por ID.
- Configurado `metadata: true` explicitamente nas três consultas paginadas.
- Projeção inclui metadados de paginação e campos sob `items.*`, seguindo o
  envelope paginado; senhas, tokens e e-mails continuam fora da consulta de usuários.
- `per_page` da resposta vem do input validado, sem depender de campo opcional
  do retorno da consulta.
- Verificação de ator ativo/admin e GUIDs preservados.

Referência oficial: [Database Operations](https://docs.xano.com/xanoscript/function-reference/database-operations),
seção Paging e exemplo de projeção com `items.*`. Os filtros de texto genéricos
não garantem suporte em expressões de consulta nesta instância; a causa acima
foi confirmada pelo erro real, não inferida apenas da documentação.

## Validação e encerramento para commit

`python -m unittest discover -s tests -p test_admin.py -q`: **18 testes passaram**,
na `.venv`. São testes locais simulados; não comprovam execução Xano desta correção.

Backup estrutural solicitado via CLI falhou com `Failed to fetch multidoc:
fetch failed`. O dry-run limitado depois passou: exatamente três atualizações,
`admin/catalog GET`, `admin/reports GET` e `admin/users GET`; nenhum outro objeto.
Nenhuma publicação remota foi executada nesta rodada. As alterações
estão salvas para o commit do usuário, conforme pedido de encerrar a sessão.
As tarefas permanecem abertas; contagem da change continua **17/34**.

Na retomada: concluir backup e dry-run limitado aos três arquivos, revisar delta,
publicar a correção dentro do escopo autorizado e validar busca por nome/ID,
diferenças de caixa, resultados vazios, tipos, filtros e paginação com conta admin
aprovada. Repetir rejeição de visitante/membro. Não conceder papel admin automaticamente.
