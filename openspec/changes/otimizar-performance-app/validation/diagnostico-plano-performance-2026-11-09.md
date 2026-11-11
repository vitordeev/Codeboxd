# Diagnóstico e plano técnico de performance — 09/11/2026

**Resultado desta etapa: diagnóstico e propostas para revisão; nenhuma otimização
implementada.** Change otimizar-performance-app permanece **17/37**, com vinte
tarefas abertas. Administração permanece 33/34, sem testes administrativos remotos.
Usuário autorizou retomar e realizou login local de conta comum; escritas de
conteúdo permaneceram bloqueadas. Não houve commit, push, merge ou arquivamento.

## Base, ambiente e evidências

Worktree D:\Repositorios GIT\Codeboxd-performance-20261109, branch
task/performance-20261109, base a21c806. Diretório original, contribuições locais
e ambos os lockfiles foram preservados. Checkpoint desta retomada contém ZIP e
hashes no diretório privado `.local/performance-resume-20261109-190918`. Compilação pode
reescrever locks: cópia privada dos gerados e restauração somente dos bytes
anteriores ao nosso build, sem restaurar dados remotos ou alterações de terceiros.

Medições locais de produção em 3032; runtime .venv existente no diretório
original, código/cwd da worktree. Python 3.13.1, Reflex 0.9.11.post1, httpx 0.28.1,
Playwright 1.64.0. Retomada com Edge 157.0.4341.42. Não atualizar
framework/dependências como parte deste diagnóstico. Sem Docker.

- [28 amostras e HTTPs anteriores](medicoes-parciais-2026-11-09.json), preservadas
  sem repetição: vinte Home e oito leituras desktop de membro.
- [Oito leituras adicionais em 390 px](medicoes-retomada-2026-11-09.json): total
  de **36 navegações únicas**, além da tentativa Python/provedores separada.
- [Plano anterior à execução](retomada-analise-2026-11-09.md) e
  [registro histórico da pausa](pausa-analise-2026-11-09.md) preservados.

Na retomada, autenticação member/active confirmada por GET independente.
Credenciais, token, cookies e storage usados somente em memória; sem screenshots,
traces, corpos, nomes, IDs de contas/obras ou tokens nos relatórios públicos.
Nove verificações offline da allowlist passaram antes da rede, incluindo GET de
discussão e recusa de mutações. Elas são validação de instrumento, não benchmark.

## Home: linha de referência de navegador

Mediana / pior amostra em segundos, cinco pares **tentados** por viewport.
Cache frio: contexto novo, cache público Python limpo na instância isolada;
aquecido: recarga no mesmo contexto, cache público preservado. Pool de conexões
permaneceu ativo: não é TCP frio. Não confundir essas condições com caches
privados da conta ou navegação SPA habitual.

| Viewport | Cache | Destaque visível | Fim do ciclo observado | Conteúdo parcial |
| --- | --- | ---: | ---: | --- |
| 1440x900 | Frio | 1,322 / 2,090 | 11,846 / 12,989 | Uma de cinco amostras |
| 1440x900 | Aquecido | 0,380 / 0,599 | 0,864 / 2,520 | Nenhuma; houve recuperação da falha anterior |
| 390x900 | Frio | 1,356 / 1,765 | 7,002 / 13,541 | Uma de cinco amostras |
| 390x900 | Aquecido | 0,401 / 0,665 | 0,786 / 4,706 | Nenhuma; houve recuperação da falha anterior |

As medianas incluem as duas tentativas com seção indisponível. Há **quatro pares
com conteúdo completo por viewport**, não cinco aprovados. Os dados não suportam
p95 nem a conclusão de que o hardware móvel é mais rápido: 390 px é viewport de
desktop, sem throttling/DPR móvel específico. Pausas de 22 s entre pares ficaram
fora dos tempos; não demonstram uso habitual sem pausas.

