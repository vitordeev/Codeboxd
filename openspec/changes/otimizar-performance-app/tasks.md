# Tasks

Continuação posterior: comunidade não depende mais do carregamento da home;
14 testes dirigidos e compile aprovados. Isolamento dos utilitários fortalecido.
7.1/7.2 permanecem abertas por cobertura social e validação real ainda ausentes;
11/37 continua sendo a contagem de tarefas integralmente concluídas.
[Incremento](validation/comunidade-sem-home-2026-10-20.md) e
[build ainda bloqueado](validation/isolamento-build-2026-10-20.md).

Retomada solicitada pelo usuário após texto obrigatório: revisão confirma
11/37 concluídas e 26 abertas. Sem encerrar novos IDs nesta auditoria.
Build/prerender falhou ao iniciar o browser; estabilização operacional precede
baseline/metas e retomada das etapas reais.
[Matriz de implementação, pendências e sequência](validation/revisao-retomada-2026-10-20.md).

Correção operacional posterior em 20/10: restauração anterior só validara HTML,
mas processo herdara rede restrita. Reinício com rede aprovado e TMDB real/UI
restaurados; utilitários protegidos contra repetir o problema. 11 testes pertinentes
aprovados. Sem alterar a contagem 11/37: não é comparação global contra metas.
[Evidência](validation/tmdb-rede-restaurada-2026-10-20.md).

Planejamento criado em 20/10/2026. Nenhuma tarefa de implementação concluída.
Antes de qualquer edição, apresentar motivo, arquivos, impacto, testes e rollback
e aguardar aprovação específica. Incluir testes, evidências e atualizações
documentais no pedido de cada intervenção. Autorizações anteriores de outra
rodada não autorizam alterações novas. Manter IDs e histórico.

## 1. Inventário e linha de base

Avanço parcial autorizado em 20/10: instrumento isolado e seis testes simulados
criados; inventário inicial de rotas e chamadas registrado. Ainda sem medição
real ou autorização para servidor/contas. [Evidência](validation/instrumentacao-2026-10-20.md).
Manter 1.1/1.2 abertas até cumprir seus critérios completos.

Segunda rodada autorizada: executor do login até perfil com handlers reais e
HTTP simulado; 25 execuções e cinco novos testes aprovados. Confirmadas seis
chamadas no sucesso e bloqueio do detalhe do perfil por falha nas referências.
[Evidência](validation/login-simulado-2026-10-20.md). Não equivale à linha de base
real 1.3 nem identifica a quota 1.4; sem implementação de otimizações nesta rodada.

Medição real autorizada em rodada posterior: executor interativo e proxy local
com escopo restrito criados, seis testes offline aprovados; execução depende
do login manual do usuário. [Registro](validation/login-real-2026-10-20.md).
Não encerrar 1.3/1.4 sem resultados e critérios completos.

Resultado real obtido: 11 chamadas remotas (10 respostas 200 e 1 HTTP 429 em
GET `/auth/me`, Retry-After 20 s), interrompido no desktop; celular não executado.
Escopo da quota ainda não confirmado e tempos de revisitas têm limitação de
correlação com on_load. Manter 1.3/1.4 abertas.
[Evidência](validation/login-real-2026-10-20.md).

- [x] 1.1 Inventariar rotas, subfluxos e chamadas disparadas por evento, do login à administração; verificar matriz de cobertura contra rotas, componentes e handlers existentes e registrar após aprovação documental.

  Concluída nesta rodada a pedido do usuário de selecionar e realizar uma tarefa:
  inventário AST reproduzível de 19 arquivos, 21 rotas, 99 vínculos on_* e 279
  funções, com matriz manual por jornada e dois testes offline aprovados.
  Chamadas posicionais, funções auxiliares e serviços estão no JSON; dispatch
  dinâmico exige interpretação. Não é medição de tráfego/latência nem validação
  remota. [Evidência e limites](validation/inventario-rotas-eventos-2026-10-20.md).
- [ ] 1.2 Propor e obter aprovação para instrumentos de medição, arquivos de evidência, servidor/reinício e dados de teste necessários; verificar registro explícito de escopo autorizado antes de criá-los ou executá-los.
- [ ] 1.3 Medir jornadas com cache vazio/aquecido, desktop/celular e contas adequadas; verificar pelo menos cinco amostras por cenário, mediana, pior amostra e contagens por serviço, sem segredos nos registros.
- [ ] 1.4 Identificar origem e escopo do HTTP 429, incluindo chamadas Python aos serviços; verificar endpoint sanitizado, sequência disparadora e Retry-After, distinguindo reprodução real de simulação.
- [ ] 1.5 Apresentar prioridades e metas numéricas por jornada e obter aprovação antes de registrá-las; verificar tabela com linha de base, orçamento, ambiente e critério de comparação para cada etapa.

