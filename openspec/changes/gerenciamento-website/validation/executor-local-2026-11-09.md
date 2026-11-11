# Ensaio do executor administrativo — 09/11/2026

## Plano registrado antes da implementação

Vínculo: tarefa 9.2, change ativa gerenciamento-website, 33/34. O pedido de
continuação e relatório autoriza desenvolver/testar localmente. Permanecem as
restrições explícitas de escrita Xano; nenhuma aprovação A2–A4 foi registrada.

Preparar `tools/admin_acceptance_executor.py` para ensaio, aceitando exclusivamente
`httpx.MockTransport` e origem HTTPS terminada em `.invalid`. Não ler `.env`,
credenciais ou manifestos reais; não mudar os executores remotos existentes.
Conectar `preview_update` ao transporte fictício com a sequência:

1. Cancelamento e prévia inicial: recusar antes de qualquer chamada simulada.
2. Reservar orçamento para quatro chamadas; serializar operações e espaçá-las.
3. Consultar ator ativo/admin e registro pelo ID/tabela configurados; revalidar
   identidade/hash e aprovação com a guarda existente.
4. Persistir intenção em journal local exclusivo e fsync antes do único PUT.
5. Reler independentemente e conferir estado persistido e identidade, sem usar
   HTTP 200 ou o corpo do PUT como prova suficiente.
6. Confirmar no journal e atualizar snapshot somente após a releitura válida.
   Falha/timeout após intenção interrompe a instância e exige reconciliação,
   sem retry automático. Journal existente impede reinício silencioso.

O journal conterá somente hashes, métodos/códigos e estados de execução; não
payloads, registros, senhas ou tokens. A simulação não prova auditoria Xano,
login/renderização Reflex, provisionamento, deduplicação ou limpeza. Não será
liberado comando de escrita real nem será alterada a política de produto.

Testar sucessos dos três PUTs, confirmação, recusa por permissões, deriva do
alvo, payload não aprovado, orçamento/ritmo, redirects/429, erro de journal,
timeout após efeito e persistência divergente. Usar relógio virtual nos testes,
sem esperar ou acessar rede real. Reexecutar as 26 guardas por serem dependência
direta do novo executor; não repetir os 68 cenários visuais já comprovados.
Conferir OpenSpec, diff, hashes/segredos e preservar o checkpoint anterior.

## Resultado

A preencher com evidência real após a implementação e os testes.

### Implementação e execução após o plano

Criado o executor de ensaio e 22 testes novos. A guarda anterior permanece
inalterada. O construtor rejeita transportes diferentes de MockTransport e
destinos fora de `.invalid`; não há opção CLI, configuração `.env` ou token que
habilite execução real. A simulação usa formas de rotas auth/Metadata/social,
sem alegar que o roteamento de branch/contratos reais foi validado por isso.

Comando executado após a revisão dos casos de falha:

```powershell
.venv\Scripts\python.exe -m unittest tests.test_admin_acceptance_executor tests.test_admin_acceptance_guard -v
```

**48 testes aprovados: 22 novos do executor e 26 regressões da dependência**.
[Saída real e hashes dos arquivos](executor-local-2026-11-09.json). A primeira
execução aprovou 45; três casos adicionais cobriram aprovação ausente, ator
divergente/membro e falha na releitura após PUT. Não somar as duas execuções.
Todos os testes do executor bloquearam socket real e usaram relógio virtual.

