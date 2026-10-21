# Design

## Context

Ver motivação e escopo em [proposal.md](proposal.md). Reflex 0.9.11.post1 mantém
estados no servidor Python; Xano autentica e persiste dados; TMDB, Kitsu e Open
Library atendem catálogo. DeepL pode participar das descrições. A identidade
Jikan legada permanece mapeada; `titulos` não se confunde com `media`.

Evidências históricas, não medições desta rodada:
- [Home](../../validation/carregamento-home-2026-10-20.md): primeira visita até
  categorias disponíveis de 26,42 s para 15,32 s; recarga de 9,40 s para 1,43 s.
  São amostras locais, não percentis ou referência universal.
- [Leituras sociais](../../validation/requisicoes-navegacao-2026-10-20.md): cache
  privado de 15 segundos, 174 testes e compilação; sem confirmação de redução
  de 429 no navegador autenticado. Não será ampliado sem verificar invalidação.
- O relato atual de 20 segundos não identifica endpoint, origem ou quota.

Nesta rodada serão validados somente os artefatos de planejamento.

## Goals / Non-Goals

**Goals:** localizar o custo real de cada jornada, priorizar o caminho crítico,
reduzir chamadas redundantes e preservar consistência e acesso protegido.

**Non-Goals:** refatoração ampla sem gargalo medido, alteração de funcionalidades,
cache de autorização como atalho, troca de provedores ou infraestrutura nova.

## Decisions

### 1. Medir antes de escolher a correção

Usar `.venv` e servidor local em produção, conforme skills Reflex. Registrar
commit/diff, portas efetivas, ambiente, viewport, perfil de rede, tamanho dos
dados, papel da conta, cache vazio/aquecido e versão do cenário. Separar tempo
de compilação/inicialização do tempo de uso. Capturar chamadas do navegador e
do Python aos provedores: o painel de rede do navegador sozinho não mostra
todo o tráfego ao Xano. Sanitizar endpoints e excluir credenciais e conteúdo.

Para cada cenário: ao menos cinco amostras comparáveis, valores individuais,
mediana e pior amostra; não chamar isso de p95 representativo. Medir navegação
até conteúdo principal utilizável, resposta visual à ação, confirmação de
gravação, contagem de chamadas/tentativas por serviço, 429 e bytes quando
disponíveis; incluir LCP/INP/CLS quando tecnicamente mensuráveis e úteis.

Depois da linha de base, propor orçamento por jornada e pedir aprovação antes
de registrá-lo. Não inventar promessa global de dois segundos para provedores
externos. Encerrar somente contra metas aprovadas e evidência comparável.
Alternativa descartada: otimizar por percepção isolada sem contagem de chamadas.

### 2. Aprovação por intervenção

Antes de editar, apresentar diagnóstico, arquivos, motivo, efeito esperado,
riscos, testes e rollback; aguardar aprovação explícita. Uma aprovação cobre
somente a intervenção descrita, seus testes e os registros documentais
explicitamente incluídos no pedido. Mudança de abordagem exige nova aprovação.
Leitura e diagnóstico sem mutações podem continuar; scripts, logs persistidos,
contas/dados de teste, reinícios e operações remotas entram no pedido aplicável.

### 3. Trabalhar do login à administração

| Etapa | Jornada e casos mínimos |
| --- | --- |
| A | Login, erro de credenciais, sessão persistida/expirada, logout, cadastro e recuperação |
| B | Home, categorias, busca mista, mais resultados, retorno e cache vazio/aquecido |
| C | Fichas internas/externas nos quatro tipos, troca rápida de obra, trailers, relacionados e streaming |
| D | Avaliar/editar, biblioteca, listas públicas/privadas, itens e atalhos |
| E | Próprio perfil e outro perfil, seguidores, comunidade, feed, posts, upload, comentários e curtidas |
| F | Login admin, dashboard, usuários, catálogo por tipo, reports e demonstração |

Confirmar subfluxos existentes no inventário de rotas, componentes e handlers;
a tabela é cobertura mínima, não autorização para excluir telas descobertas.
Cada etapa repete: medir, propor, aprovar, implementar, verificar e documentar.
Admin depende de conta aprovada; ausência de acesso mantém tarefa aberta.

### 4. Gerir tráfego sem reduzir garantias

Incremento local posterior, autorizado na continuação de 20/10: compartilhar
apenas leituras sociais equivalentes em andamento por nonce de sessão, geração
e digest da consulta, fora do estado serializado. Preservar TTL, invalidação e
cópias; não compartilhar mutações. Fixar credencial por leitura paginada e
rejeitar troca antes/durante a tarefa. GET legado que envia e-mail não é leitura
segura para retry; aplicar cooldown local após 429 ao pedido normalizado.
Catálogo passa a interpretar datas HTTP de Retry-After pelo parser comum,
encerrando tentativa quando a espera excede o limite em vez de antecipá-la.
Sem cooldown global ou promessa de deduplicação entre processos.
[Decisões e evidência](validation/cache-concorrencia-cooldown-2026-10-20.md).

Decisão incremental aprovada em 20/10 após reproduzir 429 em `/auth/me`:
reutilizar identidade de membro já verificada por até 15 segundos apenas nos
loaders de leitura, vinculada a hash do token, usuário e sessão. Guards admin
e ações protegidas continuam pedindo validação fresca; nenhuma resposta local
autoriza uma gravação no Xano. Informação de conta na navegação pode ficar
até 15 segundos atrás de mudança externa, conforme limite aprovado pelo usuário.
Identidade administrativa não participa dessa reutilização, inclusive na
navegação. Sucesso verificado no login pode atender a primeira visita ao perfil.

