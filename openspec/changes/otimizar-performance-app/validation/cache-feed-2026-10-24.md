# Reutilização de leituras do feed — 24/10/2026

## Plano antes da implementação

Continuação autorizada pelo usuário: melhorar desempenho sem alterar funcionalidades
ou design. Incremento das tarefas 7.1/7.2/7.3; critérios globais continuam abertos.
Git inicialmente limpo. `_refresh_posts` repete GET `/feed`, `/posts` e `/likes`
em revisitas; `/media` e `/profiles` já reutilizam cache privado por 15 segundos.

Incluir somente essas três leituras no mecanismo existente, sem ampliar TTL,
limites, paginação ou retries. Chave mantém token, parâmetros, dados e paginação;
compartilhamento em andamento mantém nonce de sessão e geração. Erros, inclusive
404 de `/likes`, não serão armazenados. Escritas via `_call` já invalidam antes
e depois; upload de post usa transporte separado e precisa da mesma invalidação,
inclusive em falha cuja persistência seja incerta. Nenhuma mudança visual, de
endpoint, de autorização ou de dados remotos.

Risco: publicações de outras contas podem levar até 15 segundos para aparecer em
revisitas, dentro da janela de cache de navegação; ações locais invalidam o cache.
Verificar sobretudo post com imagem, curtida, comentário e seguir/deixar de seguir.
Rollback: retirar as três rotas da seleção de cache e o wrapper de invalidação
do upload, preservando demais alterações e dados.

Arquivos: `Codeboxd_main/state/social.py`, regressões em
`tests/test_feed_navigation_performance.py`, executor comparativo
`tools/feed_navigation_measurement.py` e evidências/checklist desta change.
Validar cinco amostras de revisita com latência HTTP fictícia; registrar chamadas,
mediana/pior e igualdade dos posts, sem atribuir tempos simulados à API real.
Cobrir expiração, parâmetros, credenciais, sessão, falha/404, gravações e upload.
Executar suíte local, compilação seca e validação OpenSpec. Sem reiniciar servidor
normal nem executar mutações remotas neste incremento.

## Resultado e limites

Executor reproduzível, executado antes e depois da alteração:

```powershell
.venv/Scripts/python.exe tools/feed_navigation_measurement.py --output <arquivo-novo.json>
```

Cada amostra aquece uma visita e mede cinco revisitas completas de `load_feed`,
incluindo referências e composição dos cards. Cinco amostras por cenário,
latência HTTP fictícia de 10 ms; autenticação substituída por aprovação local
fictícia, pois esta medição isola as leituras do feed, não o login.

| Cenário | Chamadas por cinco revisitas antes/depois | Mediana antes/depois | Pior antes/depois |
| --- | --- | --- | --- |
| `/likes` disponível | 15 / 0 em todas as amostras | 251,192 / 9,298 ms | 303,490 / 17,117 ms |
| `/likes` ausente (404) | 15 / 5 em todas as amostras | 235,410 / 91,693 ms | 263,601 / 125,636 ms |

Os cinco pedidos restantes são tentativas de GET `/likes`: erros não entram no
cache. O fallback existente continua consultando a discussão sob demanda;
nenhuma rota remota foi presumida disponível ou publicada. Os valores de tempo
são sintéticos e não representam latência real, browser ou meta de aceitação.
Primeira visita conserva suas cinco leituras; o ganho é de revisita dentro do TTL.

Artefatos brutos: [antes](cache-feed-antes-2026-10-24.json) e
[depois](cache-feed-depois-2026-10-24.json). Comparação de igualdade dos cards
aprovada em todas as amostras.

Sete regressões novas cobrem conteúdo/ordem/imagem/contagens/curtidas, cópias,
expiração, páginas/autorias distintas, token e sessão, erros não cacheados,
invalidação por criação/edição/exclusão/curtida/comentário/conexão (inclusive
falha), leitura iniciada antes da gravação e upload com sucesso/falha.
Upload invalida antes e depois; falha conserva imagem e rascunho e não repete envio.

Validação local:

- `.venv/Scripts/python.exe -m unittest discover -s tests -q`: **340 testes
  aprovados**, 28,672 s, incluindo sete novos. Avisos dos cenários de falha são
  esperados; testes antigos que substituem `time.monotonic` geram avisos de
  duração artificial do asyncio, sem equivaler a latência real.
- `.venv/Scripts/python.exe -m reflex compile --dry`: **aprovado**, 11,041 s.
- Reexecução dos sete testes novos após remover substituição global do relógio
  no teste de expiração: **aprovada**, 0,809 s, sem os avisos artificiais novos.
- `openspec validate otimizar-performance-app --type change`: **aprovado**.
- `git diff --check`: **aprovado**; diff de implementação conferido.
- Componentes de páginas, CSS e contratos Xano não foram alterados.

Sem navegador nesta rodada, chamadas/mutações remotas ou reinício do servidor
normal. O código precisa de reinício do processo de produção para ser utilizado
na instância que já estiver em execução. Tarefas 7.1–7.4 e 9.1 continuam abertas:
este incremento não cobre medição social completa, aprovação de metas nem jornada
autenticada. Estado continua **14/37**; não confundir avanço parcial com aceitação
integral. Comparações reais ainda exigem login e validação por camada.
