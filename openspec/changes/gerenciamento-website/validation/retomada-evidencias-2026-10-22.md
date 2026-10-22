# Retomada: persistência de reports e mensagens

Revisão de evidências já existentes em 22/10/2026. Esta rodada não executou
novas chamadas remotas, publicação ou alterações de contas. Encerra 5.1 e 5.5;
a change passa de 19/34 para **21/34**, com 13 tarefas abertas.

## Critérios conferidos

| Tarefa | Evidência | Resultado e limite |
| --- | --- | --- |
| 5.1 | `reports-api-real-final-2026-10-22.json`, cenários `create_report_*`, `persist_report_*` e `reject_*` | Cinco tipos inseridos e consultados no armazenamento real: post, comment, profile, media e message. Conferidos denunciante, alvo, status pending, descrição, timestamp e snapshot; seis payloads inválidos rejeitados com HTTP 400, sem inserção. |
| 5.5 | Mesmo relatório, `message_context_without_live_message`, mais navegador `browser-componentes-2026-10-22/result.json` e `tools/admin_layout_browser.py` | API real aceita mensagem por snapshot sem mensageria e descarta campo extra. Interface real, com backend fictício, abre o contexto salvo e mostra o texto em 1440/390px. Isso comprova o critério de exibição, mas não a integração autenticada da fila administrativa real. |

O relatório final contém 44 checks aprovados, 12 remoções de fixtures aprovadas
e igualdade antes/depois nas oito tabelas inventariadas. O relatório anterior
`reports-api-real-2026-10-22.json` tem `passed: false` e permanece histórico;
não foi usado para concluir tarefas. A ferramenta correspondente foi lida para
conferir as asserções e os limites dos checks registrados.

O teste real também demonstrou rejeição de visitante (401) e membro (403) nas
oito operações administrativas. Isso é evidência parcial de 2.1/9.1: faltam
operações autorizadas e cenário de conta suspensa. A integridade após criar
reports está comprovada, mas 5.4 segue aberta porque inclui revisar reports.

## Validação desta rodada

- `.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_admin.py`:
  21 testes aprovados, incluindo sanitização/exibição de snapshot de mensagem,
  filtros, autorização simulada e decisão explícita sem ator no payload.
- Não houve compilação nem nova execução de navegador: alterações somente
  documentais; resultados de API e navegador acima são da execução registrada.
- `openspec validate gerenciamento-website --type change`: aprovado.
  Checklist conferido: 21 concluídas e 13 abertas. `git diff --check` aprovado,
  com avisos de conversão LF/CRLF em lockfiles e teste preexistentes.

## Próximo trabalho e bloqueio

Validar 2.1–4.2, 5.2–5.4 e 9.1/9.2 com sessão legítima da conta admin aprovada
(ID 14). Não há variável de sessão administrativa no ambiente nem chave admin
no `.env` conferido; os valores privados não foram exibidos. Credencial de
metadados Xano não substitui autenticação da aplicação. Não promover contas
nem gerar sessão por impersonação. O delta local de paginação do dashboard
continua sem publicação nesta rodada; conferir prévia e autorização antes disso.

Registrar a validação real restante somente após disponibilizar login admin
por meio privado. Preservar contas existentes e usar apenas fixtures próprias
nas operações de suspensão, catálogo e moderação.