| Cenário | Esperado | Observado | Resultado |
| --- | --- | --- | --- |
| Três atualizações válidas em memória | Ator GET, alvo GET, um PUT, alvo GET | 12 chamadas simuladas, três confirmações no journal | Aprovado local |
| Cancelar, A0/A1 apenas, payload/ID não aprovado | Zero chamadas | Nenhuma solicitação ao transporte fictício | Aprovado local |
| Ator suspenso, membro ou ID diferente | Parar antes da leitura do alvo/PUT | Apenas GET de sessão; instância interrompida | Aprovado local |
| Alvo mudou desde o snapshot | Parar antes de PUT | Duas leituras e recusa por hash | Aprovado local |
| Orçamento insuficiente | Não começar sequência parcial | Segunda operação recusada antes de novas chamadas | Aprovado local |
| Ritmo mínimo de 3,1 s | Espaçar solicitações | Três intervalos virtuais por sequência; sem espera real | Aprovado local |
| Redirect, 429 ou JSON inválido | Parar sem seguir/repetir | Uma chamada e instância interrompida | Aprovado local |
| HTTP 200 sem persistência | Não registrar sucesso | Releitura divergiu; journal exige reconciliação | Aprovado local |
| Timeout após gravação ou na releitura | Não repetir PUT nem declarar sucesso | Efeito fictício preservado, um PUT, instância interrompida | Aprovado local |
| Journal antes da gravação falha | Não enviar PUT | Somente duas leituras | Aprovado local |
| Restart com journal existente ou mesma operação já aplicada | Não repetir silenciosamente | Reinício/segunda aplicação bloqueados | Aprovado local |
| Snapshot reportado alterado na revisão | Rejeitar confirmação de integridade | Divergência detectada após releitura | Aprovado local |

As falhas da tabela são injetadas nos testes; não são defeitos encontrados no
Xano ou na aplicação. Nenhuma nova correção funcional foi necessária. A política
não aceita provisionamento, criação/deduplicação de obra, limpeza nem tentativas
de mutação como membro/visitante. Isso permanece trabalho não implementado para
a integração futura. A simulação não é executor remoto pronto para uso.

## Limites e pendências para o aceite

- O journal atual guarda hashes/estados e bloqueia reinício automático. Não
  oferece retomada/reconciliação automática nem exclusão de registros.
- A leitura imediatamente anterior reduz divergências, mas não elimina uma
  alteração concorrente entre GET e PUT; integração real requer janela controlada
  e tratamento explícito dessa condição, sem restaurar dados de terceiros.
- Papel ativo/admin, persistência e integridade foram exercitados com dados
  fictícios. Auditoria real, revisão do alvo reportado por leitura independente,
  frontend e duas larguras não foram executados nesta rodada.
- Ainda é necessário definir destino, conferir contratos publicados/cascatas,
  adequar setup/deduplicação/limpeza e obter A2–A4 antes de dados reais. Apenas
  v1/live e fonte live foram observados em A0; não criar isolamento implicitamente.
- Nenhum critério obrigatório de 9.2 foi encerrado: permanece **33/34**.

## Preservação e verificações

Checkpoint anterior: `.local/checkpoints/admin-executor-20261109-163724`, ZIP,
hashes de 13 arquivos locais e referências Git. Antes de atualizar o acompanhamento,
todos os 13 arquivos coincidiram com seus hashes, incluindo o lockfile e os
artefatos de performance. Depois, somente os três documentos de acompanhamento
indicados abaixo recebem novos registros; as demais alterações anteriores são
preservadas integralmente.

Arquivos novos desta rodada: executor, seus testes, este relatório de ensaio,
JSON de evidência e relatório consolidado do projeto. Atualizados README,
PENDENCIAS e tasks da change administrativa; nenhuma alteração em aplicação,
contratos Xano, arquivo de dependências ou tasks de performance.

`git diff --check` aprovado; as três changes funcionais ativas foram validadas
com OpenSpec. O aviso de requisito longo em content-moderation é preexistente.
Scanner heurístico dos arquivos novos sem achados de segredos, com valores
configurados comparados somente em memória. Não foi necessária compilação Reflex
ou repetição de browser/Reports, pois UI e executores remotos não foram alterados.

Nenhum acesso Xano, operação administrativa remota, commit, push, merge, troca
de branch ou arquivamento. Branch atual permanece task/performance-context-20261109.
O [relatório consolidado](relatorio-projeto-2026-11-09.md) detalha o projeto e a
sequência restante para revisão do usuário.
