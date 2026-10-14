# Pendências e sequência de retomada

Estado atualizado em 14/10/2026. A change [corrigir-erros-operacionais](changes/corrigir-erros-operacionais/tasks.md) acompanha as correções locais anteriores. Na rodada 13–14/10, contratos administrativos e dois endpoints de posts foram publicados com autorização do usuário; evidências abaixo distinguem publicação e validação completa.

## Administração — change ativa

Publicação autorizada concluída nesta rodada: tabela report + nove endpoints,
delta sincronizado e GETs com 401 para visitante/403 para membro. Falta identificar
contas aprovadas para admin/desativado e validar mutações, contagens, auditoria e
interface completa. [Evidência](changes/gerenciamento-website/validation/publicacao-admin-2026-10-13.md).
P.3 recebeu backup local verificado e utilitário/testes no commit `f93287e`;
P.5 recebeu correções de rascunho/cancelamento e contrato multipart publicadas e validadas no browser;
P.6 tem código inválido rejeitado sem trocar senha, mas e-mail e fluxo completo
continuam pendentes. Token TMDB atual confirmado igual ao histórico; não rotacionado.

Última rodada: [retomada administrativa](changes/gerenciamento-website/validation/retomada-admin-2026-10-13.md). Contratos locais corrigidos para exigir conta explicitamente ativa e permitir listagem sem termo/consulta por ID exato. Dry-run limitado reconheceu tabela report + nove endpoints novos; quatro GETs administrativos retornaram HTTP 404. Publicação do delta revisado submetida à confirmação; validação autenticada e navegador ainda pendentes.

Fonte dos checkboxes: [tasks.md](changes/gerenciamento-website/tasks.md). Há 17 tarefas concluídas e 17 abertas. A [matriz de evidências](changes/gerenciamento-website/validation/revisao-2026-10-13.md) distingue código local e validação real.

| Ordem | IDs existentes | O que falta | Critério de fechamento |
| --- | --- | --- | --- |
| 1 | 2.1 | Verificar autorização diretamente em todos os endpoints administrativos | Admin ativo autorizado; visitante, membro e conta desativada rejeitados sem dados restritos |
| 2 | 2.2–2.3 | Conferir totais, atividade e pendências no Xano real | Contagens conhecidas, paginação e vazio corretos; erro parcial sem valor fictício |
| 3 | 3.1–3.3 | Busca/filtros de usuários, suspensão/reativação e auditoria | Respostas mínimas, sessão suspensa bloqueada, ator servidor e trilha persistida; restaurar conta de teste |
| 4 | 4.1–4.2 | Paginação/filtros e correção de catálogo real | Tipo correto em todas as páginas; identidade externa preservada; erro não altera registro |
| 5 | 5.1–5.5 | Persistência, consulta, transições, snapshots e integridade de reports | Validação de alvo/motivo, acesso protegido, decisão auditada e conteúdo alvo intacto; mensagem via snapshot |
| 6 | 6.2–6.3 | Reutilização/estados de componentes e revisão visual desktop/celular | Vazio, carregamento, erro e retry; navegação legível sem overflow da página |
| 7 | 9.1–9.2 | Completar cobertura de integração e smoke com dados reais | Evidência de autorização, filtros, transições e auditoria; browser admin/membro/visitante e falhas parciais |

Arquivos administrativos já existem. Antes de publicar, comparar o delta local/remoto, conferir documentação de operações e registrar o escopo. O dry-run de setembro não garante o estado remoto atual. Não conceder papel admin automaticamente.

O endpoint local de reports aceita `reviewing`, `resolved` e `rejected`, mas não define um grafo explícito de transições terminais. A tarefa 5.3 deve verificar a política desejada e o comportamento real, sem declarar que todas as transições inválidas já estão bloqueadas.

## Pendências transversais — fora das mudanças arquivadas

Esses itens são inventário para próximas changes ou correções autorizadas. Não representam entrega já concluída nem aumentam a contagem administrativa.

