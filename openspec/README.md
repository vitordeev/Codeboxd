# OpenSpec do Codeboxd

Continuação da otimização: comunidade deixou de carregar toda a home e seus
provedores; 274 testes da suíte e compile aprovados. Frontends de validação
agora usam arquivos e dependências próprios. O timeout do build padrão continua
aberto, apesar de um build direto por Node ter passado; nenhum novo critério
amplo foi encerrado. [Comunidade](changes/otimizar-performance-app/validation/comunidade-sem-home-2026-10-20.md)
e [diagnóstico operacional](changes/otimizar-performance-app/validation/isolamento-build-2026-10-20.md).

Retomada da otimização solicitada em 20/10: auditoria confirma **11/37 tarefas**
concluídas, 26 abertas, com separação de código existente, validação local e
integração real. Build/prerender apresentou timeout e está na prioridade
operacional antes de novas medições. [Revisão e sequência para concluir](changes/otimizar-performance-app/validation/revisao-retomada-2026-10-20.md).

Texto obrigatório em denúncias/avaliações (20/10): implementado e publicado nos
dois contratos Xano, com backup e conferência do delta. 269 testes e compile
passaram; rejeição autenticada e navegador ainda pendentes (build falhou no
prerender). [Change separada, 3/5](changes/exigir-texto-denuncias-avaliacoes/tasks.md).

TMDB recuperado após relato em 20/10: o reinício anterior herdou restrição de
rede do agente (WinError 10013). App reiniciado com rede autorizada; quatro
endpoints reais retornaram 200/20 itens e as três fileiras de filmes exibiram
20 cards cada no navegador. Guardas de conectividade adicionadas aos utilitários;
11 testes pertinentes passaram. [Causa e evidência](changes/otimizar-performance-app/validation/tmdb-rede-restaurada-2026-10-20.md).

Continuação posterior em 20/10: **11/37 tarefas de performance concluídas**, 26
abertas. Encerradas 2.2/3.4/4.3/5.1/5.2: fichas progressivas, respostas tardias
protegidas e cache de busca; **259 testes e compilação aprovados**, com browser
desktop/celular e dados fictícios. Conclusão integral depende de diagnóstico/
implementação restantes, contas de teste aprovadas, baseline e metas explícitas.
[Entrega e critérios ainda abertos](changes/otimizar-performance-app/validation/continuacao-fichas-busca-2026-10-20.md).

Continuação de performance em 20/10: concluídas 2.1, 3.1, 3.2 e 3.3,
com diagnóstico, deduplicação de leituras concorrentes, proteção de credencial
na paginação e correções de retry/cooldown. **244 testes e compilação passaram**;
sem navegador, remoto ou reinício nesta rodada. Estado atual: **6/37 tarefas**,
31 abertas. [Resultado e limites](changes/otimizar-performance-app/validation/cache-concorrencia-cooldown-2026-10-20.md).

Inventário de performance atualizado em 20/10: tarefa 1.1 concluída com 21
rotas, 99 vínculos explícitos de eventos e 279 funções em 19 arquivos Python.
Ferramenta estática e dois testes offline aprovados; não mede latência ou tráfego
real. A change continua aberta, agora com 2/37 tarefas concluídas.
[Matriz, reprodução e limites](changes/otimizar-performance-app/validation/inventario-rotas-eventos-2026-10-20.md).

## Atualização de performance — 20/10/2026

Biblioteca paginada: endpoint publicado e validado autenticado no Xano com
quatro itens; primeira página aprovada, sem 429. Flag habilitada no `.env`
privado; app normal reiniciado e rotas HTTP 200 em 3030. Continuação real,
isolamento entre contas, coleções grandes e quota habitual ainda não validados;
6.2/6.4 e a change global continuam abertas. [Evidência](changes/otimizar-performance-app/validation/biblioteca-paginada-xano-real-2026-10-20.md).

Biblioteca paginada no navegador em 20/10: 18 cenários fictícios aprovados
em 1440/390px, incluindo 250 itens, lentidão, falha/retry e cooldown do 429.
Sem erros JavaScript ou overflow. Publicação/validação Xano e ativação ainda
pendentes; não encerra a change global. [Evidência](changes/otimizar-performance-app/validation/biblioteca-paginada-browser-2026-10-20.md).

