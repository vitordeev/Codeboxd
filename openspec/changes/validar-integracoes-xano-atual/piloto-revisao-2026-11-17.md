# Prévia concreta do piloto no Xano atual

Tarefa 2.1 em preparação, change **4/6**. Nenhum provisionamento, publicação, alteração ou limpeza remota foi executado.

## Destino e coleta real

Workspace **147717**, branch **v1**, fonte **live**. Grupos Authentication **429670** e Codeboxd **433585**, canônicos conferidos com as URLs privadas já configuradas na mesma instância. Origem exata permanece no manifesto privado, não foi substituída por uma instância fictícia. [Conferência de roteamento](routing-2026-11-17.json).

[Inventário real](preflight-2026-11-17-b.json): 14 tabelas paginadas, 40 chamadas GET; 11 usuários, 13 perfis, 24 listas, seis itens de lista e 2325 eventos no instante da captura. Os demais totais constam no relatório. IDs e hashes de cada registro ficam no baseline privado, sem persistir linhas completas, senhas, e-mails ou tokens. A captura é completa por paginação, mas não atômica entre tabelas; será reconferida antes de provisionar/mutar. Não inferir inconsistência de domínio apenas da diferença entre contagens de usuários/perfis.

Backup privado: `.local/shared-xano-preflight-20261117-b/contracts-without-env-records.xs`, exportado com `env=false/records=false`, SHA-256 `a499147e7226b49c8746ec812dff0978507d8e181e62e4ca82f3a273603c28f7`. Baseline: `baseline-hashes.json` no mesmo diretório. Primeira coleta restrita falhou com ConnectError e permanece no relatório `preflight-2026-11-17-a.json`; a coleta autorizada foi independente e não sobrescreveu a falha.

As rotas `GET lists/{id}` e `GET lists/public/{id}` ainda não estão publicadas. O relatório inicial registra corretamente essa reprovação. [Revisão do piloto por coleções](pilot-readiness-2026-11-17.json) confirma nove contratos já existentes para cadastro/login, coleções, atualização/remoção de listas e desativação de contas. Esta revisão não publica rotas nem conclui a change de UI. O piloto usa as coleções existentes para provar seus próprios critérios de persistência/autoria/privacidade; detalhes, busca nova e totais da UI continuam no escopo original de UI.

## Manifesto para revisão

Execução proposta: `cbshared_74089c52e9bb`. Manifesto privado `provisioning-reviewed.json`, SHA-256 canônico **`e6c2c84b2ea0f0692e16631d8b8e11e94314c1f6a60c323e6aaf0556423dcc5e`**.

1. Provisionamento, até oito chamadas de escrita: cadastrar dois membros novos, cada qual criando automaticamente perfil e duas listas padrão; tornar essas quatro listas padrão privadas como seus próprios donos; criar duas listas customizadas vazias da conta A, uma pública e uma privada. Nomes de usuário exatos serão `cbshared_74089c52e9bb_a` e `cbshared_74089c52e9bb_b`, e-mails sintéticos correspondentes em `example.invalid`, sem envio de mensagens. Senhas aleatórias e tokens somente no canal privado. Os oito registros criados automaticamente e as duas customizadas terão recibos com IDs reais e identidade/snapshot conferidos por leitura independente.
2. Validação, até duas chamadas de escrita: tentar alterar uma customizada de A com a sessão de B e exigir rejeição e preservação; mudar a lista pública para privada como A e reconferir persistência. Leituras como visitante/A/B conferem que a lista pública aparece, a privada não vaza e a coleção pessoal pertence ao usuário correto. Sem teste de carga, falha induzida ou alteração de conta anterior ao lote.
3. Limpeza, até quatro chamadas de escrita: excluir somente as duas customizadas vazias como A, após revalidar IDs/recibos/donos, ausência de itens e referências, e desativar os dois novos membros com administrador já existente. **Retenção esperada: oito registros de domínio** (dois usuários desativados, dois perfis, quatro listas padrão privadas) e auditoria. Não excluir contas, perfis, padrões ou auditoria, nem promover papel. Confirmar ausência das customizadas, retenção/estado dos demais e preservação dos registros anteriores. Dependência de terceiros ou resultado incerto interrompe a limpeza, sem retry cego.

Cada lote terá no máximo dez ações e revisão com prazo máximo de 30 minutos. O hash acima identifica a proposta de provisionamento; não é um plano executável com IDs nem substitui digest e aprovação dos lotes após recibos. Se o manifesto ou destino mudar, apresentar nova revisão. Publicação de contratos: zero. Alterações de registros de domínio anteriores ao lote: zero; autenticação e leituras do app podem acrescentar auditoria normal.

## Limites atuais e autorização necessária

**Não há IDs novos, recibos ou autorização de provisionamento.** O planejador offline não cria contas nem aceita PUTs de listas padrão; não será alterado para fingir que aceita essas ações. As etapas de cadastro/privatização exigem transporte específico e planejamento ativo complementar antes de implementação/execução, com revisão do lote concreto acima. A necessidade é preparar a evidência real de 2.1 e o futuro piloto de 2.2, não dispensar suas guardas.

O único administrador ativo encontrado ainda precisa autenticar pela interface privada e confirmar identidade antes de qualquer desativação. A aprovação da estratégia e “próxima change” não foram tratadas como aprovação deste lote mutável. Após aprovação do provisionamento, coletar recibos reais e então apresentar o lote com IDs exatos para revisão; manter 2.1 aberta até cumprir esses critérios. Browser, API, persistência e limpeza terão evidências separadas; nenhuma dessas etapas foi realizada nesta coleta.

## Validação local

Coletor `tools/shared_xano_preflight.py`: oito testes com transporte simulado aprovados, cobrindo hashes sem dados privados, IDs inválidos/duplicados, destino divergente, paginação incompleta/cíclica/com drift, rotas restritas e grupo/branch divergentes. Dezoito testes do planejador existentes aprovados. A revisão complementar de roteamento usa o descriptor real já coletado; o relatório bruto inicial preserva `branch_verified=false`, anterior a essa revisão. Testes simulados não são execução do piloto.
