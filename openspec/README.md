# OpenSpec do Codeboxd

10/11/2026 - [Auditoria de branches e integracao](changes/otimizar-performance-app/validation/integracao-develop-2026-11-10.md): branch publicada; PR aguarda criacao em sessao autenticada. Base `origin/develop` 4a7cabe. Administracao 33/34 e performance 17/37; sem merge em main. P0 movel continua pendente.

10/11/2026 — [Ambiente Cloudinary preparado](changes/hospedar-imagens-publicacoes-cloudinary/validation.md): variáveis privadas com flag false, adaptador de upload assinado e 11 testes locais aprovados; dependências existentes íntegras. Conta/credenciais, integração de posts/URL no Xano e validação real ainda pendentes. Fluxo atual de anexos preservado até ativação validada.

10/11/2026 — [Restrições de redefinição reforçadas](changes/reforcar-restricoes-redefinicao-senha/validation.md): endpoint final exige credencial exclusiva de recuperação, política 8..128/confirmação e senha diferente da atual sob lock. Feedback por etapa e limpeza seletiva da sessão local. Publicado um endpoint; 511 testes locais e 20 checks reais passaram, fixture removida sem envio de e-mail. Limites e inventário documentados.

10/11/2026 — [Recuperação exige conta ativa](changes/impedir-recuperacao-email-sem-conta/validation.md): por solicitação do usuário, endereço sem cadastro/inativo retorna 404 e permanece na primeira etapa. Publicado um endpoint com backup; 16 testes e compilação aprovados, API e navegador real confirmaram rejeição sem envio. Decisão anterior de avanço genérico substituída; falha de envio também não gera sucesso falso.

10/11/2026 — [E-mail de recuperação redesenhado e atraso diagnosticado](changes/melhorar-email-recuperacao/validation.md): HTML/texto publicados no endpoint, 14 testes e sandbox aprovados, feedback imediato e cooldown local. SendGrid revela adiamentos Gmail 421 4.7.32 por alinhamento SPF/DKIM; entregas existentes em 27s/70s e outra pendente. Corrigir causa depende de domínio próprio autenticado; redução real de entrega não comprovada.

10/11/2026 — [Página de recuperação simplificada](changes/simplificar-pagina-recuperacao/validation.md): uma etapa por vez, sem e-mail duplicado, cartão compacto e confirmação final com login. Doze testes e compilação aprovados; etapa inicial conferida no navegador em 390/1440px sem overflow. Sem novos envios ou alterações remotas.

10/11/2026 — [SendGrid para recuperação](changes/integrar-sendgrid-recuperacao/validation.md): remetente verificado e integração publicada no Xano após backup/prévia de um endpoint. Chave/remetente privados conferidos e demais variáveis preservadas; sete testes locais passaram. Aceitação de envio, recebimento e ciclo completo ainda pendentes; histórico Resend preservado.

08/11/2026 — [Mascotes Lume e carregamento revertidos](changes/melhorar-mascotes-carregamento/validation.md) a pedido do usuário. Bonecos e carregamento anteriores restaurados; integração da logo preservada. A entrega e suas evidências são históricas, sem aplicação atual.

09/11/2026 — [relatório consolidado após o ensaio administrativo local](changes/gerenciamento-website/validation/relatorio-projeto-2026-11-09.md):
48 testes aprovados (22 do executor novo + 26 guardas), sem acesso Xano ou
alteração funcional. Permanecem administração 33/34, performance 17/37 e
recuperação 8/10. Destino e A2–A4 ainda precisam de decisão específica.

09/11/2026 — retomada administrativa posterior ao registro de contexto abaixo:
A0 de inventário e login/leitura limitada A1 autorizados e executados; preparação
de [guardas locais](changes/gerenciamento-website/validation/guardas-locais-2026-11-09.md)
com 26 testes offline aprovados. A2–A4 continuam sem autorização, sem escrita
administrativa; 9.2 permanece aberta, 33/34. O registro de contexto a seguir
preserva o estado de sua própria rodada anterior à autorização de A0/A1.

09/11/2026 — [contexto atualizado e plano de performance](changes/otimizar-performance-app/validation/retomada-2026-11-09.md):
PR #28 integrado em develop (a21c806), sem concluir o aceite administrativo 9.2.
Administração 33/34, performance 17/37 e recuperação 8/10. Próxima preparação:
baseline/metas de performance 1.3/1.5; A0–A4 permanecem sem execução autorizada.

