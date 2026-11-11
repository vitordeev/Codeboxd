# Resolução dos conflitos da PR #33 — 11/11/2026

## Escopo e decisão

O usuário informou o conflito e identificou a PR #33. A consulta à API do GitHub
confirmou destino `main` em `42ff4dd364039f9e6f8f066c1a87651547ad152b`, origem
`wip/performance-preservada-20261111` em
`f19e02e52dcfd3014d5a1a0a4ba7906665392a7b`, aberta e com conflito.

Incorporar essa main à branch WIP por merge normal, sem rebase ou force push.
Resolver somente os conflitos de README, PENDENCIAS e tasks de performance:
preservar os registros novos da main e as evidências locais de 09/11. Não
selecionar um lado inteiro nem remover histórico. Nenhum ajuste funcional novo.

O registro de 10/11 que dizia P0 fora da branch descreve aquela integração.
Nesta PR o checkpoint P0 está incluído como WIP para continuação; não representa
aceite das metas móveis, autorização de deploy ou conclusão de performance.
Os 37 critérios funcionais mantêm os mesmos estados (17 concluídos, 20 abertos).
A tarefa adicional em tasks registra somente a integração documental desta PR.

As worktrees originais e branches main/develop não são modificadas por esta
resolução. Nenhum teste remoto, envio de e-mail ou mutação de dados faz parte
da validação. Não efetuar merge da PR nem arquivar a change.

## Validação

- `python -m unittest discover -s tests`: 621 testes aprovados em 28,510 s.
- `openspec validate --all`: 32 itens aprovados, nenhum erro; avisos históricos
  de requisitos longos permanecem.
- `git diff --cached --check`: aprovado; nenhum arquivo não resolvido.
- Verificação de segredos: 237 arquivos preparados inspecionados, sem achados,
  incluindo comparação com credenciais privadas configuradas, sem copiá-las.
- Revisão: os três documentos preservam as adições dos dois lados; os arquivos
  de código da Home e package.json são idênticos ao checkpoint anterior da WIP.
- Sem execução remota do aplicativo, teste de navegador ou aceite de performance.
