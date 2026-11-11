# Pendências atuais — 27/10/2026

11/11/2026 — [UI/UX: primeiro lote local após aprovação](changes/modernizar-ui-ux-codeboxd/validation/fundamentos-carrosseis-2026-11-11.md):
3/26 tarefas, com baseline Home/login/ficha, tokens e piloto de contraste,
carrossel comum de mouse/teclado/toque nativo na Home e recomendações. Toque
validado por emulação, não por aparelho físico; carregar mais/falha de capa,
shell, busca/listas, outras famílias e aceite transversal seguem abertos.
Cloudinary permanece separado, sem ativação ou escrita remota nesta continuação.
Não transferir os 632 testes da branch Cloudinary para este lote: a base desta
branch de UI tem sua própria suíte e evidências no relatório. Sem push/merge.

Registro histórico da etapa de planejamento, anterior à aprovação e ao lote acima:

11/11/2026 — [Duas frentes planejadas para aprovação](planning/cloudinary-uiux-2026-11-11.md):
Cloudinary mantém 2.1/2.2 abertas, com reserva durável, persistência e limpeza
supervisionada especificadas (marcos originais 3/5, checkpoints 3/17). UI/UX nova
0/26: tokens/contraste/navegação, prateleiras arrastáveis e busca por Obras,
Pessoas e Listas públicas, com privacidade no servidor. Atividade de lista no
feed não reproduzida no código local, sem remoção proposta por suposição.
Aguardar aprovação das duas changes antes de implementar. Xano, limpeza real
e ativação exigem autorizações específicas posteriores. Nenhum aceite funcional
novo, commit, push, merge ou mudança no trabalho local de performance.

11/11/2026 — [Homologação preparada localmente, obtenção remota recusada](changes/preparar-homologacao-xano-admin/validation.md):
4/8, pacote 32 documentos/573 testes. Sandbox HTTP 500; criação de workspace vazio
HTTP 403/ERROR_CODE_ACCESS_DENIED, nome ausente após tentativa. A conta/credencial
atual não permite a obtenção; motivo plano/permissão não confirmado. Proprietário
deve verificar painel/permissões ou disponibilizar instância isolada. Sem compras,
publicação de contratos, alteração da origem ou piloto administrativo executado.

11/11/2026 — Usuário escolheu homologação para o piloto administrativo.
[Descoberta atual e limite de acesso](changes/gerenciamento-website/validation/piloto-mutacoes-2026-11-11.md):
um perfil configurado, somente workspace 147717 acessível; destino isolado não
identificado. Solicitar identificação/configuração de homologação ou planejar
criação vazia em escopo próprio antes de qualquer provisão. Não usar live como
fallback. Administração 33/34; nenhuma escrita executada.

11/11/2026 — [Piloto administrativo preparado offline](changes/gerenciamento-website/validation/piloto-mutacoes-2026-11-11.md):
25 registros propostos, retenção de 16 e nove candidatos próprios à limpeza;
583 testes locais passaram. Pré-voo atual: uma branch live e uma fonte, sem
isolamento adicional demonstrado; exclusões/cascatas ainda não confirmadas.
Decidir destino e verificar limpeza antes de seed; nenhum registro criado,
alterado ou excluído. 9.2 preservada em 33/34; plano completo de 239 não reduzido.

11/11/2026 — [Leituras administrativas integradas aprovadas](changes/gerenciamento-website/validation/resultado-leituras-2026-11-11.md)
em desktop/celular, sem alterações remotas administrativas. A tarefa 9.2 continua
33/34 por exigir mutações, auditoria e permissões integradas sobre fixtures
controladas; A2–A4 continuam sem autorização específica. Não repetir os cenários
de leitura aprovados sem regressão ou nova necessidade.

11/11/2026 — [Confirmação manual posterior](changes/recuperar-senha-codigo-6-digitos/validation/aceite-usuario-2026-11-11.md):
usuário recebeu código, trocou senha e entrou com a nova. Essa confirmação supera
a falta de recebimento inicial; não fecha replay/restauração, comparação de
latência ou alinhamento do remetente. Checklists funcionais preservados.