Biblioteca paginada preparada localmente em 20/10: contrato candidato com
20 itens por lote e obras associadas; preservação de cards em falhas e proteção
de conta/rota. Flag desabilitada por padrão. Publicação e validação Xano,
ativação e navegador pendentes de aprovação. [Evidência](changes/otimizar-performance-app/validation/biblioteca-paginada-local-2026-10-20.md).

Biblioteca/listas no navegador em 20/10: 22 cenários com serviços fictícios
passaram em 1440/390px, sem consultas de pessoas, erros JavaScript ou overflow.
Obras, seletor, listas e falhas preservados. Sem validação Xano real nesta rodada.
[Evidência](changes/otimizar-performance-app/validation/biblioteca-listas-browser-2026-10-20.md).

Biblioteca/listas em 20/10: consulta desnecessária de pessoas removida dos dois
loaders após aprovação. 217 testes e compilação passaram. Em simulação pequena,
biblioteca 4→3 chamadas e listas 5→4; falha de perfis não bloqueia mais as telas.
Reinício e navegador pendentes. [Evidência](changes/otimizar-performance-app/validation/biblioteca-listas-sem-perfis-2026-10-20.md).

Diagnóstico de biblioteca/listas em 20/10: 90 execuções simuladas e dez testes
confirmam consulta de perfis desnecessária, carga integral antes de “Mostrar
mais” e gravações de preparação de listas ao abrir. Sem alterações de produto
ou acesso real nesta rodada. [Evidência e proposta](changes/otimizar-performance-app/validation/biblioteca-listas-diagnostico-2026-10-20.md).

Resultado real após cache em 20/10: dez visitas ao perfil (1440/390px)
concluídas, nove chamadas Xano e nenhum 429. Oito revisitas sem nova chamada,
mediana de 454,5 ms para perfil visível; renovação após expiração também passou.
App normal atualizado restaurado em 3030. Não equivale a validar todo o app.
[Evidência e limites](changes/otimizar-performance-app/validation/resultado-login-real-apos-cache-2026-10-20.md).

Recuperação local em 20/10: `.web` anterior preservada em `.local/` após
aprovação; frontend recriado em Reflex 0.9.11.post1 e compilação aprovada.
Sete testes da instrumentação passaram. Medição real retomada, aguardando
build/login antes de resultados. [Registro](changes/otimizar-performance-app/validation/retomada-medicao-cache-2026-10-20.md).

Retomada após cache em 20/10: marcos de visita corrigidos e sete testes da
instrumentação aprovados, mas inicialização falhou ao recriar frontend gerado.
Zero chamadas remotas; servidor normal parado. Preservação/recriação de `.web`
solicitada ao usuário. [Diagnóstico](changes/otimizar-performance-app/validation/retomada-medicao-cache-2026-10-20.md).

Sessão/perfil em 20/10: reutilização de identidade de leitura por 15 s, cache do
detalhe e cooldown de `/auth/me` implementados após aprovação. 205 testes e
compilação passaram; cinco visitas rápidas usam cinco chamadas em simulação.
Reinício e nova validação remota ainda pendentes.
[Evidência](changes/otimizar-performance-app/validation/sessao-cache-cooldown-2026-10-20.md).

Medição real em 20/10: aviso reproduzido na 11ª chamada remota, GET `/auth/me`,
com HTTP 429 e Retry-After de 20 s. Coleta interrompida no desktop; celular e
escopo exato da quota ainda pendentes. Próxima intervenção depende de aprovação.
[Evidência e limites](changes/otimizar-performance-app/validation/login-real-2026-10-20.md).

Perfil no navegador em 20/10: Playwright instalado após aprovação, seis cenários
desktop/celular com serviços locais fictícios passaram, inclusive 429 e editor
durante carregamento. 188 testes e pip check aprovados. Sem validação de quota
ou latência Xano real. [Evidência](changes/otimizar-performance-app/validation/perfil-browser-2026-10-20.md).

Execução local em 20/10: app atualizado iniciado em produção na porta 3030,
HTML de login/conta verificado com HTTP 200. Validação no navegador ainda
pendente: Playwright ausente na `.venv`, instalação solicitada ao usuário.
[Registro](changes/otimizar-performance-app/validation/inicializacao-browser-2026-10-20.md).

