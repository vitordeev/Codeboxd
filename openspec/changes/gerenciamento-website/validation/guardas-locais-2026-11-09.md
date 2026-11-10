# Preparação local das guardas da homologação — 09/11/2026

## Escopo e plano antes da implementação

Continuação autorizada da preparação local da tarefa 9.2, após login/leitura A1.
Não autoriza A2–A4 nem novas chamadas ao Xano. A0 encontrou somente v1/live e
fonte live; escolher o destino de escrita continua sendo decisão do usuário.
Nenhum registro existente está autorizado como alvo. Manter 33/34.

Preparar `tools/admin_acceptance_guard.py` como política pura, sem cliente HTTP,
credenciais, leitura de ambiente ou execução automática. Sua saída será apenas
uma prévia local. Não conectar a política aos executores reais nesta rodada.

A prévia de uma atualização deve exigir aprovação explícita A3 vinculada ao
destino completo, run_id e ator; aprovação adicional para destino compartilhado;
manifesto com ID, identidade e hash de uma fixture criada pela rodada; payload
exato previamente aprovado; conteúdo atual igual ao snapshot registrado; e
confirmação. Bloquear ator como alvo, contas administrativas, originais,
mudanças de identidade, rotas/métodos fora do escopo, campos extras e auditoria.
Nesta primeira preparação, somente modelar os PUTs de conta, catálogo e report.
Provisionamento, deduplicação e limpeza ficam bloqueados e requerem adaptadores
futuros próprios, sem autorizar ferramentas históricas.

Testes sintéticos específicos comprovarão os bloqueios e os três casos de
prévia aceita, sem rede. Não repetir os 68 cenários de navegador, o login real
ou Reports: não haverá alteração da UI, sincronismo ou adaptador de leitura.
Revisar diff, OpenSpec, segredos nos arquivos novos e preservação por hashes.

## Limites para a futura integração

Um objeto Python de aprovação não prova consentimento humano. O operador deverá
transcrever a autorização específica e conferir sua referência antes de usar
um futuro transporte. O manifesto deve vir de journal confiável, com origem,
donos e IDs conferidos por leitura independente; prefixo nunca prova propriedade.
A prévia não elimina concorrência entre leitura e escrita, não impõe ritmo,
teto de chamadas ou execução única e não valida cascatas. O futuro adaptador
deve implementar esses controles e reconciliação após timeout, sem retry cego.
Testes de negação com membro/visitante também ficam fora desta primeira política.

Sem aprovação de A2/A3/A4, destino, retenção e conferência dos contratos/cascatas,
não iniciar seed. A integração real e a matriz de aceite continuam pendentes.

## Resultado

Implementação e testes ainda não executados no momento de registrar este plano.
Acrescentar os resultados reais ao término, preservando este planejamento.

### Execução posterior ao planejamento

Implementados o módulo puro e seus testes, sem alterações funcionais da aplicação
e sem conexão aos proxies/executores remotos. Conferidos os contratos locais de
conta, catálogo e report; o campo do denunciante é `reporter_user_id`. A política
usa esse campo na identidade, além de tipo/ID do alvo. Isso não constitui nova
verificação dos contratos publicados no Xano.

[Log sanitizado e hashes](guardas-locais-2026-11-09.json): **26 testes aprovados**,
zero falhas/erros/skips. Executados com o loader unittest na `.venv`, com a saída
capturada no JSON; comando equivalente para reprodução:

```powershell
.venv\Scripts\python.exe -m unittest tests.test_admin_acceptance_guard -v
```

