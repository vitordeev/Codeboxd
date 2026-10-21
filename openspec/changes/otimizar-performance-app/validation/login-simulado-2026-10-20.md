# Login até perfil — cenário simulado em 20/10/2026

## Autorização e execução

Usuário autorizou o executor simulado, seus testes e registros após proposta
de confirmar chamadas e comportamento em lentidão/429. Criados somente
`tools/login_performance_scenario.py`, `tests/test_login_performance_scenario.py`
e registros desta change/README. Código do aplicativo não alterado nesta rodada.

O executor cria uma árvore real de estados Reflex, executa `SessionState.login`
e, havendo evento de redirecionamento, `SocialState.visit('profile')` com rota
`/conta`. O redirecionamento é seguido manualmente pelo executor; não há navegador.
Handlers e transporte JSON são reais; todos os clientes HTTP usam MockTransport
e URL sintética imposta no processo. As respostas contêm somente dados fictícios.
Patch temporário é restaurado na saída; não executar em servidor compartilhado.
Nenhuma conta real, rede, servidor ou envio de e-mail foi utilizado.

## Resultados

Cinco amostras por cenário, sempre estado novo/cache vazio, sem páginas extras.
JSON sanitizado com eventos e amostras em
[login-simulado-2026-10-20.json](login-simulado-2026-10-20.json).

| Cenário | Chamadas por execução | Mediana dos handlers | Pior amostra | Resultado |
| --- | --- | --- | --- | --- |
| Sucesso | 6 | 8,681 ms | 10,555 ms | Perfil preenchido |
| Referências com 50 ms de espera cada | 6 | 59,511 ms | 60,414 ms | Perfil aguarda referências |
| Login retorna 429/20 s | 1 | 0,427 ms | 0,524 ms | Erro, sem redirecionar ou repetir POST |
| Segunda validação de sessão retorna 429/20 s | 6 | 8,928 ms | 10,204 ms | Identidade preservada, perfil carregado, erro presente no estado |
| Catálogo retorna 429/20 s | 5 | 8,006 ms | 10,520 ms | Perfil não solicitado, aviso e busy liberado |

Tempos são do processo Python com dados sintéticos e espera injetada, não da
interface. Não incluem navegador, rede, TLS, imagens, renderização ou latência
real do Xano; não definem orçamento de produção. As duas referências lentas
rodam em paralelo; suas esperas não se somam linearmente.

No caso de sucesso a sequência observada é POST `/auth/login`, GET `/auth/me`,
outra GET `/auth/me`, GET `/media` e GET `/profiles` em paralelo, e então
GET `/profiles/{value}`. Um 429 nas referências bloqueia a consulta ao perfil;
isso justifica avaliar separar suas dependências, sem afirmar que é a causa
da quota remota. Erro presente no estado não comprova sua posição visual.

## Verificação

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_login_performance_scenario.py -v
.venv/Scripts/python.exe -B -m tools.login_performance_scenario --samples 5 --delay-ms 50
```

Cinco testes aprovados: sequência de seis chamadas/duas validações e relatório
sem dados sintéticos privados; precedência das referências lentas; POST 429
sem repetição; identidade após falha transitória de sessão; bloqueio do perfil
por 429 no catálogo e liberação de busy. O JSON foi persistido nesta pasta por
execução equivalente do `run_suite`, dentro da autorização documental.
O aviso preexistente de parse de `.env` na primeira linha reapareceu; arquivo
não foi exibido nem alterado.

## Próxima intervenção candidata — depende de aprovação

Separar o detalhe principal do perfil das referências de catálogo/pessoas,
com carregamento e falha por seção, preservando atividade e relacionamentos.
Não remover validações de sessão como parte dessa intervenção. Propor arquivos,
teste de precedência/429, validação visual, rollback e medições antes de editar.

Continuam pendentes linha de base real, cache aquecido, desktop/celular,
identificação da quota e metas aprovadas. Nenhuma tarefa integral da change
foi encerrada apenas por esta simulação. Rollback deste executor consiste em
remover somente seus arquivos e registros, se autorizado, preservando o app.
