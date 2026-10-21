# Revisão para finalizar a otimização — 20/10/2026

Pedido atual: retomar a otimização e verificar implementação versus pendências.
Auditoria baseada nos checkboxes, código atual e evidências existentes; não
executa nova medição de desempenho nem encerra tarefas por inferência.

## Contagem conferida

**11/37 concluídas; 26 abertas.** IDs concluídos:
1.1, 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 4.3, 5.1, 5.2 e 6.1.
Isso mede critérios de tarefas, não percentual de ganho de velocidade.

## Implementado e evidência disponível

| Área | Código existente | Evidência e limite |
| --- | --- | --- |
| Sessão | Identidade de navegação por 15 s apenas para membro; guard/mutação validam novamente; cooldown por token | Testes de expiração, troca de token, desativação e falha transitória; não substitui autorização Xano |
| Leituras | Cache privado de 15 s, cópias, invalidação antes/depois de escrita e compartilhamento de leitura pendente por sessão/token/consulta/geração | Duas leituras simultâneas equivalentes usam uma chamada em teste; resultado de conta anterior não invalida sessão nova |
| Perfil/fichas | Conteúdo progressivo, falha parcial, guardas de visita/rota/conta/obra; avaliação aguarda restauração | Perfil real: dez visitas, nove chamadas, zero 429, oito revisitas sem chamada; não cobre todo o app |
| Catálogo/busca | Cache público de 300 s, queries/páginas distintas, relevância/deduplicação e descarte de resposta antiga | Testes locais e browser com fixtures; sem baseline completo de provedores reais |
| Biblioteca/listas | Pessoas removidas dos loaders; GET /library publicado, cursor e 20 itens/lote, retry/cooldown e preservação de cards | Biblioteca real com quatro itens em uma página; 250 itens apenas em fixtures. Listas ainda carregam referências/coleções integrais |
| Operação TMDB | App precisou ser relançado com rede autorizada; preflight de conectividade protege utilitários | Quatro endpoints reais 200/20 itens e três fileiras com 20 cards; não prova quota global ou performance integral |

Evidências principais: cache-concorrencia-cooldown-2026-10-20.md,
continuacao-fichas-busca-2026-10-20.md, biblioteca-paginada-xano-real-2026-10-20.md,
resultado-login-real-apos-cache-2026-10-20.md e tmdb-rede-restaurada-2026-10-20.md.

## O que falta, por IDs preservados

| IDs | Pendência para aceitação |
| --- | --- |
| 1.2–1.5 | Completar cenário/instrumentação/dados aprovados, baseline de cinco amostras por cenário, cache vazio/aquecido e desktop/celular, escopo da quota e metas numéricas. Origem de um 429 já foi vista em auth/me; escopo da quota ainda não foi comprovado. |
| 2.3–2.4, 3.5 | Cadastro/recuperação e navegação habitual reais, preservação de campos em falha, comparação após otimizar; manter entrega real de e-mail separada. |
| 4.1–4.2, 4.4 | Medir custo por provedor/caminho crítico da home, escolher incremento fundamentado, confirmar ordem/capas/fallback e comparação real por viewport/cache. Há melhorias históricas; não equivalem ao protocolo completo desta change. |
| 5.3–5.4 | Finalizar fluxo de avaliação com persistência real e comparar ficha/salvamento contra metas. Guardas, nota decimal, envio único e rascunho têm testes locais; não encerrar só por isso. |
| 6.2–6.4 | Paginação real com mais de 20 itens e duas contas, coleções grandes, listas públicas/privadas, diagnóstico/otimização de mutações e comparações. |
| 7.1–7.4 | Diagnosticar/medir outro perfil, seguidores, comunidade, feed e payload; concluir intervenções de leitura e posts/upload/likes/comentários com regressões, persistência e comparação. |
| 8.1–8.4 | Diagnóstico e otimização administrativa com admin aprovado, contagens/filtros/páginas/mutações/auditoria e rejeição de membro/visitante/desativado. Código administrativo existente não significa desempenho aceito. |
| 9.1–9.3 | Jornada integral, orçamento aprovado, comportamento habitual com 429 controlado e relatório final de todas as rotas. Depende das etapas anteriores. |

## Situação operacional encontrada nesta retomada

A correção paralela de texto obrigatório está na change
exigir-texto-denuncias-avaliacoes, não foi somada à contagem de performance.
Suíte atual: **269 testes aprovados e compile --dry aprovado**. O teste novo
de navegador não iniciou casos: build de produção falhou no prerender de /
com timeout. A restauração subsequente também falhou; normal_restored=false.

Isso demonstra uma verificação que ainda faltava: compilar componentes e
responder HTML em rodada anterior não garante exportação completa estável.
Durante o diagnóstico havia servidor de desenvolvimento separado ativo; ele
foi preservado. Observou-se pouca memória disponível, sem concluir causalidade
entre memória, concorrência de builds e timeout.

Foi autorizada tentativa de recuperar a porta 3030 em produção com
REFLEX_SSR=false somente no ambiente do subprocesso, sem mudar rxconfig ou .env.
Essa tentativa também falhou na exportação: mesmo em modo SPA, React Router
renderiza a entrada / e voltou a atingir timeout. O smoke de /login em 3030
terminou com conexão recusada. **A porta normal 3030 não foi recuperada nesta
retomada.** Nenhuma configuração permanente de SSR foi alterada; o servidor de
desenvolvimento separado foi preservado. Não usar a tentativa como medição de
performance nem repetir restauração como se tivesse passado. Evidência nos logs
normal-restored-after-continuation.log e normal-recovery-no-prerender.log.

## Sequência recomendada para conclusão

1. Estabilizar build/restauração e fixar ambiente de medição, preservando o
   servidor do usuário e evitando concorrência no frontend gerado.
2. Medir jornadas com cache vazio/aquecido, cinco amostras, por serviço, e obter
   metas explícitas. Começar por rotas públicas enquanto não houver contas.
3. Completar biblioteca/listas com coleção grande e duas contas controladas;
   medir antes de mudar mutações ou contrato.
4. Completar social e administração com contas aprovadas e dados rastreáveis.
5. Executar jornada integral e reconciliar evidências/specs antes de arquivar.

Contas locais de teste aprovadas não foram encontradas no caminho dos scripts
históricos; não criar contas, conceder admin ou extrair senhas antigas para
marcar tarefas. Restam implementação e comprovação, não apenas documentação.