Perfil progressivo em 20/10: identidade e contagens enviadas antes de catálogo e
pessoas, com carregamento/erro por seção. 188 testes e compilação locais
aprovados; seis chamadas preservadas, sem comprovação de redução de 429.
Validação visual/interação e reinício pendentes de aprovação.
[Evidência](changes/otimizar-performance-app/validation/perfil-progressivo-2026-10-20.md).

Login/perfil em 20/10: 25 execuções simuladas de handlers reais confirmam seis
chamadas no sucesso e dependência do detalhe do perfil em referências do catálogo.
Cinco novos testes passaram; nenhum acesso remoto ou otimização do app nesta
rodada. [Evidência](changes/otimizar-performance-app/validation/login-simulado-2026-10-20.md).

Instrumentação de performance em 20/10: ferramenta local isolada criada, seis
testes simulados aprovados e inventário inicial registrado. Não houve alteração
de comportamento do app, acesso remoto ou reinício. Medições reais pendentes
de cenário e aprovação. [Evidência](changes/otimizar-performance-app/validation/instrumentacao-2026-10-20.md).

Planejamento de performance em 20/10: criada a change
[`otimizar-performance-app`](changes/otimizar-performance-app/proposal.md),
do login à administração, com diagnóstico, metas após linha de base e validação
por jornada. Implementação não iniciada nesta change. Cada alteração futura
requer aprovação prévia do usuário com motivo, escopo e verificação.
[Tarefas](changes/otimizar-performance-app/tasks.md).

Requisições em 20/10: leituras repetidas de catálogo, perfis, listas e avaliações
reutilizadas por 15 segundos por sessão, com invalidação em gravações.
174 testes e compilação locais aprovados; confirmação de redução de HTTP 429
na navegação autenticada pendente.
[Evidência](validation/requisicoes-navegacao-2026-10-20.md).

Recuperação de senha em 20/10: corrigido conflito entre os campos de e-mail
das duas etapas, reproduzido e validado no navegador. 170 testes e compilação
passaram. Change em 7/8 tarefas; entrega em caixa real ainda pendente.
[Retomada](changes/recuperar-senha-codigo-6-digitos/validation/retomada-2026-10-20.md).

Identidade da avaliação em 20/10: corrigida seleção indevida do primeiro
registro da resposta Xano; fichas e envios agora validam a obra exata.
170 testes locais e compilação aprovados; dados antigos não foram movidos.
[Evidência e pendência](validation/avaliacao-identidade-2026-10-20.md).

Avaliação em 20/10: envio bloqueado durante gravação, repetição idêntica
suprimida e formulário fechado após confirmação, com edição explícita.
165 testes locais e compilação aprovados.
[Evidência e limites](validation/avaliacao-envio-unico-2026-10-20.md).

Carregamento em 20/10: homepage exibe resultados progressivamente, usa cache
público de cinco minutos e separa consultas por provedor. Recarga medida com
categorias habilitadas em 1,43 s (antes 9,40 s).
[Evidência e limites](validation/carregamento-home-2026-10-20.md).

Seleção de séries em 20/10: Stranger Things, The Boys, Reacher e La Casa de
Papel passam ao início da fileira. [Evidência](validation/series-selecao-2026-10-20.md).

Séries populares em 20/10: cache de três séries locais passa a ser substituído
pela lista TMDB quando disponível. [Evidência](validation/series-populares-cache-2026-10-20.md).

Card principal em 20/10: destaque prioriza “Agora nos cinemas”, atualmente
Street Fighter (2026). [Evidência](validation/card-principal-atual-2026-10-20.md).

TMDB em 20/10: configuração anterior restaurada localmente; cinema, melhores
avaliados e próximos filmes retornaram HTTP 200 com 20 obras por seleção.
[Evidência](validation/restaurar-tmdb-2026-10-20.md).

Página principal em 20/10: alternativa com obras salvas restaurada por pedido
do usuário, preservando o ajuste independente no dashboard.
[Evidência](validation/restaurar-principal-2026-10-20.md).

