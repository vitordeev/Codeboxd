# Pendências atuais — 27/10/2026

Busca administrativa publicada e validada: tarefa 3.1 concluída, 79 checks reais
aprovados; administração agora **22/34**. [Entrega e limites](changes/gerenciamento-website/validation/busca-parametros-2026-10-27.md).

## Listas — concluídas e arquivadas

Change [corrigir-duplicacao-listas-padrao](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/tasks.md): **11/11 tarefas concluídas**. Coleção própria separada, descoberta agrupada por autor com nome à direita do avatar, preparação idempotente publicada no Xano e 16 identidades legadas atribuídas. 411 testes, compilação/build, 18 checks API e 14 critérios de navegador com duas contas reais comprovados. Conta e registros descartáveis removidos; 19 listas e 8 vínculos originais preservados, zero duplicatas/conflitos. [Conclusão e evidências](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/validation/conclusao.md).

Quatro requisitos sincronizados nas specs principais e change arquivada em 26/10/2026 por solicitação do usuário. Limite de chamadas em navegação rápida continua no escopo de performance; validação funcional final foi espaçada conforme a evidência. As três changes funcionais abaixo mantêm suas pendências e contagens.

## Changes funcionais abertas

| Change funcional ativa | Concluídas | Abertas | Critérios restantes |
| --- | ---: | ---: | --- |
| [gerenciamento-website](changes/gerenciamento-website/tasks.md) | 22/34 | 12 | Autorização completa, mutações, auditoria, catálogo/reports e navegador real |
| [otimizar-performance-app](changes/otimizar-performance-app/tasks.md) | 14/37 | 23 | Metas das demais jornadas, comparações completas, mutações, duas contas e browser real |
| [recuperar-senha-codigo-6-digitos](changes/recuperar-senha-codigo-6-digitos/tasks.md) | 8/10 | 2 | Envio Resend aceito, chegada na caixa e ciclo completo de recuperação |

As contagens vêm dos checklists, não medem o percentual global do produto.
As três changes têm planejamento completo; isso não significa implementação concluída.

Evidências mais recentes:

- [Performance e conexões Xano, 24/10](changes/otimizar-performance-app/validation/conexoes-xano-2026-10-24.md): 374 testes históricos, compile/build e comparação de leituras reais; não comprova a jornada inteira.
- [Leituras de admin e membro, 23/10](changes/otimizar-performance-app/validation/retomada-conclusao-2026-10-23.md): 44 e 70 checks, respectivamente; não substituem testes de mutações e navegador administrativo.
- [Administração, 22/10](changes/gerenciamento-website/validation/retomada-evidencias-2026-10-22.md): 21/34; interface local com fixtures e reports documentados.
- [Recuperação/Resend, 22/10](changes/recuperar-senha-codigo-6-digitos/validation/resend-integracao-2026-10-22.md): integração publicada; destinatário testado rejeitado pelo remetente de testes, sem entrega comprovada.

## Critérios administrativos restantes

Os 12 IDs abertos são 2.1–2.3, 3.2–3.3, 4.1–4.2, 5.2–5.4 e 9.1–9.2.
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