11/11/2026 — [Bloqueio de entrega confirmado no ensaio atual](changes/melhorar-email-recuperacao/diagnostico-entrega-2026-11-11.md):
SendGrid processing, cinco adiamentos 421/4.7.32, sem delivered. Usuário sem
código; nenhuma troca de senha até o diagnóstico. Aguardar domínio próprio/DNS
e autorização de configuração, sem reenviar para contornar a causa. Changes de
e-mail/recuperação continuam abertas; nenhuma entrega ou comparação comprovada.

11/11/2026 — Preparação do executor de dois códigos concluída localmente:
[testes, limites e escopo do ensaio](changes/recuperar-senha-codigo-6-digitos/validation/executor-dois-codigos-2026-11-11.md).
O bloqueio técnico da restauração por sessão comum foi removido do executor;
faltam autorização específica, conta/caixa controlada e aceite real. Recuperação
mantida 9/11 e SendGrid 4/5. Sem envio ou alteração remota.

11/11/2026 — [Critérios de aceite e sequência recomendada](changes/integrar-sendgrid-recuperacao/aceite-2026-11-11.md):
SendGrid 4/5, experiência do e-mail 4/5 e recuperação 9/11. Remetente verificado,
zero domínios autenticados confirmados por GET. Falta ciclo na caixa controlada,
restauração compatível com credencial exclusiva e comparação real de entrega.
3.4 Resend requer reconciliação com SendGrid, preservando histórico/ID. develop
remota `29d0456`, main remota `42ff4dd`; PRs #31/#32 já integradas. Nada fechado.

10/11/2026 - Auditoria Git e branch de integracao publicada; PR ainda aguarda criacao autenticada. [Registro e link do PR](changes/otimizar-performance-app/validation/integracao-develop-2026-11-10.md). `origin/develop` em 4a7cabe; administracao 33/34 e performance 17/37 preservadas. Branch `pedro` mantida por conter documentacao historica obsoleta; P0 movel ainda sem evidencia suficiente. Nenhuma tarefa foi fechada.

09/11/2026 — [relatório consolidado do projeto](changes/gerenciamento-website/validation/relatorio-projeto-2026-11-09.md):
administração 33/34, performance 17/37 e recuperação 8/10, 23 tarefas abertas.
Executor administrativo ensaiado somente em memória: 22 testes novos e 26
regressões aprovados, journal e releitura após PUT simulados. Nenhum acesso Xano
nesta rodada. Homologação integrada continua pendente de destino, preparação de
setup/limpeza e autorização específica A2–A4; nenhuma tarefa encerrada.

09/11/2026 — continuação local da administração: [guardas de prévia offline](changes/gerenciamento-website/validation/guardas-locais-2026-11-09.md)
com 26 testes aprovados. Bloqueiam destino/ator/ID divergentes, alterações não
aprovadas, cancelamento e métodos fora do escopo. Sem transporte ou chamadas
Xano; setup/limpeza e integração das guardas ainda não executados. Definir destino
e obter A2–A4 antes de escrita; nenhuma fixture real aprovada. 9.2 segue 33/34.

09/11/2026 — após autorização de login/leitura A1, a conta admin existente foi
autenticada e acessou dashboard, usuários, catálogo e reports pela API:
[dez checks aprovados](changes/gerenciamento-website/validation/login-e-leituras-a1-2026-11-09.md),
sete respostas 200 (um POST de autenticação e seis GET). Sem mutações
administrativas. Isso não equivale ao aceite do fluxo completo da UI; 9.2
continua aberta, 33/34. A2–A4 permanecem sem autorização. As pendências de A1
registradas abaixo descrevem o estado anterior ao login desta continuação.

09/11/2026 — retomada administrativa posterior à atualização de contexto:
[inventário A0 autorizado e executado](changes/gerenciamento-website/validation/pre-voo-a0-2026-11-09.md).
Sete GET 200 no workspace 147717, zero mutações. Branch v1/live e fonte live;
nenhum isolamento existente ou candidato a fixture confirmado para reuso.
Há oito contas ativas (uma admin), 23 obras e cinco reports, todos somente lidos.
A1–A4 continuam pendentes, assim como contratos/cascatas/quota para escrever.
Administração segue 33/34. O registro anterior de contexto descreve sua própria
rodada, quando não houve acesso Xano; o inventário administrativo foi posterior.