## 2. Login, cadastro, recuperação e sessão

Incremento de perfil aprovado e implementado localmente em 20/10: identidade e
contagens publicadas antes de referências, com erros por seção. 188 testes e
compilação aprovados; browser/reinício/metas reais ainda pendentes. Manter as
tarefas amplas abertas. [Evidência](validation/perfil-progressivo-2026-10-20.md).

Instância atualizada iniciada em produção na porta 3030; `/login` e `/conta`
retornam HTTP 200. Browser não executado: Playwright ausente e instalação
aguarda aprovação específica do usuário. [Registro](validation/inicializacao-browser-2026-10-20.md).

Rodada seguinte autorizada: Playwright instalado; seis cenários de perfil no
Edge em 1440/390px passaram, com serviços locais fictícios e editor responsivo
durante referências lentas. 188 testes e pip check aprovados. Verificação remota,
metas reais e demais fluxos permanecem pendentes.
[Evidência atual](validation/perfil-browser-2026-10-20.md).

- [x] 2.1 Diagnosticar chamadas, redirecionamentos e bloqueios nos fluxos de autenticação e propor a primeira intervenção; verificar arquivos, motivo, segurança, verificação e aprovação explícita registrados.
- [x] 2.2 Aplicar somente a intervenção aprovada e seus testes; verificar login válido/inválido, sessão persistida/expirada, logout, conta desativada e falha transitória, preservando autorização e sem repetição de efeitos colaterais.
- [ ] 2.3 Validar cadastro e recuperação em lentidão/429, incluindo feedback e preservação de entrada permitida; verificar testes pertinentes e browser com operações reais previamente aprovadas, sem encerrar a pendência histórica de e-mail por simulação.
- [ ] 2.4 Medir novamente os fluxos desta etapa e registrar resultados; verificar orçamento aprovado, desktop/celular, regressões e compilação, mantendo abertas verificações sem acesso ou evidência.

## 3. Requisições e HTTP 429

Incremento aprovado em 20/10: identidade de navegação por 15 s apenas para
membros, detalhe de perfil no cache e cooldown de `/auth/me` implementados.
205 testes e compilação locais aprovados; cinco visitas rápidas usam cinco
chamadas em simulação. Tarefas amplas continuam abertas por exigirem revisão
e validação além desse incremento. [Evidência](validation/sessao-cache-cooldown-2026-10-20.md).

Repetição real autorizada: instrumentação de ciclo corrigida (sete testes
aprovados), mas frontend gerado com versão divergente falhou na recriação.
Zero chamadas remotas; recuperação de `.web` aguarda aprovação.
[Registro](validation/retomada-medicao-cache-2026-10-20.md).

Recuperação posteriormente aprovada: `.web` preservada em `.local/` e recriada
com versão 0.9.11.post1; compilação e sete testes da instrumentação passaram.
Executor real retomado; validação permanece aberta até resultados e restauração.

Resultado posterior: usuário autenticou; dez ciclos de perfil em 1440/390px
completaram com nove respostas Xano 200 e nenhum 429, incluindo renovação após
expiração. Oito revisitas sem chamadas remotas. App normal atualizado restaurado
em 3030 e disponibilidade conferida. [Evidência](validation/resultado-login-real-apos-cache-2026-10-20.md).
As tarefas amplas permanecem abertas: faltam metas aprovadas, outras jornadas
e critérios de linha de base que esse cenário isolado não cobre.

- [x] 3.1 Revisar cache social de 15 segundos, cache público e tentativas existentes e propor ajustes fundamentados; verificar isolamento, invalidação, limites e compatibilidade, sem contabilizar implementação anterior como entrega nova.
- [x] 3.2 Após aprovação, corrigir duplicação de leituras/eventos identificada; verificar redução de chamadas com testes de concorrência, parâmetros/páginas distintos, expiração, troca de credenciais e erro não cacheado.
- [x] 3.3 Após aprovação, implementar tratamento de cooldown e tentativas no escopo diagnosticado; verificar Retry-After numérico/data HTTP, ausência/invalidade do cabeçalho, ausência de repetição de mutações e recuperação sem logout.
- [x] 3.4 Conferir invalidação após gravações e proteção contra leitura atrasada; verificar resposta tardia, troca de conta/obra e falha de gravação, sem exposição privada ou regressão de permissões.
- [ ] 3.5 Validar sequência de navegação que originou o relato e documentar volume/429 antes e depois; verificar integração real e navegador separadamente dos testes simulados e contra metas aprovadas.