Dashboard em 20/10: abas do catálogo abrem sem filtros anteriores e incluem
“Ver todas”. Ajuste anterior na descoberta retirado após esclarecimento do usuário.
[Evidência](changes/gerenciamento-website/validation/catalogo-inicial-2026-10-20.md).

Login em 20/10: erro de serviço indisponível reproduzido no navegador;
`.env` ausente restaurado com URLs públicas Xano.
[Diagnóstico e validação](validation/login-configuracao-2026-10-20.md).

Mostrar/ocultar senha em 20/10: controle adicionado ao login, cadastro e
redefinição. [Implementação e validação](validation/mostrar-senha-2026-10-20.md).

Limpeza local em 20/10: 28 arquivos de cache Python removidos (540.904 bytes).
Arquivos com finalidade documentada e dados locais preservados.
[Escopo e evidência](validation/limpeza-arquivos-2026-10-20.md).

Meias estrelas em 19/10: seleção de 0,5 a 5, preenchimento parcial, vírgula decimal
e restauração para visitante/conta. 148 testes, compilação e navegador/Xano real
aprovados, com limpeza da avaliação de teste. [Change](changes/avaliar-meias-estrelas/tasks.md),
5/5 tarefas verificadas.

Retorno à descoberta aprimorado em 19/10: botão arredondado com seta amarela,
hover/foco e área de toque de 46px. Compilação e navegador desktop/celular
aprovados. [P.13 / evidência](validation/voltar-descoberta-2026-10-19.md).

Denúncia de obras corrigida em 19/10: erros visíveis no modal, rascunho preservado,
espera de 429 respeitada e identidade externa resolvida ao enviar. 143 testes,
compilação, Xano real e fluxo de sucesso no navegador aprovados, com limpeza dos
reports de teste. [Evidência](changes/gerenciamento-website/validation/denunciar-obras-2026-10-19.md).

Tradução em 19/10/2026: DeepL integrado localmente às descrições das fichas de
animes/livros, com cache persistente e fallback. Chave configurada privadamente;
smoke real DeepL e 136 testes locais passaram. Revisão de navegador pendente.
[Change](changes/traduzir-descricoes-deepl/tasks.md), 5/6 tarefas verificadas.

Atualização de 19/10/2026: os três GETs de buscas administrativas foram publicados
após backup e dry-run limitado; conferência final sem delta. 18 testes locais
passaram e o acesso de visitante/membro foi rejeitado. Validação funcional com
admin aprovado ainda pendente por falta de token. [Evidência atual](changes/gerenciamento-website/validation/publicacao-buscas-admin-2026-10-19.md).

Revisão documental: 13/10/2026. Este é o ponto de entrada para retomar o projeto.

Encerramento da rodada em 14/10/2026: administração publicada no Xano com
validação parcial de acesso; P.5 (imagem de post) corrigida/publicada e validada
em 15 cenários de browser; 120 testes locais passaram. Backup verificado no commit
`f93287e` de 13/10, às 23h42. Contas administrativas aprovadas, fluxo de e-mail e
rotação TMDB continuam pendentes. Evidências atuais:
[publicação administrativa](changes/gerenciamento-website/validation/publicacao-admin-2026-10-13.md)
e [uploads/sessão](validation/uploads-and-session-2026-10-13.md).

## Onde encontrar cada informação

| Documento/pasta | Responsabilidade |
| --- | --- |
| [RELATORIO_STATUS.md](RELATORIO_STATUS.md) | Relatório do que está pronto, implementado sem validação completa e ainda pendente |
| [AMBIENTE.md](AMBIENTE.md) | Setup canônico `.venv`, execução, segurança do histórico e armazenamento de uploads |
| [CONTEXTO.md](CONTEXTO.md) | Arquitetura, funcionalidades, decisões e mapa de arquivos por tópico |
| [HISTORICO.md](HISTORICO.md) | Evolução, entregas, evidências e decisões substituídas |
| [PENDENCIAS.md](PENDENCIAS.md) | Trabalho restante, prioridades e critérios de conclusão |
| [VALIDACAO.md](VALIDACAO.md) | Verificações desta revisão e limites das evidências |
| [documentation-checks-2026-10-13.json](documentation-checks-2026-10-13.json) | Resultado estruturado da conferência de tarefas, links, specs e evidências |
| `specs/<capability>/spec.md` | Contratos consolidados das mudanças concluídas |
| `changes/gerenciamento-website/` | Planejamento e tarefas administrativas em andamento |
| `changes/corrigir-erros-operacionais/` | Correções de Git, ambiente e uploads; execução local sem Docker |
| `changes/recuperar-senha-codigo-6-digitos/` | Recuperação com seis dígitos, publicada e validada por camadas; entrega real do e-mail pendente |
| `changes/archive/2026-10-13-criar-modelo-dados-xano/` | Modelo de dados concluído: 37/37 tarefas |
| `changes/archive/2026-10-13-definir-fundacao-codeboxd/` | Fundação concluída: 87/87 tarefas |