Todas as visitas frias fizeram 23 chamadas Python: dez TMDB, três Kitsu, nove
Open Library e uma Xano. Nas revisitas após conteúdo completo: zero aos provedores
e uma Xano. As revisitas após falha refizeram consultas necessárias para recuperar
as seções; isso não é evidência de cache quebrado. Não contar o proxy local e seu
encaminhamento como duas chamadas físicas. Zero erros JavaScript na Home.

## Comparação com medições anteriores

Em [04/11](retomada-2026-11-04.md), a camada **Python/provedores**, excluindo
Xano/browser, teve cinco pares completos: mediana destaque/conclusão fria
0,252/3,457 s; aquecida 0,101/0,118 s; 22/0 chamadas. Na nova tentativa dessa
mesma camada, dois pares completaram: conclusão fria 4,224 e 9,790 s; aquecida
0,028 e 0,026 s. A terceira amostra fria terminou parcial em 12,855 s.

A referência antiga continua válida para seu escopo, mas não é linha anterior
do browser atual. Não atribuir diferença a melhoria/regressão de código: não houve
intervenção A/B, há versões/condições de runtime e rede diferentes, e a tentativa
nova não completou cinco pares. As 34 etapas funcionais de 05/11, com pausas de
22 s e uma amostra por viewport, também não eram benchmark completo.

## Biblioteca, listas e social: leitura descritiva

Desktop anterior, fim do ciclo primeiro/repetido: biblioteca 1,373/0,169 s;
listas 1,548/0,173 s; perfil 1,458/0,183 s; feed 2,038/0,292 s.
Retomada em 390 px:

| Jornada | Visita | Fim do ciclo (s) | HTTPs Python observados | Alertas UI |
| --- | --- | ---: | ---: | ---: |
| library | first | 2.492 | 3 | 0 |
| library | repeat | 0.394 | 0 | 0 |
| lists | first | 1.552 | 3 | 0 |
| lists | repeat | 0.250 | 0 | 0 |
| profile | first | 2.680 | 4 | 0 |
| profile | repeat | 0.338 | 0 | 0 |
| feed | first | 2.616 | 6 | 0 |
| feed | repeat | 0.517 | 1 | 0 |

Na retomada foram renderizados quatro cards na biblioteca, duas listas próprias,
quatro cards de atividade no perfil e quatro posts no feed. Mesmas contagens na
repetição, zero alertas capturados. O seletor de primeiro conteúdo em biblioteca,
listas e feed era o heading; por isso não se usa primary_ms dessas telas como
prova de dados utilizáveis. Fim do ciclo busy e contagens após carregar sustentam
as leituras, sem substituir integridade/paginação completas.

São **um par por rota/viewport**, não cinco amostras nem coleções grandes.
Desktop foi medido em navegador visível; retomada em headless após login visível,
com cookies/storage transferidos só em memória. A identidade igual entre as
sessões não foi registrada/provada; ambas foram verificadas como member/active.
Não calcular ganho percentual desktop→390 como efeito do layout ou de otimização.
Cache privado não foi controlado: as repetições sem HTTP são observadas, não
garantia geral de TTL, invalidação ou isolamento entre contas.

Esta retomada fez **23 requisições Xano: um POST de login e 22 GET**, com 21
respostas 200 e duas 404 em /likes; zero 429 e nenhum método de mutação de
conteúdo. O POST autentica/emite sessão; não chamar tudo de leitura pura. Logs
operacionais normais de autenticação não foram apagados. Não há prova de ausência
de 429 em navegação habitual: as pausas entre rotas continuam relevantes.

## Gargalos confirmados e hipóteses