05/11/2026 - Aplicacao atualizada em producao local (3030), sem Docker. 494 testes locais, 34 etapas reais desktop/celular e remocao na interface atualizada aprovados; dados descartaveis limpos. Performance 17/37, administracao 33/34 e recuperacao 8/10: **23 tarefas funcionais abertas**. Capa/sinopse mobile corrigida, validada em 20 cenarios e [arquivada](changes/archive/2026-11-05-corrigir-capa-sinopse-mobile/validation.md). [Evidencias e limites desta rodada](changes/otimizar-performance-app/validation/conclusao-2026-11-05.md). Resend: chave restrita ao envio; 401 ao listar dominios nao prova chave invalida. Recebimento/ciclo real de recuperacao continuam pendentes.

04/11/2026 - Conexoes/feed/listas concluida (10/10), specs sincronizadas e
change [arquivada](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/conclusao-2026-11-04.md).
Dashboard administrativo publicado e validado: administracao 33/34,
performance 14/37 e recuperacao 8/10. Restam 26 tarefas funcionais;
os registros datados anteriores preservam seus respectivos estados.
Scaffold corrigir-follow-feed-status-filmes arquivado como supersedido,
sem nova entrega funcional. OpenSpec global: 22/22 validos.


03/11/2026 — [encerramento no estado atual para Git](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/encerramento-2026-11-03.md):
conexões/listas **9/10**, contratos publicados e seis itens migrados para cinco
relações. API e integridade aprovadas, fixtures/rotas temporárias removidas.
Aceite visual continua aberto; rota dinâmica direta retornou 404 no servidor
local. Sem novas implementações após o pedido de encerrar, sem arquivo ou commit.

03/11/2026 — implementação de contratos de conexões/listas autorizada e pronta
localmente: [15 documentos em prévia aprovada, 477 testes e backup/rollback](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/implantacao-2026-11-03.md).
Change agora **7/10** após detalhar a implantação autorizada. Branch e fonte de
teste recusadas pelo plano gratuito; publicação ainda não executada. A escolha
do ambiente de ensaio está pendente. Avaliações e dados remotos não alterados.

03/11/2026 — [conferência das changes e do Xano](changes/archive/2026-11-04-auditar-estado-remoto-changes-abertas/report.md):
acesso administrativo de leitura validado; tabela/função/rotas do novo status
de listas ausentes, feed direto presente e contratos admin/Resend inspecionados.
Flags locais de biblioteca paginada e identidade padrão estão desativadas em
processo novo, divergindo da ativação histórica. Sem migração ou escrita remota;
38 tarefas funcionais continuam abertas. Scaffold sem planejamento falha na
validação global; evidências e próximos passos no relatório.

30/10/2026 — [relatório atualizado das changes](RELATORIO_CHANGES_2026-10-30.md):
quatro entregas concluídas foram sincronizadas/arquivadas, preservando limites
de validação local/remota. Permanecem quatro changes funcionais com **38 tarefas
abertas** e um scaffold sem planejamento. Conexões/feed/listas (1 pendente) e
recuperação de senha (2 pendentes) são as próximas prioridades; o relatório
detalha aplicação manual Xano, contas e caixa de e-mail necessárias.

29/10/2026 — correções locais de seguir, feed e switch das listas padrão na
[change corrigir-conexoes-feed-listas](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/proposal.md).
O backend Xano **não foi alterado**: roteiro de migração/contratos e verificações
em [xano-changes.md](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/xano-changes.md).
O switch depende da aplicação manual desse contrato. Aceite remoto permanece
aberto; [evidências locais](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation.md).

28/10/2026 — feed corrigido localmente: foto principal e obra em miniatura,
curtidas com estado/pending e comentários em diálogo contextual. Change
[corrigir-publicacoes-foto-interacoes](changes/archive/2026-10-30-corrigir-publicacoes-foto-interacoes/tasks.md)
com **6/6 tarefas**, 432 testes e oito cenários de navegador fictício aprovados.
[Entrega e limites](changes/archive/2026-10-30-corrigir-publicacoes-foto-interacoes/validation.md).
Sem publicação Xano ou reinício da instância normal; as três changes abaixo
continuam com seus próprios critérios e contagens. Sincronização/arquivo do
feed não executados.