Rodada de continuação autorizada pelo usuário após 1.1: 2.1/3.1/3.2/3.3
concluídas em seus critérios de diagnóstico e implementação/testes locais.
Leituras equivalentes pendentes agora compartilham uma chamada por sessão,
credencial, parâmetros e geração; duas consultas concorrentes usam uma chamada
no teste. Paginação fixa token e rejeita troca antes/durante a leitura.
GET de e-mail não repete automaticamente e respeita cooldown local; catálogo
interpreta Retry-After como data HTTP e não tenta antes de prazo longo.
244 testes e compilação passaram. Sem browser, remoto ou reinício; 3.4/3.5
continuam abertas. [Diagnóstico, decisões, testes e limites](validation/cache-concorrencia-cooldown-2026-10-20.md).

## 4. Home, categorias e buscas

- [ ] 4.1 Medir e propor melhoria do caminho crítico da home e das categorias; verificar distribuição de custo por provedor, primeiro conteúdo utilizável e aprovação da intervenção.
- [ ] 4.2 Aplicar melhoria aprovada de carregamento/recursos visuais e validar incrementalmente; verificar conteúdo principal antes de seção lenta, falha parcial, capas, ordem das séries e destaque preservados, com evidência e compilação.
- [x] 4.3 Medir e otimizar busca/paginação após aprovação; verificar busca nos quatro tipos, relevância, mais resultados sem duplicatas e resposta antiga ignorada, com testes e evidência por consulta.
- [ ] 4.4 Comparar ida/retorno e recarga em desktop/celular com cache vazio/aquecido; verificar metas de tempo/chamadas e registrar perdas ou limitações sem ocultar provedores indisponíveis.

## 5. Fichas e avaliações

- [x] 5.1 Diagnosticar fichas internas/externas nos quatro tipos e aprovar separação de dependências principais/complementares; verificar proposta com impacto em tradução, trailers, streaming, relacionados e críticas.
- [x] 5.2 Aplicar intervenção aprovada com regressões e documentação; verificar ficha utilizável durante complemento lento, identidade externa/Jikan preservada e resposta atrasada de outra obra ignorada.
- [ ] 5.3 Otimizar caminho de avaliação após aprovação; verificar nota decimal, editar/salvar, envio único, confirmação persistida, rascunho após falha e invalidação da leitura afetada.
- [ ] 5.4 Comparar carregamento e salvamento em desktop/celular; verificar metas aprovadas, testes pertinentes, compilação e browser autenticado, mantendo separado eventual reparo histórico de avaliações.

Continuação solicitada para concluir o restante: encerradas 2.2/3.4/4.3/5.1/5.2
por implementação e regressões locais. Busca repetida: duas consultas equivalentes
em uma chamada HTTP simulada; query/página distintas preservadas. Fichas têm
publicação progressiva e guardas para resultado tardio, inclusive avaliação,
feed, referências e listas. 259 testes e compilação passaram; browser em produção
com fixtures cobriu os quatro tipos, 1440/390px e cadastro/recuperação com 429.
5.3/5.4 continuam abertas por persistência/comparação real. Estado 11/37;
não encerrar etapas remotas, metas ou quota a partir de simulação.
[Evidência, reprodução e dependências](validation/continuacao-fichas-busca-2026-10-20.md).

## 6. Biblioteca e listas

Diagnóstico autorizado em 20/10: ferramenta local, 18 cenários × cinco amostras
e dez testes passaram, sem rede ou gravações reais. Confirmadas referências
de pessoas desnecessárias e carga integral antes de mostrar mais. Proposta
inicial de remover só essa dependência aguarda aprovação; 6.1 permanece aberta.
[Evidência](validation/biblioteca-listas-diagnostico-2026-10-20.md).

Intervenção posteriormente aprovada e implementada: removida só a dependência
de perfis nos dois loaders. 217 testes e compilação aprovados; 90 novas
execuções simuladas confirmaram redução e dados preservados. 6.1 concluída
como diagnóstico simulado/aprovação; navegador e uso real permanecem pendentes.
[Evidência atual](validation/biblioteca-listas-sem-perfis-2026-10-20.md).

Validação posterior autorizada: 22 cenários no Edge em 1440/390px passaram com
serviços locais fictícios, sem consultas de pessoas e com abertura/obras/seletor
preservados. Não equivale a paginação na origem ou autorização/quota real.
[Evidência](validation/biblioteca-listas-browser-2026-10-20.md). 6.2–6.4 continuam
abertas por critérios além dessa intervenção.

