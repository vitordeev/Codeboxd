# Estado do Codeboxd — 26/10/2026

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

| Change funcional ativa | Concluídas | Abertas | Critérios restantes |
| --- | ---: | ---: | --- |
| [gerenciamento-website](changes/gerenciamento-website/tasks.md) | 21/34 | 13 | Autorização completa, mutações, auditoria, filtros/paginação e navegador real |
| [otimizar-performance-app](changes/otimizar-performance-app/tasks.md) | 14/37 | 23 | Metas das demais jornadas, comparações completas, mutações, duas contas e browser real |
| [recuperar-senha-codigo-6-digitos](changes/recuperar-senha-codigo-6-digitos/tasks.md) | 8/10 | 2 | Envio Resend aceito, chegada na caixa e ciclo completo de recuperação |

As contagens vêm dos checklists, não medem o percentual global do produto.
As três changes têm planejamento completo; isso não significa implementação concluída.

Evidências mais recentes:

- [Performance e conexões Xano, 24/10](changes/otimizar-performance-app/validation/conexoes-xano-2026-10-24.md): 374 testes históricos, compile/build e comparação de leituras reais; não comprova a jornada inteira.
- [Leituras de admin e membro, 23/10](changes/otimizar-performance-app/validation/retomada-conclusao-2026-10-23.md): 44 e 70 checks, respectivamente; não substituem testes de mutações e navegador administrativo.
- [Administração, 22/10](changes/gerenciamento-website/validation/retomada-evidencias-2026-10-22.md): 21/34; interface local com fixtures e reports documentados.
- [Recuperação/Resend, 22/10](changes/recuperar-senha-codigo-6-digitos/validation/resend-integracao-2026-10-22.md): integração publicada; destinatário testado rejeitado pelo remetente de testes, sem entrega comprovada.

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