GET `/profiles/<id>` entra no cache privado existente de 15 segundos, com
invalidação antes/depois de mutações e em respostas 401/403. Um contador de
geração impede leitura iniciada antes de uma gravação de repovoar o cache após
a invalidação. Dados já renderizados por resposta tardia continuam sujeitos
às verificações de rota/token de cada loader; não confundir as duas garantias.

429 na validação registra cooldown por hash do token no estado da sessão;
nenhuma nova consulta a `/auth/me` ocorre nesse escopo até o prazo expirar.
Não estender esse bloqueio ao Xano inteiro sem conhecer a quota. Falha
transitória preserva token e identidade, remove papel privilegiado e exige
nova verificação após o prazo. Caminho de fallback social preexistente para
falhas transitórias permanece: eventual gravação continua sujeita à autorização
do próprio endpoint Xano. Testes locais não substituem revisão remota desse contrato.

Investigar duplicação de eventos e leituras, paginação que carrega tudo, N+1,
criação/reparo de listas na navegação, chamadas de sessão, conexões HTTP e
concorrência por provedor. Aplicar só as intervenções justificadas pelos dados.
Paginar na origem quando suportado, preservando acesso a todos os resultados;
não reduzir silenciosamente listas, estatísticas ou busca para parecer rápido.

Cache público só para dados públicos. Cache privado limitado por sessão,
credencial, consulta e paginação, com expiração, cópias e invalidação por
gravação/troca de conta. Deduplicar apenas leituras equivalentes. Manter
autorização no servidor, detecção de conta desativada e invalidação 401/403.

Investigar 429 por serviço e contexto; respeitar Retry-After inclusive data HTTP,
limitar retries e concorrência e impedir ações repetidas no cooldown aplicável.
Escopo do cooldown depende do limite confirmado: não bloquear o aplicativo
inteiro presumindo que toda quota é global. Não repetir automaticamente login,
recuperação, uploads e mutações, inclusive endpoints GET com efeitos colaterais.
Alternativas descartadas: ocultar aviso, aumentar retries ou ampliar cache global
de dados privados. Alterar Xano/quota exige aprovação específica e verificação.

### 5. Priorizar conteúdo utilizável

Incremento posterior em 20/10: `_media_updates` publica a ficha antes dos
complementos; editor pessoal só aparece depois de restaurar a avaliação.
Guardas de geração/rota/token/obra cobrem respostas tardias e a geração da nota
impede leituras antigas de reverter uma gravação. Busca pública TMDB/Open Library
passa a usar o cache existente de 300 s/128 entradas, com consulta e página na
chave; Kitsu mantém cache próprio. Sem alterar identidade Jikan, tradução,
notas antigas ou contratos remotos. [Evidência](validation/continuacao-fichas-busca-2026-10-20.md).

Separar dados principais e complementares, limitar custo de imagens e estado
sincronizado quando medido, e apresentar carregamento/erro por seção. Ao trocar
rota/obra/consulta, cancelar ou ignorar resultados antigos. Não exibir dados
de outra identidade nem deixar controles permanentemente bloqueados.
Evitar adicionar bibliotecas antes de verificar recursos existentes.

## Risks / Trade-offs

Incremento da biblioteca aprovado em 20/10: preparar localmente GET `/library`
autenticado com join de mídia e cursor por ID da interação, 20 itens por lote
e lookahead de 21 para `has_more`. Cliente valida/aplica lote atomicamente,
preserva cards em falha e descarta respostas fora da conta/rota/credencial.
Não exibe total global nem baixa catálogo inteiro. Flag
`LIBRARY_PAGINATION_ENABLED=false` mantém comportamento legado por padrão;
publicação, verificação remota do contrato/autorizações/join e ativação são
etapas separadas. Sem snapshot global: novas inclusões podem aparecer na
continuação; exclusões anteriores não deslocam o cursor. Rollback por flag
desligada e reinício aprovado, sem alterar dados. [Contrato, testes e limites](validation/biblioteca-paginada-local-2026-10-20.md).

- Cache obsoleto ou entre contas → expiração, limites, invalidação e regressões.
- Concorrência excessiva ou retries sincronizados → limites por serviço e cooldown fundamentado.
- Paginação altera contratos → conferir API real; propor mudança remota separadamente.
- Provedor lento distorce ganho local → separar tempos e registrar falha/degradação.
- Gravação otimista mostra sucesso falso → confirmar persistência e preservar rascunho.
- Melhorar desktop piora celular → comparar ambos com os mesmos cenários.
- Otimizações interferem em changes ativas → preservar IDs e contratos e registrar dependências.

## Migration Plan

Sem migração ou publicação nesta fase. Implementação futura em incrementos
aprovados, com testes pertinentes e compilação; reinício explicitamente incluído
na aprovação para testar a versão correta. Não iniciar Docker.

Rollback por intervenção: reverter somente seus trechos, preservar dados,
uploads e trabalho anterior; invalidar caches afetados; registrar comparação.
Se houver contrato remoto, exigir plano próprio com backup, delta, publicação
aprovada e validação; arquivo local/dry-run não comprova publicação.

## Open Questions

- Qual endpoint/quota origina o 429 observado? Será identificado na linha de base.
- Quais tempos e volumes cada jornada apresenta no ambiente controlado?
  As metas numéricas serão propostas após essa medição, antes das correções.
- Quais contas de teste/aprovações estarão disponíveis para validação remota
  e admin? Registrar indisponibilidade, sem conceder privilégios automaticamente.
