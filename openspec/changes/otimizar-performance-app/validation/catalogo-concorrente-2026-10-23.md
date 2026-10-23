# Catálogo público concorrente — 23/10/2026

## Escopo e autorização

Usuário solicitou executar a otimização de performance após definir prioridade
para apresentação de segunda-feira, mantendo documentação OpenSpec. Esta rodada
implementa localmente a deduplicação de leituras públicas concorrentes, dentro
dos requisitos request-lifecycle e das tarefas 4.1/4.2. A autorização atual
cobre código, regressões e evidência; não inclui publicação remota.

## Diagnóstico e plano anterior à implementação

`services/catalog.py:fetch` consulta o cache de 300 segundos, mas armazena somente
após receber a resposta. Duas consultas equivalentes durante cache vazio criam
dois clientes e duas chamadas HTTP. A home e buscas compartilham esse transporte.

Intervenção: compartilhar somente `cache=True` por event loop e hash de URL,
parâmetros e headers; devolver cópias independentes. Preservar TTL, limite de
128 respostas, retries e tratamento de erros. Limitar também o registro de
consultas pendentes a 128; excedentes continuam pelo transporte normal.
Cancelamento de um consumidor não cancela os demais. Remover tarefas terminadas
e consumir exceções mesmo quando todos os consumidores abandonarem a consulta.

Arquivos: `Codeboxd_main/services/catalog.py`, testes de performance da home,
este registro e tasks.md. Risco: tarefa compartilhada sobreviver ao consumidor;
limitado pelo timeout/retries existentes e limpeza ao terminar. Rollback:
remover somente o wrapper de compartilhamento e suas regressões.

Validação prevista: cinco repetições de concorrência com HTTP fictício,
isolamento por parâmetros/credenciais, cópias, falha/retry, cancelamento,
chamadas sem cache e limite de pendências; suíte local e compile --dry.
Não equivale a baseline de provedores reais, browser ou metas globais.

## Resultados

Validação local concluída:

- `.venv/Scripts/python.exe -m unittest discover -s tests`: **311 testes
  aprovados**, incluindo cinco regressões novas (oito testes no arquivo dirigido).
- `.venv/Scripts/python.exe -m reflex compile --dry`: aprovado, 3,162 segundos
  informados pelo compilador. Não representa tempo de navegação.
- `openspec validate otimizar-performance-app --type change`: aprovado.
- `git diff --check`: aprovado; somente avisos de conversão LF/CRLF.
- Cinco amostras com dez consumidores simultâneos, cache vazio e HTTP fictício:
  transporte anterior `[10, 10, 10, 10, 10]` chamadas; wrapper novo
  `[1, 1, 1, 1, 1]`. Mediana/pior: 10/10 antes, 1/1 depois; redução de 90%
  exclusivamente nesse cenário de concorrência. Cada amostra conferiu cópias
  independentes e registro pendente vazio após conclusão.
- Testes adicionais: consultas/páginas/credenciais separadas; chamadas sem cache
  independentes; cancelamento de um consumidor; falha compartilhada removida e
  nova tentativa efetiva; 130 consultas distintas concluídas com no máximo 128
  entradas pendentes. Regressões existentes cobrem expiração e erros não cacheados.

Somente transporte público optante por `cache=True` (TMDB/Open Library) foi
alterado. Kitsu conserva seu cache e transporte atuais. Nenhum estado ou API
Reflex foi modificado; as três skills exigidas foram verificadas e lidas no
diretório `C:/Users/victo/.codex/skills/`. Ambiente `.venv` existente confirmado
com Reflex 0.9.11.post1. Tentativa inicial de instalação foi interrompida após
localizar as skills já instaladas; nenhum arquivo de instalação aparece no diff.

Sem chamadas reais a provedores, navegador, publicação, reinício do servidor ou
novas contas. Portanto 4.1/4.2 e as demais etapas amplas permanecem abertas:
faltam baseline real, custo por provedor, metas e comparação de desktop/celular.
O resultado não comprova redução de 90% no tempo global do aplicativo nem
eliminação dos 429. Contagem integral mantida em **11/37**.