- [x] 6.1 Medir cargas integrais, referências e criação/reparo de listas durante navegação e apresentar intervenção; verificar quantidade de chamadas por ação e aprovação explícita.
- [ ] 6.2 Aplicar otimização aprovada de consulta/paginação; verificar acesso a todos os itens, ordenação/identidade, totais corretos, listas públicas/privadas e isolamento entre contas, com regressões e evidência.

  Incremento aprovado em 20/10: contrato candidato `/library`, tela/estado
  paginados e testes locais implementados, com flag desabilitada por padrão.
  Sem publicação, ativação, reinício ou navegador; listas ainda não paginadas.
  Tarefa permanece aberta. [Evidência e pré-condições](validation/biblioteca-paginada-local-2026-10-20.md).

  Validação posterior aprovada: 18 casos no navegador com fixtures locais
  passaram em 1440/390px, incluindo continuação completa de 250 itens,
  falha/retry, lentidão e cooldown. Sem alteração adicional de produto.
  Publicação, contrato/autorização/quota reais e ativação permanecem pendentes;
  não encerra 6.2 nem 6.4. [Resultado](validation/biblioteca-paginada-browser-2026-10-20.md).
  Validação real posterior: endpoint publicado no workspace 147717; login,
  sessão, perfil e primeira página autenticados responderam HTTP 200. Quatro
  itens reais passaram no contrato, sem 429; a flag foi habilitada no `.env`
  privado e o app normal reiniciado em 3030 (login/biblioteca HTTP 200). A conta
  não tem continuação; acesso a todas as páginas, isolamento entre contas,
  coleções grandes, quota habitual e listas continuam sem validação real.
  6.2 e 6.4 permanecem abertas. [Evidência](validation/biblioteca-paginada-xano-real-2026-10-20.md).
- [ ] 6.3 Otimizar atalhos e mutações aprovadas; verificar criar/editar/remover lista, adicionar/remover obra, refletir alteração confirmada e preservar rascunho em falha, sem repetição automática.
- [ ] 6.4 Comparar biblioteca/listas pequenas e grandes em desktop/celular; verificar metas aprovadas, chamadas sem N+1 e compilação, registrando validação real e simulada separadamente.

## 7. Perfis, comunidade e feed

- [ ] 7.1 Medir próprio perfil/outro perfil, seguidores, comunidade e feed e aprovar intervenções; verificar matriz de chamadas, referências, paginação e payload de estado/imagens.
- [ ] 7.2 Aplicar otimizações de leitura aprovadas; verificar perfis, estatísticas, seguir/deixar de seguir, feed e paginação sem omissões, duplicações ou alteração de permissões, com testes e evidência.
- [ ] 7.3 Aplicar otimizações aprovadas de posts/upload/curtidas/comentários; verificar criação/edição/exclusão, progresso, envio único, rascunho em falha, discussão sob demanda e limpeza de dados de teste autorizados.
- [ ] 7.4 Comparar sequência social em desktop/celular; verificar orçamento de tempo/chamadas, imagens e estado de interface em falhas parciais, com compilação e registros por camada.

## 8. Administração

- [ ] 8.1 Medir login admin, dashboard, usuários, catálogos, reports e demonstração com conta aprovada e propor intervenções; verificar dependências com gerenciamento-website sem conceder privilégios automaticamente.
- [ ] 8.2 Aplicar otimizações aprovadas de consultas/filtros/paginação; verificar contagens reais, busca, vazio, falha parcial, ausência de respostas antigas sobrescrevendo filtros e rejeição de membro/visitante/desativado.
- [ ] 8.3 Validar performance de mutações administrativas previamente aprovadas; verificar persistência, auditoria, autorização e ausência de duplicatas, preservando critérios funcionais da change administrativa.
- [ ] 8.4 Comparar todas as telas administrativas em desktop/celular contra metas aprovadas; verificar testes, compilação, browser e evidência remota, mantendo abertas tarefas sem conta/acesso.

## 9. Integração da jornada completa

- [ ] 9.1 Executar jornada login → home → busca → ficha → avaliação → biblioteca/listas → perfil/comunidade/feed → logout e suíte administrativa separada; verificar metas aprovadas, navegação rápida e ausência de vazamento entre contas.
- [ ] 9.2 Conferir cenário de uso habitual e falhas controladas com 429; verificar redução comprovada de chamadas e ausência de 429 no cenário habitual acordado, respeitando espera e preservando dados nas falhas induzidas.
- [ ] 9.3 Consolidar comparações finais, aprovações, limitações e pendências nas evidências e documentos centrais previamente autorizados; verificar cobertura de todas as rotas inventariadas, testes/compilação e distinção entre implementação, simulação, remoto e navegador.

## Workflow follow-up

- Após critérios atendidos e aprovação documental, sincronizar specs e arquivar pela skill apropriada.
- Não arquivar nem declarar performance integralmente resolvida enquanto metas ou validações obrigatórias permanecerem abertas.
