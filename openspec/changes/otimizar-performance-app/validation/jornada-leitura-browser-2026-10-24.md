# Jornada de leitura real no navegador — 24/10/2026

## Plano antes da implementação

Continuação autorizada pelo usuário na change de performance. Priorizar evidência
de interface após pools de catálogo/Xano, sem funcionalidades ou design novos.
Cobertura parcial 1.3/1.4/4.4/5.4/6.4/7.1/7.4/9.1. Não contabilizar leitura como
validação de gravações ou encerrar change por cenário parcial.

Instância isolada de produção em 3031, arquivos/dependências próprios e o mesmo
código atual do produto; app normal 3030 não reiniciado. Proxy loopback para Xano
com allowlist de GETs de leitura e somente POST de login. Bloquear outras ações,
inclusive GET de envio de e-mail; registrar apenas método/endpoint sanitizado,
status/tempo/contagem. Sem cookies no pool do proxy nem credenciais padrão.
Este salto extra e o servidor isolado devem constar como limite da medição.

Login manual de membro no app de teste. Token temporário somente em memória e
armazenamento da janela temporária, descartada ao encerrar. Preflight por GET
confirma membro ativo, listas padrão já existentes sem nomes legados e uma obra
interna existente; assim evita reparo automático esperado. Se houver tentativa
de reparo/escrita, o proxy recusa antes de chegar ao Xano e encerra o cenário.
Não acessar metadados, não criar fixtures, contas ou privilégios.

Até cinco amostras de home → busca → ficha → perfil → biblioteca → listas → feed
→ comunidade em 1440 e 390 px, intervalo 3 s entre ações. Limite 400 chamadas
Xano físicas incluindo login/preflight; interromper na primeira 429, falha,
tentativa bloqueada ou erro de JavaScript. Sem retry de cenário. Não afirmar que
400 chamadas é uma quota do Xano. Comparar mediana/pior das amostras concluídas,
primeiro conteúdo visível e fim do ciclo real de carregamento (WS busy=True →
False). Registrar bytes/frames de WS sem conteúdo, overflow e falhas parciais.

Cache: browser novo por execução; mesma sessão ao longo das revisitas e mudança
de viewport. Não forçar limpeza de caches privados/públicos por endpoints de
debug e não rotular arbitrariamente visita como fria/quente. Medidas não
substituem matriz de cache controlado nem a contagem de provedores Python.
Chamadas Xano são contadas pelo proxy; catálogo Python não é medido por ele.

Arquivos novos: executor de jornada/proxy e testes offline de allowlist,
orçamento, bloqueio de escrita, sanitização e correlação WS; documentação nesta
change e pontos centrais pertinentes. Reusar VisitCycle/Measurement existentes.
Validar salvaguardas antes da rede. Preparar frontend independente, executar
com rede/cache/npm autorizados, limpar apenas processos/servidores próprios.
Rollback: encerrar somente subprocesso de teste; preservar app normal e logs.

Preparação: sete salvaguardas offline aprovadas e `py_compile` aprovado.
Cobrem allowlist, bloqueio antes de encaminhar escrita, 429 sem novas chamadas,
cookies/headers por identidade, preflight de membro/listas/obra, ciclo WS sem
aceitar snapshot antigo e resumo sem fabricar cinco amostras. A jornada aguardará
login manual na instância isolada. Reusar frontend **inativo**
`.local/frontends/feed-lists-15664`; o normal está em `xano-pool-20261024` (PID
10856). Script recusa explicitamente usar o frontend normal atual. Bibliotecas
e frames não são exportados; somente estatísticas sanitizadas.