| Área | Evidência | Conclusão e limite |
| --- | --- | --- |
| Espera global da Home | Buscar desabilitado no momento do destaque em 20/20 visitas; disabled depende de S.busy, liberado após a conclusão do carregamento | Gargalo de interação comprovado. Fim do ciclo chega a 13,54 s; ainda medir timestamp direto do botão habilitado para comparação futura |
| Dependência Kitsu | Três consultas serializadas pelo semaphore de anime; dois erros de rede de ~8 s e forte variação entre amostras | Fonte externa prolonga complementos. Não justifica aumentar retries, timeout ou concorrência sem estudo |
| Estado Reflex | Payload WebSocket aquecido mediano de 231396 bytes (~226 KiB), frio mediano ~852/785 KiB em 1440/390; 113 campos públicos anotados e nove computed vars em SocialState | Volume medido; CPU, custo de serialização e causa exata da demora ainda não isolados. Bytes são payload UTF-8 decodificado, não TLS/bytes físicos |
| Imagem principal | Natural 1280 px para 351 px de exibição na visita 390 px/DPR padrão 1 | Candidata a srcset/sizes; não forçar baixa resolução em DPR 2/3. Bytes transferidos/LCP ainda não medidos por CDP |
| Biblioteca | Retomada fez GET de media e interactions antes dos quatro cards, compatível com caminho legado; flag de paginação não definida no .env usado | Carga de catálogo integral no código e ausência de continuação grande medida. Não ativar flag sem contrato/contas/limites verificados |
| Listas | Catálogo carregado antes do diretório; três GET na primeira visita para duas listas | Dependência de referência candidata a adiamento; preservar seletor de obras, itens e preparação dos padrões existentes |
| Perfil/feed | Perfil consulta referências; feed fez seis HTTPs na primeira visita e um na repetição | Investigar consultas/referências por contexto. Não eliminar dados de autores, mídia ou permissões para reduzir contagem |
| /likes | 404 em primeira visita e repetição, duas vezes na retomada, como no desktop anterior | Contrato remoto ausente ou incompatível observado; fallback mantém fluxo. Não mascarar com cache negativo nem publicar mudança remota sem escopo/aprovação |

Requisições do browser e payload de estado são camadas diferentes. ResourceTiming
cross-origin pode informar tamanho zero sem Timing-Allow-Origin; não interpretar
isso como zero tráfego de imagem. LCP, CLS, INP, bytes CDP e CPU não foram medidos
adequadamente nesta etapa. Não há conclusão de vazamento ou defeito do framework.

