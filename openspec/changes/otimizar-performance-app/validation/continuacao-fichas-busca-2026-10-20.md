# Continuação: fichas, busca e respostas tardias — 20/10/2026

## Pedido e escopo

Usuário pediu concluir o restante da change. A autorização cobre o avanço local,
testes, ferramentas de browser com fixtures e reinício da instância normal.
Preservadas todas as alterações e evidências das rodadas anteriores.

Foi solicitado ao usuário indicar contas exclusivas/aprovadas de membro e
administrador, sem enviar senhas na conversa, e avaliar metas propostas. Até
este registro não houve resposta. Nenhuma conta real foi utilizada ou criada;
nenhum privilégio concedido e nenhum e-mail real enviado. Metas propostas não
foram incorporadas como critérios aprovados. A solicitação ampla de concluir
não comprova credenciais, quota, baseline nem aprovação de números específicos.

## Implementação e diagnóstico

| Tarefa | Resultado desta rodada |
| --- | --- |
| 2.2 | Regressões locais de login válido/inválido, sessão persistida/expirada, logout, conta desativada e falhas transitórias aprovadas com os testes de autenticação/sessão existentes e ampliados. Mutações mantêm validação fresca e autorização no endpoint. Não equivale a validação de contas reais ou ao fluxo de e-mail. |
| 3.4 | Guardas de rota, visita, token e identidade da obra impedem respostas tardias de reescrever fichas, avaliação, referências, feed e seleção de listas. Perfil distingue gerações de carga. Preparação de listas interrompe sequência de mutações ao trocar rota/conta. Erro 401 tardio de outro token vira conflito local, sem invalidar sessão nova. Geração da avaliação impede leitura iniciada antes/durante gravação de restaurar a nota antiga. Cache mantém invalidação antes/depois de mutações, inclusive falhas. |
| 4.3 | Busca TMDB e Open Library agora reutiliza o cache público existente de 300 s/128 entradas; Kitsu já tinha cache. Chave conserva consulta, página, tipo/endpoint e credencial. Teste HTTP simulado confirmou duas buscas idênticas com uma chamada; outra página e outro termo fazem chamadas distintas. Busca e continuação descartam resposta após sair da rota. Relevância e deduplicação dos quatro tipos continuam verificadas pela suíte. |
| 5.1 | Conferidas fichas internas por ID e externas por fonte/tipo/ID: detalhe/identidade são principais; trailers, streaming, recomendações, críticas, avaliação pessoal e listas são complementares. O detalhe externo continua usando catalog.detail, preservando tradução e mapeamento Jikan/Kitsu; não altera identidade externa nem move avaliações antigas. Intervenção apresentada na commentary e executada no escopo solicitado. |
| 5.2 | visit(media/external) publica título/capa/descrição antes dos complementos, com carregamento e erro visíveis. Editor pessoal aguarda restauração da avaliação para não substituir nota persistida por formulário vazio durante a carga. Complementos têm cópia da obra e guardas de identidade; falha opcional preserva ficha principal. Casos internos/externos dos quatro tipos e Jikan legado verificados localmente. |

Arquivos: state/social.py, pages/social.py, services/catalog.py; novos testes
test_media_progressive.py, test_search_lifecycle.py e test_stale_social_reads.py;
nova ferramenta tools/performance_continuation_browser.py. A ferramenta aceita
--output e se recusa a sobrescrever um result.json existente.

## Avaliações e atalhos — incremento sem encerrar 5.3/6.3

Salvamento captura a identidade da ficha antes de autenticar/persistir. Troca de
conta/obra durante autenticação impede envio; confirmação antiga não fecha nem
substitui o rascunho de outra obra. _persist_selected confere identidade depois
de awaits; quick_add interrompe passos subsequentes ao trocar a ficha.

O teste de confirmação tardia verifica o payload enviado para a obra original e
o rascunho preservado na nova. Os testes existentes preservam notas decimais,
envio único, edição explícita, falha/retry e cache invalidado. **5.3 continua
aberta:** falta confirmação real de persistência; **6.3 continua aberta:** falta
concluir otimização e validar todas as mutações de listas/atalhos.

