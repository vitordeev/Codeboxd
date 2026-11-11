# Pausa da análise de performance — 09/11/2026

Pausa solicitada explicitamente pelo usuário para sair e retomar mais tarde.
Executor, navegador temporário e servidor isolado encerrados; porta 3032 sem
listener ao salvar. Nenhuma otimização, operação administrativa, mutação de
conteúdo, commit, push, merge ou exclusão realizada. Tokens não foram salvos.

## Onde continuar

Diretório: **D:\Repositorios GIT\Codeboxd-performance-20261109**.
Branch: **task/performance-20261109**, base a21c806. Change
**otimizar-performance-app: 17/37**, vinte tarefas abertas. Administração 33/34
permanece aguardando homologação, que não foi iniciada. Não executar novos
processos até o usuário pedir retomada.

O diretório original D:\Repositorios GIT\Codeboxd e seus arquivos locais foram
preservados integralmente, incluindo reflex.lock/package.json. O lock da worktree
também foi restaurado aos bytes anteriores à compilação pelo finally do executor.
Runtime utilizado somente para medição: .venv do diretório original, Python
3.13.1, Reflex 0.9.11.post1, httpx 0.28.1, Playwright 1.64.0. Nenhuma dependência
foi atualizada. Código/cwd da worktree; frontend privado e recompilado em
produção, sem Docker. Configuração passada em memória, sem criar/copiar .env.

## Evidências salvas

[Dados sanitizados completos](medicoes-parciais-2026-11-09.json): **28 amostras**,
sendo vinte Home (cinco pares por viewport) e oito leituras desktop da conta
comum (um par por biblioteca/listas/perfil/feed). As duas amostras frias com
seção indisponível estão incluídas nas medianas abaixo, não ocultadas.

| Viewport | Cache | Tentativas | Destaque, mediana / pior (s) | Fim do ciclo, mediana / pior (s) | Casos com seção indisponível |
| --- | --- | ---: | ---: | ---: | ---: |
| 1440 | cold | 5 | 1.322 / 2.090 | 11.846 / 12.989 | 1 |
| 1440 | warm | 5 | 0.380 / 0.599 | 0.864 / 2.520 | 0 |
| 390 | cold | 5 | 1.356 / 1.765 | 7.002 / 13.541 | 1 |
| 390 | warm | 5 | 0.401 / 0.665 | 0.786 / 4.706 | 0 |

São cinco pares tentados em cada largura, **quatro pares com conteúdo completo
em cada uma**. Kitsu teve dois erros de rede de cerca de oito segundos; as
revisitas recuperaram as seções. Não declarar cinco pares integralmente aprovados.
Nenhum erro JavaScript nos registros Home. HTTP 200 sozinho não foi usado como
prova: ciclo busy iniciado/finalizado e destaque no DOM foram observados.

Cada Home fria fez 23 chamadas Python: dez TMDB, três Kitsu, nove Open Library
e uma Xano pelo proxy. Nas revisitas normais completas, zero aos provedores e
uma Xano; revisitas após falha fizeram consultas adicionais para recuperação.
Não somar a observação do proxy local e seu encaminhamento como duas chamadas
físicas ao Xano. Recursos de navegador incluem cache; tamanhos de imagens
cross-origin via ResourceTiming são incompletos. Payload WebSocket é UTF-8
decodificado, não tráfego TLS medido.

Comparação histórica: em 04/11, a Home Python/provedores (sem Xano/browser)
tinha mediana fria de 0,252 s para destaque e 3,457 s para conclusão; aquecida
0,101/0,118 s, em cinco pares completos. Nova tentativa nessa mesma camada em
09/11 completou dois pares (frio 4,224 e 9,790 s; aquecido 0,028 e 0,026 s),
depois parou com seção ausente em 12,855 s. Não equivale a comparação A/B de
duas implementações nem permite atribuir diferença a uma mudança de código.

Leituras desktop descritivas, fim do ciclo primeiro/repetido: biblioteca
1,373/0,169 s; listas 1,548/0,173 s; perfil 1,458/0,183 s; feed 2,038/0,292 s.
O primeiro conteúdo de biblioteca/listas/feed pode ser só o título da página;
esses tempos de heading não provam dados utilizáveis. Pausas de 22 s entre
pares/rotas ficaram fora das medidas; não provam uso habitual sem pausas.

## Gargalos e hipóteses já identificados