A documentação [de estrutura de estado](https://reflex.dev/docs/state-structure/overview/)
explica o custo de carregar estados relacionados e computed vars; a de
[backend-only vars](https://reflex.dev/docs/vars/base-vars/) orienta manter dados
não renderizados fora da sincronização. Isso fundamenta uma inspeção localizada,
não uma migração ampla ou upgrade. Conferir APIs da versão instalada ao implementar.

O [plano Free publicado pelo Xano](https://www.xano.com/pricing/) mantém 10
requisições/20 s, compatível com o diagnóstico histórico de 05/11. O plano efetivo
da conta não foi reinspecionado nesta retomada; não presumir quota por endpoint
ou usuário. Zero 429 com pausas não comprova que o limite foi removido.

## Plano ordenado por impacto e esforço — para revisão

| Ordem | Proposta | Impacto / esforço | Arquivos candidatos e validação antes de considerar entrega |
| --- | --- | --- | --- |
| P0 Home | Separar pendência da busca das seções opcionais, preservando carregamento progressivo | Alto / médio; evidência mais direta de espera percebida | state/social.py e pages/social.py; testar busca durante Kitsu lento/falho, home→busca→obra, geração/rota/query e dupla submissão. Um loader não pode liberar o pending de outra operação |
| P1 Biblioteca | Validar leitura do contrato paginado já existente e ativação apenas em ensaio aprovado; evitar catálogo completo | Alto conforme crescimento / médio | state/social.py, env de ensaio e testes; primeira/última página, 250+ itens descartáveis só se autorizados, sem omissão/duplicata, duas contas. Nenhuma flag foi alterada agora |
| P2 Listas | Adiar referências de mídia até abrir itens/seletor, se não necessárias ao diretório | Médio-alto / médio | state/social.py e componentes de listas; diretório vazio, público/privado, padrões, seleção, abertura/retorno e permissões. Não remover reparo sem contrato substituto |
| P3 Avaliações | Completar medição da ficha e avaliação atual, separando dados principais, complementos e restauração pessoal | Decisão depende de dados / baixo para medir | Reusar entregas 5.1–5.3; 5.4 ainda sem benchmark. Gravações somente com alvos descartáveis autorizados; não repetir avaliação real nesta rodada |
| P4 Estado e imagens da Home | Medir campos efetivamente usados por cards, deltas e imagem principal; propor representação compacta e variantes responsivas | Médio-alto / médio | pages/social.py, apresentação de mídia e state/social.py; preservar conteúdo, navegação e detalhes; CDP, LCP/CLS, DPR 1/2/3 e comparação por campo. Sem refatorar toda SocialState |
| P5 Social | Reduzir dependências de referências por rota e revisar contrato /likes | Médio-alto / médio-alto | state/social.py e serviços; perfil próprio/outro, atividade vazia, feed, seguir/curtir e invalidação. Alteração de endpoint Xano é proposta separada, não autorizada automaticamente |

P0 é o primeiro candidato para implementação **após revisão**, por ter evidência
de interação e não exigir mudança de contrato remoto, TTL ou autorização. Os
demais exigem medições/contratos adicionais antes de escolher a intervenção.
Não implementar P0 simplesmente removendo disabled: há concorrência entre eventos
e a guarda busy atual protege outras ações. Não aumentar cache/retry para esconder
erros, retirar seções ou dados, ou remover validação fresca de ações protegidas.

Para cada incremento aprovado: preservar o diff anterior, aplicar somente seus
arquivos, executar regressões pertinentes, compile seco e produção isolada,
repetir os cenários afetados no mesmo protocolo. Rollback só do próprio incremento;
contratos/dados remotos exigem plano separado. Sem reset global ou exclusão de logs.

## Metas numéricas propostas — ainda NÃO aprovadas

| Escopo | Proposta | Justificativa / dependência |
| --- | --- | --- |
| Home browser: destaque, mediana | Frio <=1,5 s; aquecido <=0,5 s | Próximo das medianas observadas 1,32–1,36/0,38–0,40; preservar caminho que já atende, sem impor esses números aos provedores individualmente |
| Home browser: busca habilitada, mediana | Frio <=3 s; aquecido <=1 s | Conteúdo chega antes, mas busy depende do fim em até 13,54 s. Medir o botão diretamente no baseline adicional; não confundir essa meta com terminar todas as seções remotas em 3 s |
| Chamadas Home com todas as seções completas | Não exceder 22 provedores +1 Xano a frio; 0 provedores +1 Xano aquecida | Contagens observadas. Recuperação de seção falha é caso separado; orçamento não proíbe retry manual necessário nem omite conteúdo |
| Payload de estado da Home | Reduzir >=30% no aquecido, mantendo conteúdo e contagens; ~226 para <=158 KiB | Volume medido; aceitar só com deltas e dados comparáveis e sem degradação funcional. Não promete o mesmo ganho de latência |
| Biblioteca/listas/perfil/feed, conjunto pequeno | Mediana primeira <=3 s; repetida <=0,75 s; sem elevar chamadas atuais | Todos os pares descritivos terminaram primeira em <=2,69 s/repetida <=0,52 s. Proposta conservadora, precisa de cinco amostras por cenário, estado vazio e tamanhos maiores |
| Paginação | Custo inicial limitado ao lote de 20 itens e às chamadas do contrato, independente de N | Baseado no candidato já publicado, não em baixar só 20 e omitir o resto. Validar continuação/identidade/totais e duas contas antes de aprovar orçamento definitivo |
| Imagens e Web Vitals | Definir orçamento de bytes e LCP/CLS depois de CDP/DPR; investigar se >=30% de bytes da imagem principal podem ser reduzidos em DPR 1 | 1280→351 px é indício dimensional; não há base para inventar ganho em bytes, LCP ou meta absoluta agora |

As metas históricas aprovadas da **camada Python/Home** continuam distintas:
medianas destaque/conclusão fria <=1/10 s e aquecida <=0,2/0,5 s; 22/0 chamadas
de provedores. Não transplantar essas metas para browser ou outras jornadas.
As novas propostas atendem ao pedido de plano para revisão; não são decisões
aprovadas nem encerram 1.5. Onde falta baseline, a pendência está explícita.

## Checklist e lacunas que permanecem

Concluídas (17): 1.1, 1.2, 1.4, 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 6.1, 6.3.

Pendentes (20): 1.3, 1.5, 2.3, 2.4, 3.5, 4.4, 5.4, 6.2, 6.4, 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4, 9.1, 9.2, 9.3.

Ordem recomendada: completar 1.3 e revisar/aprovar 1.5; depois comparação Home
4.4 e preparação de biblioteca/listas 6.2/6.4; completar leitura/benchmark de
avaliações 5.4 e social 7.1–7.4. Autenticação/cadastro/recuperação 2.3/2.4,
uso habitual/429 3.5 e integração 9.1–9.3 exigem suas próprias condições. Etapa
administrativa 8.1–8.4 fica fora desta rodada por instrução do usuário.

Não executados ou insuficientes: cinco pares completos Home por viewport, cinco
pares por jornada privada, coleções grandes/página final, segunda conta,
cache privado frio/aquecido comprovado, outra identidade de perfil, avaliação/
salvamento, upload/curtidas/comentários e jornada habitual sem pausas. A discussão
foi permitida na guarda, mas sua leitura funcional não foi exercitada nesta
retomada. Nenhum dado foi criado para preencher esses casos.

As medições atuais fundamentam prioridades, não fechamento de 1.3, 4.4, 5.4,
6.4 ou 7.1. 9.3 pede consolidação final de toda a change e também permanece
aberta. Administração não é concluída por benchmark de Home.

## Encerramento e preservação

Build isolado concluído e leituras executadas; encerramento gerou mensagens
ConnectionResetError no proxy ao fechar sockets, sem falha nas oito amostras.
Servidor 3032 e navegador de medição encerrados. Original e worktree conferidos
por hashes; arquivos de implementação, dependências e dados administrativos
inalterados. Novos arquivos desta retomada são planejamento, evidência e este
relatório; acompanhamento central recebe registro adicional sem apagar a pausa.
Validação Git/OpenSpec e scanner serão registrados na conferência final, sem
repetir a suíte funcional antiga de 494 testes ou os cenários administrativos.


### Confer?ncia final executada

- git diff --check: aprovado.
- git diff --quiet -- Codeboxd_main rxconfig.py requirements.txt reflex.lock:
  exit 0, sem altera??es funcionais/depend?ncias.
- openspec validate otimizar-performance-app --type change: v?lido.
- 17 checkboxes conclu?dos e vinte abertos, conferidos por leitura do checklist.
- Nove casos offline da guarda aprovados; oito novas amostras reais e 36 IDs
  ?nicos de navegador; 28 amostras anteriores conferidas integralmente.
- Scanner heur?stico em seis arquivos desta retomada: zero achados de padr?es
  ou valores secretos configurados, comparados somente em mem?ria. N?o ? garantia
  absoluta sobre outros arquivos n?o examinados.
- Preserva??o dos arquivos anteriores/original e dos dois locks da worktree por
  SHA-256; refer?ncia a21c806 e branches existentes mantidas. Porta 3032 livre.
- N?o foram reexecutados testes funcionais/administrativos j? comprovados:
  produto n?o foi modificado. Todos os resultados s?o das camadas identificadas.