09/11/2026 — estado conferido no GitHub: [PR #28](https://github.com/vitordeev/Codeboxd/pull/28)
foi integrado a develop em 05/11, merge a21c806. Administração continua **33/34**:
merge não conclui 9.2 nem autoriza A0–A4. Performance **17/37**, com 20 tarefas
abertas; iniciar por baseline/metas (1.3/1.5), antes de novas otimizações.
[Comparação Git, preservação e plano de retomada](changes/otimizar-performance-app/validation/retomada-2026-11-09.md).
Nenhum commit, teste integrado ou acesso Xano nesta atualização.

09/11/2026 — análise retomada e consolidada, sem otimizações: [diagnóstico e plano técnico para revisão](changes/otimizar-performance-app/validation/diagnostico-plano-performance-2026-11-09.md). 36 navegações reais preservadas (20 Home +16 leituras de membro); oito novas em 390 px. Metas propostas, não aprovadas; performance 17/37, administração 33/34. Processos de medição encerrados.


09/11/2026 — análise de performance pausada por solicitação do usuário. [Contexto, 28 amostras reais e retomada](changes/otimizar-performance-app/validation/pausa-analise-2026-11-09.md). Home em 1440/390 e leituras desktop de membro; critérios incompletos preservados. Processos de medição encerrados, sem otimizações ou escritas administrativas. Performance 17/37; administração 33/34.

05/11/2026 - Aplicacao atualizada em producao local (3030), sem Docker. 494 testes locais, 34 etapas reais desktop/celular e remocao na interface atualizada aprovados; dados descartaveis limpos. Performance 17/37, administracao 33/34 e recuperacao 8/10: **23 tarefas funcionais abertas**. Capa/sinopse mobile corrigida, validada em 20 cenarios e [arquivada](changes/archive/2026-11-05-corrigir-capa-sinopse-mobile/validation.md). [Evidencias e limites desta rodada](changes/otimizar-performance-app/validation/conclusao-2026-11-05.md). Resend: chave restrita ao envio; 401 ao listar dominios nao prova chave invalida. Recebimento/ciclo real de recuperacao continuam pendentes.

05/11/2026 — preparação documental da homologação integrada 9.2:
[plano e autorizações A0–A4](changes/gerenciamento-website/design.md#plano-de-homologação-integrada-da-92--preparado-em-05112026).
Preferir destino isolado; disponibilidade atual ainda não inventariada. Proposto
lote próprio com teto de 26 contas member, 104 obras, 30 reports e um post,
além dos efeitos de signup/auditoria; preservar eventos e referências na limpeza.
Executores históricos de escrita/limpeza não estão liberados para reuso como
estão. Nenhum teste integrado ou acesso remoto executado nesta preparação.
Aprovação de destino, dados, mutações e limpeza/retenção é condição para executar.
Change mantida em 33/34, sem conclusão ou arquivamento.

05/11/2026 — continuação exclusiva da administração 9.2: executor sincronizado
com resposta e renderização; Reports com dados reais carregado em 1440/390.
Feedback de erros encoberto pelos modais foi identificado, documentado e
corrigido, com regressão local. As modalidades e critérios por cenário estão na
[continuação do aceite](changes/gerenciamento-website/validation/continuacao-9-2-2026-11-05.md).
Manter 33/34 enquanto houver critério obrigatório de aceite integrado sem
evidência; não confundir fixtures com novas mutações no Xano. Registros abaixo
preservam seus estados históricos.

Resultado da continuação: 68 cenários distintos aprovados com fixtures e dois
casos reais de renderização de Reports; 44 cenários revalidados após corrigir
feedback nos modais. [Matriz detalhada](changes/gerenciamento-website/validation/matriz-9-2-2026-11-05.md).
Falta homologação da UI integrada ao Xano nos fluxos de alteração e na matriz
completa de permissões, com contas/alvos descartáveis e escrita/limpeza definida.
Nenhuma mutação remota foi executada; 9.2 continua aberta, administração 33/34.

04/11/2026 - Conexoes/feed/listas concluida (10/10), specs sincronizadas e
change [arquivada](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/conclusao-2026-11-04.md).
Dashboard administrativo publicado e validado: administracao 33/34,
performance 14/37 e recuperacao 8/10. Restam 26 tarefas funcionais;
os registros datados anteriores preservam seus respectivos estados.
Scaffold corrigir-follow-feed-status-filmes arquivado como supersedido,
sem nova entrega funcional. OpenSpec global: 22/22 validos.


Encerramento de 03/11/2026 a pedido do usuário: [evidências para Git](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/encerramento-2026-11-03.md).
Conexões/listas **9/10**, backend publicado, migração e limpeza aprovadas.
3.2 continua aberta pelo aceite visual; HTTP direto de rota dinâmica retornou
404 no servidor local de produção. Nenhuma correção de roteamento realizada.
São **38 tarefas funcionais abertas** nesta configuração de checklists.
As contagens de 40 abaixo são do estado anterior ao corte concluído.

Continuação de 03/11/2026: [contratos implementados e implantação preparada](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/implantacao-2026-11-03.md).
Conexões/listas **7/10**: prévia remota de 15 documentos e 477 testes aprovados;
backup, plano e pacote de rollback preparados. Sem publicação ou migração.
Plano gratuito recusou branch/fonte isolada; aguarda escolha de ambiente de
ensaio. Com três tarefas novas detalhadas e uma concluída, há **40 tarefas
funcionais abertas**; os registros históricos de 38 são da conferência anterior.

Conferência de 03/11/2026: [relatório remoto/local](changes/archive/2026-11-04-auditar-estado-remoto-changes-abertas/report.md).
Contrato novo de status ainda ausente no workspace, embora default_key histórico
exista. Flags efetivas de biblioteca paginada e identidade padrão false em
processo novo. Admin e Resend têm contratos presentes; efeitos reais continuam
pendentes. O acesso administrativo de leitura funcionou nesta sessão, superando
a limitação anterior de acesso, sem autorizar implantação. Contagens funcionais
preservadas; scaffold corrigir-follow-feed-status-filmes falha por falta de planejamento.

Atualização de 30/10/2026: [estado completo das changes](RELATORIO_CHANGES_2026-10-30.md).
As quatro entregas locais completas foram arquivadas; conexões/feed/listas
permanece **6/7**, aguardando aplicação manual Xano. Recuperação **8/10** precisa
de destinatário elegível e caixa controlada; administração **22/34** e performance
**14/37** mantêm seus critérios. Credenciais não substituem implementação e evidência.

Busca administrativa publicada e validada: tarefa 3.1 concluída, 79 checks reais
aprovados; administração agora **22/34**. [Entrega e limites](changes/gerenciamento-website/validation/busca-parametros-2026-10-27.md).

## Listas — concluídas e arquivadas

Change [corrigir-duplicacao-listas-padrao](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/tasks.md): **11/11 tarefas concluídas**. Coleção própria separada, descoberta agrupada por autor com nome à direita do avatar, preparação idempotente publicada no Xano e 16 identidades legadas atribuídas. 411 testes, compilação/build, 18 checks API e 14 critérios de navegador com duas contas reais comprovados. Conta e registros descartáveis removidos; 19 listas e 8 vínculos originais preservados, zero duplicatas/conflitos. [Conclusão e evidências](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/validation/conclusao.md).

Quatro requisitos sincronizados nas specs principais e change arquivada em 26/10/2026 por solicitação do usuário. Limite de chamadas em navegação rápida continua no escopo de performance; validação funcional final foi espaçada conforme a evidência. As três changes funcionais abaixo mantêm suas pendências e contagens.

## Changes funcionais abertas

| Change funcional ativa | Concluídas | Abertas | Critérios restantes |
| --- | ---: | ---: | --- |
| [gerenciamento-website](changes/gerenciamento-website/tasks.md) | 33/34 | 1 | Aceite completo da interface no navegador real |
| [otimizar-performance-app](changes/otimizar-performance-app/tasks.md) | 17/37 | 20 | Metas das demais jornadas, comparações completas, mutações, duas contas e browser real |
| [recuperar-senha-codigo-6-digitos](changes/recuperar-senha-codigo-6-digitos/tasks.md) | 8/10 | 2 | Envio Resend aceito, chegada na caixa e ciclo completo de recuperação |

As contagens vêm dos checklists, não medem o percentual global do produto.
As três changes têm planejamento completo; isso não significa implementação concluída.

Evidências mais recentes:

- [Performance e conexões Xano, 24/10](changes/otimizar-performance-app/validation/conexoes-xano-2026-10-24.md): 374 testes históricos, compile/build e comparação de leituras reais; não comprova a jornada inteira.
- [Leituras de admin e membro, 23/10](changes/otimizar-performance-app/validation/retomada-conclusao-2026-10-23.md): 44 e 70 checks, respectivamente; não substituem testes de mutações e navegador administrativo.
- [Administração, 22/10](changes/gerenciamento-website/validation/retomada-evidencias-2026-10-22.md): 21/34; interface local com fixtures e reports documentados.
- [Recuperação/Resend, 22/10](changes/recuperar-senha-codigo-6-digitos/validation/resend-integracao-2026-10-22.md): integração publicada; destinatário testado rejeitado pelo remetente de testes, sem entrega comprovada.

## Critérios administrativos restantes

Registro historico de 27/10: Os 12 IDs abertos são 2.1–2.3, 3.2–3.3, 4.1–4.2, 5.2–5.4 e 9.1–9.2.
Em 04/11, apos 119 checks reais aprovados, resta somente 9.2.
[Evidencias atuais](changes/gerenciamento-website/validation/aceite-2026-11-04.md).
Telas/contratos já existem; falta completar os critérios reais indicados no checklist.
5.1 e 5.5 estão concluídas; 6.2/6.3 tiveram validação local com fixtures.
As leituras admin reais de 23/10 eliminam a antiga afirmação de que nunca houve
acesso admin, mas não comprovam suspensão/reativação, decisões, auditoria,
integridade dos alvos e jornada completa no navegador.

## Pendências transversais — fora das mudanças arquivadas

Esses itens são inventário para próximas changes ou correções autorizadas. Não representam entrega já concluída nem aumentam a contagem administrativa.

| ID | Prioridade | Tópico e situação | Critério de conclusão |
| --- | --- | --- | --- |
| P.1 | Resolvida na cobertura auditada | TMDB rotacionado e exposto revogado; quatro senhas substituídas, quinta conta ausente; sessões anteriores revogadas por política publicada; prevenção e navegador validados | Evidências nas changes proteger-credenciais-expostas (9/9) e revogar-sessoes-apos-troca-senha (6/6). Histórico preservado; scanner heurístico e cobertura documentados, sem garantia sobre fontes não examinadas |
| P.2 | Resolvida localmente | `.venv` instalada e canônica; dependências diretas fixadas; pip check, 113 testes e compilação passaram | Comandos em [AMBIENTE.md](AMBIENTE.md); `venv` anterior preservada |
| P.3 | Alta antes de hospedar | URL concreta de banner corrigida/testada; execução e armazenamento locais, sem Docker | Manter backup do diretório de uploads; escolher persistência para hospedagem quando essa etapa for solicitada |
| P.4 | Resolvida | Mensagens de erro de upload corrigidas e verificadas | Testes de rede, HTTP e JSON inválido passaram |
| P.5 | Resolvida em 14/10/2026 | Contrato multipart e preservação do rascunho/cancelamento corrigidos; browser real validado | Criar/editar/recarregar, rejeitar inválido e cancelar passaram; posts, arquivos staged e blobs de teste limpos. Evidência em `validation/uploads-and-session-2026-10-13.md` |
| P.6 | Bloqueada na entrega real | Código de seis dígitos implementado/publicado com 15 minutos, cinco tentativas, cooldown e uso único; fluxo de senha verificado no Xano | Confirmar chegada do e-mail e fluxo com caixa controlada. Change `recuperar-senha-codigo-6-digitos`; integração Resend publicada em 22/10, destinatário não elegível para o remetente de testes. Ver evidência Resend na tabela acima |
| P.7 | Média | `/likes` remoto ausente no último registro | Revalidar contrato remoto; manter fallback ou publicar rota após revisão; verificar curtidas sem N+1 |
| P.8 | Resolvida para retomada | Checkpoints atuais de `docs/` apontam para OpenSpec; histórico anterior preservado | Novas alterações continuam centralizadas no OpenSpec |
| P.9 | Conforme crescimento | Estado e páginas sociais concentram muitas responsabilidades | Separar por domínio quando houver necessidade concreta, mantendo rotas/eventos e testes relevantes |
| P.10 | Fora da etapa atual | Publicação/domínio/HTTPS ainda não validados; Docker excluído por decisão do usuário | Definir hospedagem somente quando solicitada; operação atual local com `.venv` |
| P.11 | Antes de reusar validações | Scripts históricos têm caminhos anteriores ao arquivo e portas fixas | Copiar/adaptar scripts para nova pasta de resultados; preservar arquivo histórico e não criar contas incidentalmente |
| P.12 | Publicada em 19/10; validação funcional parcial | Três GETs corrigidos publicados após backup de 77 documentos e delta limitado; dry-run final sem mudanças. 18 testes locais passaram; visitante 401 e membro 403 confirmados | Validar buscas, caixa, vazio, filtros e paginação com admin aprovado e interface no navegador. Leituras admin reais posteriores registradas em 23/10; mutações e browser completo continuam pendentes. [Evidência](changes/gerenciamento-website/validation/publicacao-buscas-admin-2026-10-19.md) |

Atualização P.6 em 28/10: os testes locais de recuperação/cooldown passaram
(24 testes); a documentação oficial confirma a restrição do remetente de teste.
Nenhuma chamada ou troca real executada. 3.2/3.4 continuam abertas até envio
aceito a uma caixa elegível e ciclo/restauração controlados. [Evidências e próximo passo](changes/recuperar-senha-codigo-6-digitos/validation/elegibilidade-resend-2026-10-28.md).


## Ajustes visuais e entregas encerradas

Atualização da P.1 em 26/10/2026: a change arquivada
[proteger-credenciais-expostas](changes/archive/2026-10-26-proteger-credenciais-expostas/tasks.md)
inventariou o histórico e comprovou a rotação TMDB: novo token aceito (200),
exposto rejeitado (401), aplicação recarregada e catálogo aprovado no navegador.
Quatro senhas de teste substituídas (novas aceitas/antigas rejeitadas); quinta
senha histórica já rejeitada. Dois tokens históricos retornam 401. Verificador
de segredos adicionado, testes sintéticos aprovados e ignore reforçado.
Na continuação autorizada, a dependência revogar-sessoes-apos-troca-senha publicou
e comprovou a revogação em 39 rotas protegidas: 29 checks remotos, 392 testes
locais e navegador autenticado aprovados. A quinta identidade foi confirmada
ausente por metadados, sem remoção nesta rodada. Tarefa 2.3 concluída; P.1
resolvida na cobertura auditada, sem reescrita do histórico. As pendências de
entrega de e-mail e das outras changes funcionais permanecem independentes.
As duas changes de segurança foram arquivadas nesta data; os seis requisitos
foram sincronizados nas especificações principais. Novas evoluções exigem change ativa.
Evidência: [validação](changes/archive/2026-10-26-proteger-credenciais-expostas/validation.md).

- P.13 — Retorno à descoberta: resolvido localmente em 19/10, com compilação e checks de navegador. [Evidência](validation/voltar-descoberta-2026-10-19.md).
- Sobreposição da capa de livro com sinopse em 390px: pendência visual preservada, sem correção nesta revisão; exige change ativa específica antes de implementação.
- Meias estrelas: 5/5, sincronizadas e arquivadas em 21/10.
- DeepL: 6/6, quatro cenários reais de navegador e arquivamento em 21/10; não é mais pendência de ativação.
- Feed/listas: 6/6, arquivadas em 22/10; navegador desta entrega usou fixtures, sem nova integração autenticada Xano.

## Fora da etapa atual

Hospedagem, domínio/HTTPS, Docker, chat, notificações e recomendações por aprendizado
de máquina. Reports de mensagem por snapshot não representam mensageria implementada.

## Encerramento

Marcar tarefa somente com evidência do critério. Validar, sincronizar deltas concluídos
e arquivar quando não houver critérios pendentes. Nenhuma das três changes funcionais
atende hoje esse critério. Preservar IDs e históricos; não somar cópias de arquivos.