## Evidência executada

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests -q
.venv/Scripts/python.exe -m reflex compile --dry
.venv/Scripts/python.exe -B -m tools.performance_continuation_browser
.venv/Scripts/python.exe -B -m tools.performance_continuation_browser --output openspec/changes/otimizar-performance-app/validation/continuacao-browser-final-2026-10-20
```

**259 testes aprovados; compilação Reflex aprovada.** Quinze novos testes nesta
rodada, além dos 244 anteriores. Há casos parametrizados: 4 tipos, resultados e
erros de complementos tardios, troca de conta, falha/invalidação de gravação,
seleção de lista e referências/feed que respondem depois de sair da rota.
Avisos asyncio ligados ao relógio mockado não são medidas reais de latência.

Primeira execução: [12 casos de browser aprovados](continuacao-browser-2026-10-20/result.json),
1440/390px, Edge headless, servidor Reflex em produção e serviços fictícios.
Oito fichas dos quatro tipos exibiram conteúdo principal em 265–392 ms enquanto
a avaliação artificialmente atrasada por 3 s ainda carregava. Quatro casos de
cadastro/recuperação com 429 preservaram o e-mail; pedido repetido no cooldown
não enviou segunda chamada. Sem erros JavaScript ou overflow. Uma amostra por
caso: **não é benchmark de produção nem cumpre as cinco amostras da tarefa 1.3**.

A [repetição final](continuacao-browser-final-2026-10-20/result.json) aprovou os
12/12 casos com o código final, sem erros JavaScript ou overflow. As oito fichas
registraram 449–2.205 ms até o título, uma amostra por caso. A variação entre
execuções reforça que isto não estabelece baseline ou cumprimento de metas.
Ambos os relatórios têm failure vazio e normal_restored=true. O servidor normal
foi restaurado em 3030 com a configuração privada habitual, sem overrides de
fixtures; smoke com redirects seguidos retornou HTTP 200 em login/conta/biblioteca.
A compilação não é contada como validação de browser nem remota.

No log da repetição houve erro de sessão alterada em tarefa protegida após
troca de contexto e tentativas opcionais de catálogo que terminaram em
ConnectError. Esses eventos de backend não são erros JavaScript, não fornecem
validação de provedor real e não entram como sucesso remoto. O browser bloqueia
tráfego externo, mas esta versão da ferramenta não intercepta globalmente toda
tentativa HTTP opcional do backend. Não caracterizar a execução como garantia
de zero tentativas externas.

Durante um smoke HTTP local, rotas estáticas retornaram 307 antes de seguir
redirect; /obra/1 retornou 404 no servidor de arquivos, embora a ficha funcione
no browser com roteamento cliente. O status HTTP de entrada dinâmica não está
resolvido por estes testes de interface e fica registrado como limitação.

## Pendências e dependências para encerrar o restante

| Grupo | O que ainda falta |
| --- | --- |
| 1.2–1.5 | Completar aprovação de cenário/dados reais, baseline de todas as jornadas com cinco amostras, diagnosticar escopo da quota e obter metas numéricas explícitas. Ferramentas/servidor/fixtures desta rodada foram autorizados e executados; isso não aprova automaticamente números ou contas. |
| 2.3/2.4, 3.5 | Cadastro/recuperação reais com caixa controlada, comparação contra metas e reprodução do uso habitual com a conta adequada. Browser com fixtures não encerra esses critérios. |
| 4.1/4.2/4.4, 5.3/5.4 | Diagnósticos/comparações restantes de home e fichas com provedores reais, cache vazio/aquecido e metas; persistência real de avaliação. |
| 6.2–6.4 | Continuação real acima de 20 itens, duas contas para isolamento, coleções grandes, listas públicas/privadas e otimização/validação de mutações. Conta histórica tinha quatro itens. |
| 7.1–7.4 | Diagnosticar e concluir intervenções sociais (outro perfil, comunidade, feed, posts/upload/likes/comentários) com baseline e dados de teste aprovados; comparar contra metas. |
| 8.1–8.4 | Conta admin ativa aprovada e outra desativada para rejeição; validar contagens/paginação/mutações/auditoria reais e interface. Não conceder admin para viabilizar teste. |
| 9.1–9.3 | Jornada integral com metas aprovadas, redução/429 no uso habitual, relatório final completo. Depende das etapas anteriores; não encerrar por simulação parcial. |

Permanecem 26 tarefas abertas; esta rodada encerra cinco tarefas locais e leva
a change a 11/37. Nenhuma tarefa de medição/integração real foi encerrada sem
evidência. Há implementação adicional pendente, além das validações remotas.

Rollback: reverter apenas os trechos desta rodada nos três arquivos de produto,
remover seus três testes e a ferramenta/evidências novas; reabrir os cinco IDs
e reconciliar os documentos centrais. Preservar a rodada de cache/concorrência
anterior, dados privados e evidências históricas; não há migração remota.
