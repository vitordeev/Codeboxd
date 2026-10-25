# Conexões HTTP do catálogo — 24/10/2026

## Plano anterior à implementação

Usuário testou o app e relatou pouca diferença perceptível, autorizando continuar
com desempenho e preservação de funcionalidades/design. Priorizar custo de rede
do catálogo público nas tarefas 4.4/9.1/9.3, sem recontar entregas anteriores.
Jornada autenticada anterior parou em `member-preflight`: login 200, metadados
403, zero etapas/mutações. Não escolher outro token ou conceder permissões.

Diagnóstico: `_fetch_response` cria/fecha um AsyncClient para cada chamada,
descartando conexões HTTP. Home dispara múltiplas leituras por provedor;
logs reais mostram ConnectTimeout. Isso não prova que pooling resolverá todos os
timeouts. Links já usam React Router na versão instalada, hipótese de reload
completo por `rx.el.a` descartada sem alterações.

Medir primeiro a home pública com o executor existente, cinco pares frios/quentes,
limite de amostras e interrupção em falha/429 existentes. Sem Xano ou contas.
Comparar depois com pool de conexões ligado no mesmo cenário e preservar dados
brutos, perdas e falhas. Tempos dos handlers não substituem navegador.

Intervenção proposta/autorizada na continuação: um AsyncClient público por loop
do backend durante lifespan, com fechamento garantido no shutdown. Somente
catálogo: não reutilizar cliente de autenticação, dados privados ou uploads.
Headers de autorização permanecem por requisição; bloquear cookies no cliente
compartilhado. Manter timeouts, retries, cache e limites de concorrência.
Fora do lifespan (scripts/testes sem pool), preservar cliente por chamada.

Arquivos: serviço de catálogo, registro de lifespan no app, testes pertinentes,
opção explícita no executor de medição e evidências/design/tasks/README.
Validar reaproveitamento, fechamento, isolamento de loops, cookie/header,
fallback, falhas e cache existentes; suíte e compile isolado. Se o ganho real
não for demonstrado, não afirmar melhora geral nem encerrar 4.4.

Preparar build isolado antes de trocar o servidor normal; só substituir sua
árvore identificada após build válido, iniciando com rede autorizada. Não tocar
outros processos, dados ou design. Conferir catálogo público real depois.
Rollback: retirar lifespan e seleção do cliente compartilhado, preservar todos
os incrementos anteriores e reiniciar somente processo normal da rodada.

Referências consultadas: documentação oficial HTTPX sobre clientes e pooling;
API `App.register_lifespan_task` inspecionada na versão Reflex instalada.

Baseline e execução com pool interromperam após a primeira amostra fria por
conteúdo parcial. Preservar ambos; não completar cinco pares artificialmente.
Para separar custo de conexão de indisponibilidade de outros provedores,
comparar agora cinco pares das mesmas três seleções TMDB, alternando ordem
legado/pool, sem cache de resposta entre modos. Limite de 30 leituras lógicas;
registrar tentativas/status físicos e interromper em falha/429. Novo executor
offline de orquestração `tools/catalog_connections_measurement.py`, sem contas,
usando transporte real; não chamar esses tempos de jornada de navegador/home.

## Resultado da implementação e medições

Pool público por loop implementado em `catalog_connection_pool`, registrado no
lifespan Reflex. Cliente criado somente na inicialização do backend e fechado
ao encerrar; scripts sem lifespan preservam cliente por chamada. Política
descarta cookies recebidos e enviados; token TMDB continua no header individual
da chamada. Xano, autenticação, uploads, timeouts, retries e cache não alterados.

Primeira amostra da home (ambas interrompidas por conteúdo parcial):

| Modo | Primeiro conteúdo | Conclusão | Chamadas | HTTP 200 / falhas de rede | Fileiras com erro |
| --- | --- | --- | --- | --- | --- |
| Antes | 4.172,044 ms | 14.115,896 ms | 22 | 14 / 8 | 6 |
| Pool | 536,362 ms | 8.288,291 ms | 22 | 16 / 6 | 4 |