| Cenário local | Esperado | Observado / resultado |
| --- | --- | --- |
| PUT de conta, obra e report com intenção exata | Produzir apenas prévia por hashes | Três prévias aceitas; `remote_execution=false`, socket bloqueado no teste; aprovado |
| Aprovação ausente, A0/A1 apenas, ator divergente ou sem confirmação | Recusar | Motivos específicos de recusa; cancelamento não abre socket; aprovado |
| Destino alterado, HTTP, URL com credenciais/path/query, workspace inválido | Recusar | Recusado antes da prévia; aprovado |
| Fonte live sem consentimento adicional, inclusive shared=false | Recusar | Recusado; destino sintético isolado com aprovação própria aceito; aprovado |
| Sem manifesto, ID duplicado/estrangeiro ou outra rodada | Recusar | Recusado, mesmo com prefixo semelhante; aprovado |
| Ator como alvo, admin/moderator ou papel ausente | Recusar | Conta protegida; aprovado |
| ID/identidade/hash da releitura divergentes | Parar para reconciliação | Recusado; aprovado |
| Campos extras, alteração de identidade/ator, decisão sem marcador ou payload diferente | Recusar | Recusado; aprovado |
| POST/DELETE/PATCH, setup, limpeza, auditoria e variantes de rota | Permanecer fora do escopo | Recusado; aprovado |

Não houve novos bugs funcionais identificados na aplicação nesta rodada. O
resultado comprova somente a política offline; não comprova autoria de manifesto,
papel atual do ator no servidor, execução única, ausência de concorrência ou
homologação da UI. Não há configuração/manifesto real de escrita aprovado nem
comando de mutação liberado. Os testes usam aprovação e registros sintéticos.

Preservação: checkpoint privado `.local/checkpoints/admin-guards-20261109-163136`
guarda o estado anterior aos novos
arquivos. Nenhum commit/push, troca de branch, seed, limpeza ou acesso Xano nesta
rodada. `reflex.lock/package.json` permanece com SHA-256
`60953f76d66b9864a8ccf100dfc3520f6a5d07f7b3759cc52d4fd5747a54c3e0`.

### Próximos passos ainda bloqueados ou não executados

1. **Decisão pendente do usuário:** destino isolado ou autorização expressa para
   v1/live, fonte live, com efeitos visíveis no ambiente compartilhado. O pré-voo
   não identificou outro destino disponível.
2. **Não executado:** adequar provisionamento/deduplicação e limpeza com retenção;
   conectar guardas ao transporte, impor teto/ritmo, journal persistente e
   interrupção/reconciliação de escrita ambígua. Ensaiar localmente antes da rede.
3. **Sem autorização:** A2 (lote proposto de até 239 registros mais auditoria),
   A3 (operações E1–E7 sobre manifesto) e A4 (limpeza limitada e retenção C2),
   nos termos do design. Nenhum objeto de teste substitui essa autorização.
4. **Aceite integrado não executado nesta rodada:** permissões no navegador,
   alterações/persistência/auditoria, filtros/página 2, snapshots, erros/retry e
   verificação visual em 1440/390. Preservar as evidências reais anteriores com
   seus limites, sem repetir os testes aprovados por mera contagem.

9.2 permanece aberta, **33/34**, sem recomendação de conclusão ou arquivamento.

### Conferência final desta rodada

- `git diff --check`: aprovado. Arquivos novos também conferidos quanto a espaços
  finais, por leitura local.
- `openspec validate gerenciamento-website --type change`: válido, com o aviso
  preexistente de requisito longo em content-moderation, sem erro.
- Scanner `scan_bytes` nos quatro arquivos novos desta rodada, incluindo valores
  configurados em memória: zero achados. Verificação heurística, não garantia
  absoluta de ausência de segredos.
- Hashes dos dois arquivos Python coincidem com o JSON dos testes. Arquivos
  preexistentes fora dos três documentos de acompanhamento editados permanecem
  iguais ao checkpoint, incluindo os registros de performance e o lockfile.
- Branch mantida em `task/performance-context-20261109`, HEAD `a21c806`.
  Referência local develop permanece `ac3317d`; origin/develop permanece
  `a21c806` na referência já consultada, sem novo fetch nesta rodada.
- Nenhuma compilação/execução Reflex foi necessária: nenhuma API Reflex,
  componente, estado ou processo da aplicação foi alterado.
