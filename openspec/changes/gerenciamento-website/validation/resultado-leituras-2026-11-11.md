# Aceite administrativo de leitura — 11/11/2026

## Escopo e resultado

Usuário autorizou login de admin existente e validação somente de leitura.
Branch task/admin-readiness-20261111 baseada em develop 29d0456. Resultado bruto
preservado em [browser-leituras-2026-11-11.json](browser-leituras-2026-11-11.json):
passed=true para o escopo limitado de leituras. Não significa aceite completo 9.2.

Login inicial rejeitado 403, tentativa manual posterior 200 e auth/me 200.
Não foram emitidas credenciais no chat ou gravadas no relatório. Nenhum papel
foi concedido ou alterado. Auditoria normal de login pode ser produzida pelo
backend; não é alegado zero efeito de autenticação.

| Verificação automatizada | 1440px | 390px |
| --- | --- | --- |
| Dashboard, Usuários, Filmes, Séries, Livros, Animes, Reports | Aprovada | Aprovada |
| Cinco buscas sem resultados (usuários + quatro catálogos) | Aprovadas | Aprovadas |
| Dashboard mantém totais confirmados após 503 local | Aprovada | Aprovada |
| Reports renderizado e controles disponíveis | Aprovada | Aprovada |
| Ausência de erro JS/overflow segundo assertions do runner | Aprovada | Aprovada |

Quatro checks adicionais de contrato/paginação Reports (primeira/segunda página)
passaram antes da navegação. Não generalizar essa paginação de API ao aceite de
todos os controles de página da interface. As capturas reais permanecem privadas
em `.local/admin-readonly-browser-20261111/admin-{1440,390}.png`. Não foram
publicadas, nem alegada inspeção visual humana das capturas nesta rodada.

## Contagens e limitação corrigida do runner

O JSON bruto da execução tinha defeito de contabilidade: `requests` foi
sobrescrito pelas linhas do proxy, e `request_count=5` ficou restrito ao Probe.
Não alterar silenciosamente esse arquivo histórico e não interpretar 5 como
total remoto. Apuração dos dados vistos durante a execução e do JSON final:

- Bootstrap: cinco chamadas (dois POST de login, um GET auth/me e dois GET Reports).
- Proxy: 50 respostas registradas, das quais dois 503 injetados somente localmente.
- Proxy upstream: 48 GET com resposta 200; zero 429.
- Total remoto observado: **53 chamadas**, dois POST de autenticação + 51 GET.
- Nenhum PUT/PATCH/DELETE ou POST de mutação administrativa.

Correção local posterior separa `proxy_requests` de `requests`, preserva bootstrap
e contabiliza `proxy_upstream_requests` inclusive tentativas sem resposta, mantendo
falhas locais separadas. Três testes de configuração/contabilidade e 12 regressões
de admin_reads_remote passaram após a correção. Não repetido ensaio remoto só para
reescrever o formato da evidência. A suíte completa de 568 e compile seco aprovados
na preparação precedem essa última correção local de relatório.

## Preservação e encerramento do processo

App normal não reiniciado. Servidor de teste e contextos de navegador encerrados
pelo runner após as duas larguras. Build de produção regenerou package.json e
package-lock.json desta worktree; saídas geradas guardadas privadamente e ambos
restaurados byte a byte a partir da worktree Cloudinary limpa nesses arquivos,
com mesmo HEAD 29d0456. bun.lock não mudou. Hashes/reconciliação privados em
`.local/locks-restored-admin-run-20261111.json`. Nenhuma edição na worktree usada
como fonte ou na de performance. Git final sem alterações de lockfiles.

## O que continua aberto

Administração **33/34**, tarefa 9.2 aberta. Não foram testadas neste ensaio
suspensão/reativação, edição/criação de catálogo, decisão de reports, efeitos e
auditoria dessas ações na UI real; tampouco visitantes/membros em cenários
negativos integrados. Falhas são locais ao proxy e não indisponibilidade real.

O plano existente de homologação completa prevê setup/manifesto, identidade
de atores, ciclo de mutações e limpeza/retenção A2–A4. Isso exige revisão e
autorização específica antes de qualquer escrita, inclusive criação de fixtures.
O executor de mutações preparado em 09/11 continua exclusivamente simulado.
Nenhuma autorização de leituras foi ampliada para essas operações. Não marcar
9.2 completa, sincronizar specs, arquivar, fazer push ou merge nesta rodada.
