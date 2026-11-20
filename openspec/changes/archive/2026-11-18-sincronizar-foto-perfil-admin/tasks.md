## 1. Atualizar identidade administrativa

- [x] 1.1 Buscar `/admin/me` novamente sempre que o menu de identidade for aberto.
- [x] 1.2 Cobrir com teste a foto alterada entre aberturas e preservar verificacao de sessao/fallback.

## 2. Validar e registrar

- [x] 2.1 Executar teste direcionado, `reflex compile --dry`, `git diff --check` e `openspec validate sincronizar-foto-perfil-admin --type change`.
- [x] 2.2 Registrar que o teste confirma a atualizacao local; leitura Xano real e confirmacao visual ainda dependem de abrir o painel com a conta no ambiente conectado.

## Evidencias locais (2026-11-18)

- Reabrir o menu dispara nova leitura autenticada de `/admin/me`; o teste simula perfil sem foto na primeira abertura e foto nova na seguinte.
- Teste direcionado passou; `reflex compile --dry`, `openspec validate sincronizar-foto-perfil-admin --type change` e `git diff --check` passaram.
- A leitura ao Xano conectado e a confirmacao visual na conta real nao foram executadas nesta sessao.
- A suite mais ampla `tests.test_admin` ainda tem uma falha preexistente fora desta tarefa: expectativa de `per_page=25` para livros, enquanto o codigo atual envia `35`.