- **Confirmado no navegador e código:** Buscar continuou desabilitado quando o
  destaque apareceu em todas as vinte amostras. O busy global só foi liberado
  no fim, chegando a cerca de 13 s por depender das seções complementares.
- **Confirmado nas chamadas:** Kitsu variável e três consultas sequenciais
  (limite de concorrência atual um) prolongam a conclusão da Home; dois erros
  de rede nesta rodada. Não aumentar retries/concorrência sem investigar quota.
- **Confirmado volume, causa de CPU não provada:** mediana de payload recebido
  por WebSocket na Home aquecida foi 231396 bytes (226 KiB), em ambas as larguras.
  SocialState tem 113 campos públicos anotados e nove computed vars. Redução de
  dados de cards merece comparação; não justificar refatoração ampla só por isso.
- **Imagem:** em 390 px/DPR 1, a imagem principal de 1280 px foi exibida em
  351 px. Estudar srcset/sizes com DPR 1/2/3; não reduzir cegamente a qualidade.
  Economia de bytes/LCP ainda não medida.
- **Configuração/código:** LIBRARY_PAGINATION_ENABLED não está definida no .env
  usado, portanto o padrão é o caminho legado (sujeito a overrides de ambiente).
  Biblioteca e listas podem baixar todo o catálogo. Não ativar flag sem validar
  contrato real, continuação, duas contas e regressões. DEFAULT_LIST_IDENTITY_ENABLED=true;
  navegação de listas pode criar padrões ausentes, por isso escritas foram bloqueadas.
- **API social:** duas respostas 404 reais de /likes, com fallback existente;
  não confundir com sucesso do endpoint. Não publicar correção remota nesta rodada.

## Interrupções e limites do instrumento

Primeira tentativa: readiness esperava 200 em /login, mas a rota retorna 307;
corrigida no instrumento e acrescida conferência de /_health. Segunda: nenhum
ciclo válido de browser confirmado, logo zero tempos publicados dessa tentativa.
Terceira: localhost alinhado ao endpoint WebSocket, proxy existente de leituras
e vinte amostras Home válidas como medições (duas com conteúdo parcial).

Depois do desktop, o proxy recusou localmente GET /posts/{id}/discussion por
allowlist incompleta, antes de encaminhar. Isso não era escrita. A allowlist do
instrumento foi ampliada somente para esse GET; a retomada pulava Home/desktop,
mas o usuário pediu pausa antes das leituras móveis da conta. O fechamento
solicitado gerou TargetClosedError/ConnectionResetError no encerramento: não
classificar isso como novo defeito funcional. Uma tentativa de login retornou
403 antes de sessão member ativa ser confirmada; credenciais não foram registradas.

Raw privados e fontes do instrumento: .local/performance-analysis-20261109 no
diretório original. Todas as tentativas preservadas (.attempt1/.attempt2/.attempt3).
Não repetir run.py na mesma pasta: usa destinos fixos. Retomada requer novo
diretório de saída/frontend ou parametrização, preservando as 28 amostras.
Sessão anterior encerrada; se medir conta novamente, login manual seguro.

## Próximos passos após o usuário retomar

1. Consolidar diagnóstico e plano técnico final; não implementar otimizações.
2. Revisar métricas/instrumento e registrar versão do navegador, LCP/CLS e bytes
   de imagens por CDP; distinguir falha parcial de sucesso completo. Validar a
   guarda da nova rota GET sem liberar qualquer POST/PUT/DELETE de conteúdo.
3. Completar leituras de conta em 390 px, avaliações somente de leitura e social;
   depois cinco pares controlados, tamanhos de coleção e duas contas quando
   autorizados. Nenhuma escrita/conta nova foi autorizada por esta pausa.
4. Propor primeiro separar o busy da busca das seções opcionais, com guardas
   de geração/rota/query; depois apresentação compacta de cards, imagens e
   paginação/referências. Classificar impacto/esforço e riscos antes de implementar.
5. Apresentar metas numéricas justificadas para revisão, ainda não aprovadas.
   As metas históricas Python/Home (destaque/conclusão mediana fria <=1/10 s,
   aquecida <=0,2/0,5 s; chamadas de provedor <=22/0) não são metas de browser.

1.3 permanece parcial; 1.5 depende da apresentação/aprovação do plano. O relatório
final e a priorização solicitados antes da pausa ainda precisam ser concluídos.
Nenhuma tarefa foi marcada como concluída; nenhuma medição administrativa remota.