| ID | Prioridade | Tópico e situação | Critério de conclusão |
| --- | --- | --- | --- |
| P.1 | Alta | Ignore e índice corrigidos; 441 entradas privadas/geradas retiradas sem apagar cópias locais. Histórico de `.env` e contas foi confirmado em referência origin/main | Revisar/rotacionar chaves expostas e tratar contas de teste; limpeza atual não elimina commits antigos |
| P.2 | Resolvida localmente | `.venv` instalada e canônica; dependências diretas fixadas; pip check, 113 testes e compilação passaram | Comandos em [AMBIENTE.md](AMBIENTE.md); `venv` anterior preservada |
| P.3 | Alta antes de hospedar | URL concreta de banner corrigida/testada; execução e armazenamento locais, sem Docker | Manter backup do diretório de uploads; escolher persistência para hospedagem quando essa etapa for solicitada |
| P.4 | Resolvida | Mensagens de erro de upload corrigidas e verificadas | Testes de rede, HTTP e JSON inválido passaram |
| P.5 | Resolvida nesta rodada | Contrato multipart e preservação do rascunho/cancelamento corrigidos; browser real validado | Criar/editar/recarregar, rejeitar inválido e cancelar passaram; posts, arquivos staged e blobs de teste limpos. Evidência em `validation/uploads-and-session-2026-10-13.md` |
| P.6 | Em validação final | Código de seis dígitos implementado/publicado com 15 minutos, cinco tentativas, cooldown e uso único; fluxo de senha verificado no Xano | Confirmar chegada do e-mail e fluxo com caixa controlada. Change `recuperar-senha-codigo-6-digitos`, evidência `validation/implementacao-2026-10-14.md` |
| P.7 | Média | `/likes` remoto ausente no último registro | Revalidar contrato remoto; manter fallback ou publicar rota após revisão; verificar curtidas sem N+1 |
| P.8 | Resolvida para retomada | Checkpoints atuais de `docs/` apontam para OpenSpec; histórico anterior preservado | Novas alterações continuam centralizadas no OpenSpec |
| P.9 | Conforme crescimento | Estado e páginas sociais concentram muitas responsabilidades | Separar por domínio quando houver necessidade concreta, mantendo rotas/eventos e testes relevantes |
| P.10 | Fora da etapa atual | Publicação/domínio/HTTPS ainda não validados; Docker excluído por decisão do usuário | Definir hospedagem somente quando solicitada; operação atual local com `.venv` |
| P.11 | Antes de reusar validações | Scripts históricos têm caminhos anteriores ao arquivo e portas fixas | Copiar/adaptar scripts para nova pasta de resultados; preservar arquivo histórico e não criar contas incidentalmente |
| P.12 | Corrigida localmente, publicação pendente | Usuário esclareceu que o erro ocorre no admin: logs confirmaram `Invalid filter: to_lower` em usuários/catálogo e `reports.items` ausente; três GETs corrigidos e 18 testes admin passaram | Concluir backup/dry-run, publicar e validar com admin aprovado. [Checkpoint](changes/gerenciamento-website/validation/buscas-admin-2026-10-14.md); testes públicos anteriores não validam o painel |

## Fora do escopo atual

Chat/mensageria privada, notificações, recomendações por aprendizado de máquina, replicação integral de provedores e infraestrutura de múltiplas réplicas não fazem parte das entregas encerradas. Reports `message` não significam que há mensageria implementada. Não transformar esses tópicos em tarefas concluídas.

## Como encerrar a próxima change

Evidência das correções locais: [correcoes-2026-10-13.md](changes/corrigir-erros-operacionais/validation/correcoes-2026-10-13.md). A change concluiu 7/7 tarefas do escopo local e aguarda arquivamento; 3.1/3.2 foram retiradas do escopo por decisão do usuário, sem serem contabilizadas como entregas.

Registrar evidência por ID (data, comando/cenário, camada, resultado, limitações e limpeza de dados de teste). Marcar somente o critério verificado. Validar artefatos, sincronizar os deltas concluídos em `specs/`, conferir correspondência e arquivar a change sem tarefas abertas. Atualizar README, contexto, histórico e pendências na mesma rodada.
