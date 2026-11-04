# Estado das changes — 30/10/2026

## Resultado da revisão

Quatro entregas anteriores, com 16 tarefas concluídas no total, foram encerradas
e arquivadas após conferir artefatos, checklists e evidências. A consolidação
documental desta rodada também é rastreada em change própria. Não houve alteração
do produto, deploy, acesso ao workspace Xano, mutação de contas ou envio de e-mail.

| Entrega encerrada | Checklist | Evidência e limite |
| --- | --- | --- |
| [auditar-relatos-testes-manuais](changes/archive/2026-10-30-auditar-relatos-testes-manuais/tasks.md) | 3/3 | Auditoria/backlog documental; não é correção dos seis relatos |
| [reposicionar-card-obra-feed](changes/archive/2026-10-30-reposicionar-card-obra-feed/tasks.md) | 3/3 | Renderer e compile; revisão visual em navegador não executada nessa entrega |
| [corrigir-upload-imagem-feed](changes/archive/2026-10-30-corrigir-upload-imagem-feed/tasks.md) | 4/4 | Testes com mocks e compile; upload autenticado real não comprovado |
| [corrigir-publicacoes-foto-interacoes](changes/archive/2026-10-30-corrigir-publicacoes-foto-interacoes/tasks.md) | 6/6 | Testes e oito cenários históricos em navegador com fixtures; não conta real |

Os deltas das três entregas de feed foram sincronizados na spec consolidada.
Como foto/interações e reposicionamento modificavam o mesmo requisito, a revisão
preservou todos os cenários de fallback, fotos e telas estreitas. A ordem efetiva
de fechamento respeitou essa dependência. Os critérios das entregas concluídas
não exigiam novo deploy ou aceite remoto para seu escopo local. Seus limites
continuam documentados nos arquivos de validação arquivados e abaixo.

## Changes que permanecem abertas, por menor quantidade pendente

| Change | Concluídas | Pendentes | Estado atual e próximo passo |
| --- | ---: | ---: | --- |
| [corrigir-conexoes-feed-listas](changes/corrigir-conexoes-feed-listas/tasks.md) | 6/7 | 1 | Python e mocks concluídos; aplicar migração/contratos Xano e validar jornadas reais (3.2) |
| [recuperar-senha-codigo-6-digitos](changes/recuperar-senha-codigo-6-digitos/tasks.md) | 8/10 | 2 | Integração publicada historicamente; envio aceito e recebimento/ciclo de recuperação ainda sem evidência (3.4/3.2) |
| [gerenciamento-website](changes/gerenciamento-website/tasks.md) | 22/34 | 12 | Autorização completa, mutações, auditoria, catálogo/reports e browser real ainda pendentes |
| [otimizar-performance-app](changes/otimizar-performance-app/tasks.md) | 14/37 | 23 | Baselines/metas, comparações das jornadas, browser e mutações reais; não é apenas falta de credencial |

Total dessas quatro changes: **50 tarefas concluídas, 38 abertas**. As contagens
não medem percentual de produto nem somam testes históricos como execuções novas.

`corrigir-follow-feed-status-filmes` contém somente `.openspec.yaml`, sem
proposal/design/specs/tasks. É um scaffold preexistente, **não uma entrega 0/0
concluída**. Foi preservado. Seu nome parece sobrepor a change conexões/feed/listas;
para reaproveitá-lo é preciso definir trabalho novo e planejamento, ou decidir
explicitamente descartá-lo. Não inventar requisitos nem arquivar como concluído.

## O que preciso do usuário

### 1. Xano — desbloqueia a change mais próxima de terminar

Não tenho acesso direto ao workspace e a restrição anterior de aplicação manual
continua válida. É necessário aplicar e conferir o
[roteiro completo](changes/corrigir-conexoes-feed-listas/xano-changes.md):

- Backup, limpeza de follows e índice único composto.
- Stacks idempotentes PUT/DELETE de follow e feed consultando posts dos seguidos.
- Tabela de status único, migração dos itens padrão com Assistido vencendo conflitos.
- GET/PUT `/media-list-status/{media_id}` e todas as projeções/escritas das listas padrão.
- Ensaios de concorrência, privacidade, avaliações preservadas e usuário sem posts.