## Situação das mudanças

| Change | Estado | Concluídas | Restantes | Critério |
| --- | --- | --- | --- | --- |
| `otimizar-performance-app` | Ativa | 11 | 26 | Inventário, cache/retry, fichas e busca validados localmente; implementação restante, medições, metas e integração completa pendentes |
| `criar-modelo-dados-xano` | Arquivada | 37 | 0 | Checklist histórico completo, evidências de persistência e validação documental |
| `definir-fundacao-codeboxd` | Arquivada | 87 | 0 | Busca Kitsu comprovada em setembro; marcador final corrigido e validação documental atual |
| `gerenciamento-website` | Ativa | 17 | 17 | Implementação local parcial/completa por tópico; integração remota e interface ainda não concluídas |
| `corrigir-erros-operacionais` | Concluída, aguardando arquivamento | 7 | 0 | Correções locais verificadas; Docker retirado do escopo pelo usuário |
| `recuperar-senha-codigo-6-digitos` | Ativa | 7 | 1 | Implementação publicada, conflito de campos corrigido e browser validado; chegada do e-mail em caixa controlada pendente |

A contagem administrativa anterior era 24/41 porque incluía sete itens H.1–H.7 de trabalho anterior. Eles foram preservados em [HISTORICO.md](HISTORICO.md), sem contar como implementação administrativa. Os 34 IDs administrativos originais permanecem estáveis.

## Como interpretar o estado

- **Concluída:** há evidência compatível com o critério original da tarefa. Ela pode ser histórica; a data e a camada estão documentadas.
- **Implementada localmente, validação pendente:** arquivos e testes simulados existem, mas falta a verificação real exigida. O checkbox continua aberto.
- **Arquivada:** o escopo original terminou e seus contratos foram sincronizados em `specs/`. Isso não garante disponibilidade contínua de provedores nem encerra melhorias posteriores.
- **Pendência transversal:** registrada em `PENDENCIAS.md`; não é incorporada silenciosamente a uma change arquivada.

## Rotina de retomada

Checkpoint de 14/10 para commit: [correção das buscas administrativas](changes/gerenciamento-website/validation/buscas-admin-2026-10-14.md).
Três endpoints corrigidos localmente, 18 testes admin passaram; publicação remota
da correção e teste com admin aprovado pendentes. Usuário pediu encerrar a sessão
para realizar o próprio commit; nenhum commit foi criado nesta rodada.

Por orientação do usuário, toda modificação no projeto deve ter vínculo e registro nesta pasta. A regra permanente está no `AGENTS.md` da raiz: identificar a change ou pendência relacionada e atualizar contexto, tarefas e evidências na mesma rodada. Arquivos de implementação continuam em seus diretórios próprios; a documentação de acompanhamento é centralizada no OpenSpec.

1. Ler os quatro documentos centrais e depois a proposta, o design e as tarefas da change ativa.
2. Conferir `git status --short` sem restaurar automaticamente arquivos de outras sessões.
3. Usar `.venv\Scripts\python.exe` para os comandos locais; ver AMBIENTE.md.
4. Consultar `openspec list --json` e `openspec status --change gerenciamento-website --json`.
5. Executar somente o trabalho autorizado, registrando data, camada, resultado e limitações da validação.
6. Atualizar tarefas e documentos centrais quando o estado mudar; não reescrever saídas históricas para fazê-las parecer recentes.

Artefatos completos no `openspec status` indicam planejamento completo, não implementação concluída. O checklist de tarefas e suas evidências determinam o encerramento.