[Antes](conexoes-home-antes-2026-10-24.json) e
[depois](conexoes-home-depois-2026-10-24.json). Não são cinco pares completos;
falhas externas e amostra única impedem aceitação global ou conclusão de 4.4.

Comparação controlada TMDB, cinco pares com ordem alternada, três seleções por
modo e sem cache de resposta entre modos: **30 chamadas, todas 200**, conteúdo
igual entre modos em cada par. Não houve remoção de chamadas/resultados.

| Modo | Mediana das três consultas | Pior amostra | Chamadas por amostra |
| --- | --- | --- | --- |
| Cliente por consulta | 2.064,146 ms | 2.320,972 ms | 3 em todas as cinco |
| Pool | 886,108 ms | 975,394 ms | 3 em todas as cinco |

Redução de **57,07% na mediana** deste transporte real TMDB, não do aplicativo
inteiro. [Resultado bruto](conexoes-tmdb-comparacao-2026-10-24-tentativa-2.json).
Primeira tentativa do executor tinha colisão de `elapsed_ms` ao combinar métricas
e terminou após três leituras, sem resultado aceito. Artefato vazio preservado;
correção e três testes novos aprovados antes da segunda tentativa. Tempos finais
incluem criação/fechamento do cliente; não esconder esse custo no modo pooled.

Validação local:

- Sete testes de transporte aprovados: reaproveitamento, fechamento, fallback,
  cookies/headers, concorrência, erro não cacheado, cancelamento, escopos de loop
  e rejeição de lifespan duplicado.
- Três testes do comparador aprovados: cinco pares/ordem alternada, interrupção
  sanitizada em falha e orçamento limitado.
- Suíte final **364 testes aprovados**, 26,749 s.
- Compile seco com `.local/compile-catalog-pool-20261024`: **aprovado**, 11,771 s.

Próxima etapa: build isolado de produção, troca do processo normal identificado,
verificação HTTP e das três fileiras reais no navegador. Não encerrar orçamento
global, demais jornadas ou dependência de metadados 403 com este incremento.

## Aplicação na instância normal

- Frontend independente `.local/frontends/catalog-pool-20261024` preparado sem
  tocar o frontend normal anterior. Export de produção sem zip aprovado;
  build reportou 49 s. Log `.local/catalog-pool-build-20261024.log`.
- Conectividade autorizada conferida antes da troca. Launcher anterior
  identificado por PID **3764 e horário de criação exato**, único launcher normal
  desta workspace em 3030. Somente sua árvore foi encerrada; navegador do usuário
  e outros processos não foram selecionados.
- Novo launcher oculto **16476**, `.venv`, produção, single-port 3030, npm,
  frontend `catalog-pool-20261024`. Build do run reportou 37 s; preparação de
  dependências adicional não integra métricas de uso. Logs privados
  `.local/normal-catalog-pool-20261024-stdout.log` e `-stderr.log`.
- HTTP final `/`, `/login` e `/listas`: **200** após redirecionamentos normais.
- Navegador real público: **três fileiras TMDB com 20 cards cada**.
  [Resultado](conexoes-tmdb-browser-2026-10-24.json). Open Library ainda apresentou
  ConnectTimeout: não afirmar disponibilidade plena de todos os provedores.
- Manifest/lock gerados pelo build foram preservados em
  `.local/catalog-pool-generated/`; conferida diferença apenas de formatação e
  prefixos `^`. Restaurado manifest original e mantida ausência preexistente do
  lock. Nenhuma atualização de dependência integra a mudança.

O código novo está aplicado ao servidor normal; não está aguardando reinício.
Estado continua **14/37**: orçamento de todas as jornadas, cinco pares completos
da home, integração autenticada e verificações restantes ainda não concluídos.
`openspec validate otimizar-performance-app --type change` e `git diff --check`
aprovados no fechamento (somente avisos de normalização LF/CRLF em gerados).
