# Validação sem outro ambiente Xano — decisão de 17/11/2026

O usuário confirmou que não consegue criar ambiente separado e pediu reformular o trabalho. **Nenhuma entrega vigente exige criar sandbox, workspace, fonte de dados ou plano adicional.** O destino atual conhecido é workspace 147717, branch v1/fonte live; identidade/origem/grupo precisam ser reconferidos no lote real.

Essa decisão autoriza a estratégia e a implementação local. Publicação ou mutações reais dependem de um lote concreto com impacto e limpeza revisados; não estão sendo executadas por este documento ou pelo planejador. Simulação e dry-run continuam distintos de aceite remoto.

| Frente / IDs preservados | Caminho sem ambiente adicional | Evidência que continua necessária |
| --- | --- | --- |
| `preparar-homologacao-xano-admin` 2.2 e 3.1–3.3 | Estratégia supersedida. Preservar 4/8 e ferramentas históricas; retirar os quatro itens não realizados dos pré-requisitos vigentes | Não marcar ambiente criado/publicado; continuação em `validar-integracoes-xano-atual` 2.1/2.2 |
| UI 5.1/5.2 | Contratos, privacidade, paginação e respostas atrasadas testados localmente, com lambdas/fixtures | Execução Xano real para consultas, totais, autenticação e privacidade |
| UI 5.3/5.4 | Backup/prévia do lote no workspace atual; piloto com duas contas descartáveis e listas públicas/privadas próprias | Leitura independente do contrato publicado, visitante/dono/outra conta, mudança de visibilidade, navegador e limpeza/preservação dos dados anteriores |
| Cloudinary 2.1.2 e 2.1.4–2.1.6 | Reservas/posts de duas contas de teste no workspace atual; testes de falha induzida locais; ensaios transacionais limitados ao par de operações aprovado | Persistência/idempotência/autoria/revisão/fila no banco, além dos testes locais já existentes |
| Cloudinary 2.1.7–2.1.9 e 2.2.x | Desenvolver executor e UI localmente; prévia de contratos/limpeza separada no destino atual; ativos descartáveis por ID verificado | Executor supervisionado ainda precisa implementação, referências/estado/retensão reais, API/CDN/navegador e ativação revisada. O planejador genérico não faz destroy |
| Performance 1.3/1.5, 2.3 e 8.x/9.x | Medições de leitura no app atual com limite e conta apropriada; ensaio mutável somente em fixtures próprias; lentidão/429 induzidos em mocks locais | Metas aprovadas, amostras comparáveis e jornadas reais. Não induzir carga/429 na instância compartilhada |
| Recuperação 3.2 | Conta/caixa controlada no backend atual; não exige nova instância | Concluída em 12/12 e arquivada em 17/11: restauração autorizada, login e identidade confirmados. Ensaio original com falha preservado. Nenhum novo código necessário para esse aceite |
| SendGrid / experiência do e-mail | Remetente individual verificado no serviço existente, sem domínio próprio por decisão do usuário | Ambas concluídas em 5/5 e arquivadas: integração comprovada, chegada real e melhora percebida aceita qualitativamente pelo usuário. Sem benchmark quantitativo/SLA ou DNS obrigatório |
| Administração arquivada | Preservar aceite de leitura histórico. Mutações futuras usam a nova change e fixtures próprias | Não reabrir/sobrescrever a entrega arquivada nem confundir leitura administrativa com mutação validada |

## Lotes e limites

1. Leituras/prévias: conferir destino e esquema sem exportar dados/segredos para documentos públicos. `/auth/me` e login podem produzir auditoria normal; não prometer ausência de qualquer escrita interna por usar GET.
2. Preparação de fixtures: revisão própria com quantidade, identidade e journal de criação. O planejador desta change **não provisiona contas**; recibos devem vir de operação aprovada e observada independentemente. Marcador no nome sozinho não prova propriedade.
3. Prévia de alterações: máximo dez ações por lote; digest inclui destino, baseline, recibos, snapshots e payloads. Validade máxima de 30 min. Conta operadora original ativa e de papel admin não é alvo. PUTs administrativos têm allowlist restrita. Senhas, papéis, e-mails/reset, env/schema e DELETE de contas não são aceitos.
4. Limpeza: DELETE genérico limitado a post/lista de fixture com dono comprovado e inventário explícito de referências vazio. Comentários, likes ou itens existentes bloqueiam esse caso; não presumir que os dependentes pertencem ao teste. Auditoria é preservada. Assets Cloudinary exigem sua ferramenta específica e prévia independente.
5. O futuro executor precisa autenticar a identidade do operador nos PUTs admin e a identidade do dono de fixture nos DELETEs de post/lista, reler alvo/referências imediatamente antes de cada ação e confirmar resultado. O planejador valida coerência, **não autentica a origem dos snapshots nem concede permissão de execução**.

## Ferramenta implementada

Exemplo inteiramente sintético, sem rede ou arquivos de credenciais:

```powershell
.venv/Scripts/python.exe -m tools.shared_xano_acceptance --example
```

Prévia de JSON privado preparado independentemente:

```powershell
.venv/Scripts/python.exe -m tools.shared_xano_acceptance --plan .local/lote-xano.json
.venv/Scripts/python.exe -m tools.shared_xano_acceptance --plan .local/lote-xano.json --approval .local/revisao-lote.json
```

O formato executável de referência é `example()` em `tools/shared_xano_acceptance.py`. O JSON contém destino completo, run_id, operator_id, created_at/expires_at, baseline (identidade do destino, data, completude e hashes por ID), snapshots atuais, recibos de criação/identidade/snapshot e ações. Revisão contém `plan_digest`, `reference`, `reviewed_at`, `expires_at`. Ambos os arquivos devem permanecer sob `.local/`. A saída só contém contagens, prazos, hashes e estados. Mesmo uma revisão válida retorna **`remote_execution: false`** e **`baseline_verified_remotely: false`**.

## Contagem e histórico

A preparação isolada permanece visível no CLI por rastreabilidade, com quatro caixas abertas supersedidas. Não se trata de quatro novos bloqueios nem de tarefas concluídas. O quadro vigente exclui essa estratégia e inclui a substituta; o inventário bruto pode apresentar totais diferentes e deve ser identificado como tal. As evidências anteriores de 718 testes e bloqueio de ambiente preservam sua data e não são reescritas como novas execuções.
