# Estado do Codeboxd — atualização 14/11/2026

## Resumo vigente

As sete changes funcionais ativas somam **47/111 tarefas concluídas e 64
abertas**, segundo `openspec list --json` e os checklists atuais. Os critérios
remotos e de navegador permanecem abertos quando não há evidência própria. O
quadro único, com contagens, bloqueios e links, está em
[README.md — Estado atual](README.md#estado-atual-14112026).

**Bloqueios principais:** recuperação da conta controlada após HTTP 403;
autenticação de domínio e comprovação de entrega de e-mail; disponibilidade de
workspace Xano isolado. `gerenciamento-website` foi arquivada em 34/34 para o
escopo de leitura, sem aceite de mutações administrativas reais.

## Registros históricos

05/11/2026 - Aplicacao atualizada em producao local (3030), sem Docker. 494 testes locais, 34 etapas reais desktop/celular e remocao na interface atualizada aprovados; dados descartaveis limpos. Performance 17/37, administracao 33/34 e recuperacao 8/10: **23 tarefas funcionais abertas**. Capa/sinopse mobile corrigida, validada em 20 cenarios e [arquivada](changes/archive/2026-11-05-corrigir-capa-sinopse-mobile/validation.md). [Evidencias e limites desta rodada](changes/otimizar-performance-app/validation/conclusao-2026-11-05.md). Resend: chave restrita ao envio; 401 ao listar dominios nao prova chave invalida. Recebimento/ciclo real de recuperacao continuam pendentes.

04/11/2026 - Conexoes/feed/listas concluida (10/10), specs sincronizadas e
change [arquivada](changes/archive/2026-11-04-corrigir-conexoes-feed-listas/validation/conclusao-2026-11-04.md).
Dashboard administrativo publicado e validado: administracao 33/34,
performance 14/37 e recuperacao 8/10. Restam 26 tarefas funcionais;
os registros datados anteriores preservam seus respectivos estados.
Scaffold corrigir-follow-feed-status-filmes arquivado como supersedido,
sem nova entrega funcional. OpenSpec global: 22/22 validos.


Atualização de 30/10/2026: [relatório das changes](RELATORIO_CHANGES_2026-10-30.md).
Quatro entregas locais completas arquivadas; conexões/feed/listas 6/7,
recuperação 8/10, administração 22/34 e performance 14/37 permanecem abertas.
O relatório distingue validação histórica/local e dependências externas.
As seções abaixo preservam a reconciliação anterior.

Busca administrativa: tarefa 3.1 concluída após correção e publicação limitada
ao GET /admin/users. Backup conferido, dry-run posterior sem delta e 79 checks
reais aprovados em 34 requisições, sem 429. Administração **22/34**; demais
critérios continuam abertos. [Evidências e limites](changes/archive/2026-11-12-gerenciamento-website/validation/busca-parametros-2026-10-27.md).

## Listas concluídas e arquivadas

[corrigir-duplicacao-listas-padrao](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/tasks.md): 11/11. Coleção pessoal corrigida, descoberta agrupada por autor e nome à direita da foto; identidade padrão anulável/única publicada e ativada, com backfill de 16 listas. 411 testes, build, 18 checks API e 14 critérios reais de navegador comprovados; teste descartável limpo, preservando 19 listas/8 vínculos originais e zero duplicatas. [Evidências e condições](changes/archive/2026-10-26-corrigir-duplicacao-listas-padrao/validation/conclusao.md). Quatro requisitos sincronizados e change arquivada em 26/10/2026. Quotas de navegação rápida permanecem na change de performance.

## Funcionalidades entregues no escopo arquivado

| Área | Entrega e limite |
| --- | --- |
| Conta | Cadastro, login, logout e isolamento por conta; recuperação ainda ativa |
| Catálogo | TMDB (filmes/séries), Kitsu (animes), Open Library (livros); disponibilidade externa variável |
| Descoberta/ficha | Busca, categorias, paginação, metadados e complementos conforme a fonte |
| Biblioteca | Status de consumo, reviews e notas de 0,5 a 5; persistência histórica verificada |
| Perfis/social | Perfil, seguidores, posts, imagens, curtidas e comentários; compatibilidade histórica para `/likes` ausente |
| Listas | Públicas/privadas e itens dos quatro tipos; listas iniciais padronizadas |
| Complementos | DeepL, texto obrigatório em denúncias/reviews e edição de feed/inclusão em listas arquivados |
| Segurança | Credenciais 9/9 e sessões 6/6, arquivadas em 26/10 após sincronização: TMDB rotacionado, quatro senhas substituídas, quinta conta ausente e revogação validada em 39 rotas |
| Dados | Modelo Xano concluído no escopo original; administração acompanhada separadamente |

O arquivamento comprova os critérios documentados da entrega e sua data; não
garante disponibilidade contínua dos provedores ou funcionamento atual de todas as telas.

## Trabalho ainda ativo

O estado funcional vigente está no [quadro consolidado](README.md#estado-atual-14112026)
e nos checklists vinculados. São sete changes ativas, 47/111 tarefas concluídas
e 64 abertas. Os registros históricos acima não substituem essa fonte atual nem
comprovam critérios posteriores à data de cada evidência.

## Limites da avaliação

A revisão documental inicial de 26/10 não executou o aplicativo. Na continuação
de segurança dessa data houve 392 testes locais aprovados, 29 checks remotos e
navegador real; [evidências da entrega arquivada](changes/archive/2026-10-26-revogar-sessoes-apos-troca-senha/validation.md).
O arquivamento posterior conferiu esses registros e validou documentos, sem
reexecutar testes remotos. Hospedagem segue fora da etapa; execução com `.venv`,
sem Docker. P.1 resolvida na cobertura auditada; backup de uploads e refinamento
visual continuam em [PENDENCIAS.md](PENDENCIAS.md). Não há cálculo comprovado de “80% do projeto”.

## Histórico e rastreabilidade

Relatórios datados e evidências preservam o estado de suas próprias rodadas.
Os documentos centrais anteriores a esta reconciliação foram preservados em
[snapshot da revisão](changes/archive/2026-10-26-reconciliar-openspec-ap2/antes/README.txt).
Esses snapshots não são o estado atual. Portas, processos e janelas citados em
evidências históricas não foram verificados como ativos em 26/10.
