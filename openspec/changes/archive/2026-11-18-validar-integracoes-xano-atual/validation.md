# Evidências da reformulação — 17/11/2026

Pedido vigente: continuar os avanços e reformular o que dependia de outro ambiente Xano, indisponível ao usuário. Implementação local coberta por esta change; nenhum ambiente, fixture ou dado remoto criado nesta rodada.

## Entrega

- [Matriz por frente](matriz-validacao.md) define testes locais, leituras/prévias no workspace atual e piloto real limitado. Preserva requisitos de persistência, autorização, privacidade, entrega, concorrência e limpeza.
- `preparar-homologacao-xano-admin` marcada documentalmente como supersedida em proposal/design/spec/tasks; 4/8 preservado, sem marcar as quatro etapas não executadas como concluídas. Suas guardas e ferramentas não foram enfraquecidas.
- Cloudinary, UI e performance tiveram proposal/design/tasks reconciliados. Critérios remotos permanecem abertos, com alternativa no backend existente. Recuperação/e-mail não dependiam de outro workspace: DNS/caixa e decisão sobre restauração continuam independentes dessa mudança.
- `tools/shared_xano_acceptance.py` planeja até dez ações e valida destino canônico, operador, baseline anterior, recibos, identidade/snapshot, propriedade, referências vazias para DELETE, allowlists, digest e prazo. Mudanças de papel/senha, mensagens/reset, exclusão de contas, env/schema e alvos anteriores ao baseline são recusados. Não tem cliente HTTP nem modo de execução live.
- CLI `python -m tools.shared_xano_acceptance --example` executada com dados fictícios: uma ação e duas fixtures, `remote_execution=false`, `approval_checked=false`, `baseline_verified_remotely=false`. Apenas hashes/contagens/prazo em saída. O caso com revisão válida também continua sem execução remota nos testes.

## Verificações

| Comando/verificação | Resultado |
| --- | --- |
| `.venv/Scripts/python.exe -m unittest discover -s tests -p test_shared_xano_acceptance.py -v` | **18 aprovados**, incluindo destino divergente, IDs preexistentes, snapshots alterados, conta protegida, papéis/senhas/rotas proibidas, dependentes existentes, prazo e saída sanitizada |
| `.venv/Scripts/python.exe -m tools.shared_xano_acceptance --example` | Aprovado; nenhuma operação remota, sem credenciais ou dados reais |
| `.venv/Scripts/python.exe -m unittest discover -s tests -q` | **736 testes aprovados**, 86,128 s |
| `openspec validate --all --no-interactive` | **39/39**, dez changes em disco e 29 specs principais |
| `git diff --check` | Aprovado; somente avisos LF/CRLF preexistentes/normalização |

Não houve alteração em componentes Reflex nesta rodada; a compilação de 6,503 s e os 718 testes do lote Cloudinary pertencem à rodada anterior, não são novas medições. Código/configuração preexistentes preservados; sem Docker, publicação, reset, mensagens ou alteração de flags.

## Pendências e contagem

As tarefas 1.1–1.4 desta change estão concluídas; **4/6**. 2.1/2.2 permanecem abertas: lote real ainda precisa backup/inventário independente, recibos de criação aprovados, autenticação do operador/donos e aceite API/navegador/limpeza. JSON coerente não autentica a origem de snapshots nem autoriza execução.

O quadro vigente usa sete changes: **54/109**, 55 abertas. O inventário bruto dos oito checklists funcionais em disco inclui a estratégia isolada supersedida: **58/117**, 59 caixas abertas, quatro delas descontinuadas como pré-requisitos. As duas changes documentais não entram nesses totais. Nenhum cancelamento foi contado como funcionalidade entregue.