27/10/2026 — busca administrativa corrigida e publicada no Xano, com backup,
dry-run final sem delta e **79 checks reais aprovados** após login admin.
Tarefa 3.1 concluída; administração **22/34**. [Publicação, aceite e limites](changes/gerenciamento-website/validation/busca-parametros-2026-10-27.md).

Listas: [corrigir-duplicacao-listas-padrao](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/tasks.md) foi sincronizada e arquivada em 26/10/2026 com **11/11 tarefas**. Coleção própria separada, públicas agrupadas por autor e identidade estável publicada/ativada. Validação local, API e duas contas reais no navegador, limpeza e limites estão na [conclusão](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/validation/conclusao.md). As três changes funcionais abaixo mantêm suas pendências; o arquivo histórico agora reúne 18 entregas/diretórios, preservando as contagens anteriores por rodada.

Estado documental reconciliado em **26/10/2026**, para a AP2.

Continuação de segurança nesta data: [proteger-credenciais-expostas](changes/archive/2026-10-26-proteger-credenciais-expostas/status.md)
está concluída com 9/9 tarefas; a dependência
[revogar-sessoes-apos-troca-senha](changes/archive/2026-10-26-revogar-sessoes-apos-troca-senha/tasks.md)
está concluída com 6/6. TMDB e quatro senhas de teste rotacionados, quinta conta
histórica ausente, revogação publicada e validada em 39 rotas protegidas.
Ambas foram arquivadas em 26/10/2026 por solicitação do usuário, após sincronizar
seis requisitos com as specs principais e conferir tarefas/evidências.
A tabela funcional abaixo preserva as três changes de produto, sem alterar
suas pendências ou contagens.

## Estado atual

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
- [Recuperação/Resend, 28/10](changes/recuperar-senha-codigo-6-digitos/validation/elegibilidade-resend-2026-10-28.md): 24 testes locais passaram; a elegibilidade do destinatário ainda bloqueia envio/entrega reais, e 3.2/3.4 permanecem abertas.

## Entregas arquivadas

Fundação (87 tarefas únicas), modelo de dados (37), meias estrelas, listas iniciais,
tradução DeepL, conteúdo obrigatório, correções operacionais e ajustes de feed/listas
têm entregas arquivadas. Os 14 diretórios históricos anteriores são preservados;
fundação e modelo de dados aparecem em duas datas e não são entregas somáveis.
Esta revisão documental foi validada e arquivada em 26/10, chegando a 15 diretórios.
As duas entregas de segurança arquivadas posteriormente nessa data elevam o total a 17.
Nenhuma change funcional ativa está pronta para arquivar.

## Onde consultar

| Documento | Conteúdo |
| --- | --- |
| [RELATORIO_STATUS.md](RELATORIO_STATUS.md) | Entregas e limites atuais |
| [PENDENCIAS.md](PENDENCIAS.md) | Pendências com IDs preservados |
| [CONTEXTO.md](CONTEXTO.md) | Arquitetura e decisões |
| [AMBIENTE.md](AMBIENTE.md) | Ambiente `.venv` e operação local sem Docker |
| [HISTORICO.md](HISTORICO.md) | Rodadas anteriores e decisões substituídas |
| [VALIDACAO.md](VALIDACAO.md) | Validações documentais e limites |
| `specs/` | 19 contratos consolidados |
| `changes/` | Planejamento, tarefas e evidências ativas |
| `changes/archive/` | Entregas históricas, incluindo esta revisão concluída |

## Rotina de trabalho

1. Ler contexto, pendências, histórico e artefatos da change pertinente.
2. Conferir `git status --short` e `openspec list --json`.
3. Criar change com planejamento antes de editar se o pedido não estiver coberto.
4. Distinguir implementação local, testes simulados, API remota e navegador real.
5. Registrar evidências por tarefa; manter critérios não atendidos abertos.
6. Validar change e specs antes de sincronizar/arquivar entregas concluídas.

## Histórico e rastreabilidade

Relatórios datados e evidências preservam o estado de suas próprias rodadas.
Os documentos centrais anteriores a esta reconciliação foram preservados em
[snapshot da revisão](changes/archive/2026-10-26-reconciliar-openspec-ap2/antes/README.txt).
Esses snapshots não são o estado atual. Portas, processos e janelas citados em
evidências históricas não foram verificados como ativos em 26/10.