Preciso da confirmação de quais passos foram aplicados e resultados sanitizados
dos ensaios. Para validar pela aplicação, serão necessárias duas contas de teste
controladas: uma leitora sem posts e outra autora com posts; podem ser usadas
também nas jornadas de listas. Não é necessário fornecer chave de metadados
Xano enquanto a operação continuar manual. REST configurada não concede acesso
administrativo ao workspace nem substitui a atualização dos stacks.

### 2. Recuperação de senha — envio e caixa de entrada reais

Disponibilizar uma conta Codeboxd de teste com caixa controlada elegível ao
remetente Resend configurado. Conforme a evidência histórica da change, pode ser
o e-mail do proprietário da conta Resend para o remetente compartilhado de testes,
ou uma caixa atendida pelo remetente de domínio próprio já verificado.

Confirmar no Xano se `RESEND_API_KEY` e `RESEND_FROM` estão configurados e válidos,
sem compartilhar valores. A chave não precisa ser substituída só por existir
uma pendência. Caso seja necessário corrigir configuração, fazê-lo no ambiente
privado do workspace e aplicar apenas a mudança planejada, com backup.

Após existir destinatário elegível, testar um envio aceito, chegada do código,
troca de senha, login novo, rejeição de reutilização e restauração segura da
conta. Será necessária participação do titular para ler o código. O executor
`tools/password_recovery_remote.py` tem saída histórica datada: adaptar o destino
na change ativa antes de reusar, sem sobrescrever evidências antigas. Não foi
executado nesta rodada, nem foi revalidada externamente a configuração Resend.

### 3. Administração

Uma conta de teste com papel admin, duas contas de membro controladas (uma pode
ser suspensa/reativada durante o ensaio), acesso a ambiente de desenvolvimento
com dados descartáveis e confirmação dos endpoints publicados. Não promover
conta existente automaticamente, não usar credencial Xano como sessão admin.
Login/senhas serão inseridos por fluxo privado quando o ensaio estiver pronto.
Validar papel, contagens, paginação, mutações, auditoria e preservação dos alvos.
Ainda há implementação/verificação a completar; credenciais sozinhas não encerram
as 12 tarefas.

### 4. Performance

As mesmas contas e backend atualizado, um ambiente/URL de teste definido e a
aprovação de metas mensuráveis por jornada após levantar a linha de base. O
checklist exige pelo menos cinco amostras frias/quentes, desktop/celular, chamadas
por serviço, mediana e pior amostra. Valores propostos anteriormente não foram
automaticamente aprovados por este pedido de revisão. Não declarar eliminação
de 429 com base em mocks ou em um único cenário.

### Forma de disponibilizar

Não enviar senhas, códigos ou chaves no chat/OpenSpec/Git. Confirmar apenas os
recursos disponíveis. No momento do teste, usar login interativo ou configuração
privada local não versionada, com acesso mínimo e contas descartáveis. Esta
rodada não leu valores privados nem assumiu validade de credenciais históricas.

## Validação e acompanhamento desta rodada

- Artefatos e checklists das quatro entregas completos, conferidos por `openspec status`.
- `openspec validate --specs`: **19 aprovadas, zero falhas**, após as duas etapas de merge.
- Validação individual e arquivo via CLI das quatro changes aprovados; operações
  usaram `--skip-specs` somente após merge manual e conferência (auditoria sem deltas).
- Registros `archival.md` preservam os limites em cada diretório arquivado.
- Links ajustados para os destinos de arquivo, inclusive os dois documentos em
  docs/planning; apenas destinos dos links foram alterados nesses documentos.
- Testes/compile da aplicação não repetidos: trabalho desta rodada é documental;
  resultados funcionais citados são históricos, não execução nova.
- A change [consolidar-estado-changes](changes/archive/2026-10-30-consolidar-estado-changes/tasks.md)
  registra o fechamento documental e as verificações finais.

Próxima ordem recomendada: aplicar Xano/conexões → validar recuperação com caixa
elegível → completar administração → comparações completas de performance.
Os ensaios reais de upload e revisão visual arquivados como limites podem ser
incluídos na jornada social após o backend estar atualizado, sem reescrever seu histórico.
