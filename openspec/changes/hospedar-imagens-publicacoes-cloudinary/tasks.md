## 1. Preparação autorizada

**Replanejamento solicitado — somente documentação:** marcos originais 1.1–1.3
concluídos e 2.1/2.2 abertos, preservados. Subtarefas abaixo tornam o esforço
restante explícito; contagem expandida não mede percentual nem nova entrega.
Proposta/design/specs atualizados aguardam aprovação junto à change UI/UX.
Nenhum teste remoto ou implementação foi executado nesta rodada de planejamento.

11/11/2026, continuação local de 2.1: [contrato candidato e endurecimento do recibo](contrato-integracao-2026-11-11.md).
Assinatura/versão/URL verificadas e payload vinculado ao autor implementado no
adaptador; 18 testes Cloudinary e suíte completa de 632 testes aprovados.
Persistência durável, endpoints, integração SocialState e publicação continuam
pendentes; nenhum checkbox funcional adicional concluído. Flag false.

11/11/2026, ensaio real autorizado e executado: [resultado](ensaio-real-2026-11-11.md).
Upload/download/limpeza HTTP 200; bytes idênticos e exclusão confirmada pela API.
Zero chamadas Xano, sem alterar flag ou dados existentes. Mantido 3/5 porque
persistência e ciclo de vida integrados continuam pendentes. A prévia abaixo
registra o estado histórico antes dessa autorização.

11/11/2026, após preenchimento: [conta Free validada por leitura e prévia do ensaio](preflight-cloudinary-2026-11-11.md).
GET /usage HTTP 200, 0/25 créditos e nenhum recurso reportado. Flag false.
Executor opt-in preparado com seis testes simulados aprovados, sem execução
remota. A ausência de credenciais abaixo descreve a rodada anterior.

11/11/2026, continuação: [cotas, alternativa R2 e revisão de configuração](limites-alternativas-2026-11-11.md).
22 testes locais aprovados novamente. Usuário informou preenchimento, mas os
valores não foram localizados nos .env das worktrees; caminho solicitado.
Plano/consumo da conta ainda não consultados. Integração e ativação mantidas abertas.

11/11/2026: [revisão de prontidão e testes](aceite-2026-11-11.md). Credenciais
locais ausentes, flag false e contrato externo de post ainda incompleto.
22 testes locais passaram; nenhum asset real acessado ou alterado. Mantido 3/5.

- [x] 1.1 Preparar variáveis privadas ausentes, exemplos sem valores e flag desativada, verificar presença/ignore sem expor segredos e pip check na .venv.
- [x] 1.2 Implementar adaptador assinado com guardas e erros sanitizados; verificar configuração, assinatura/transporte, limites e respostas com testes simulados sem rede real.
- [x] 1.3 Registrar uso e limites, validar OpenSpec e git diff --check.

Evidências em [validation.md](validation.md), configuração em [setup.md](setup.md). Preparação 3/3 concluída; integração/ativação 2.1/2.2 pendentes.

## 2. Integração e ativação posteriores

Incremento local planejado de 2.1: verificar recibo Cloudinary (assinatura,
versão e URL canônica do mesmo asset), preparar payload vinculado ao autor e
regressões contra URL/assinatura adulterada, dono diferente e identidade inválida.
Documentar contrato futuro e reconciliação; não conectar posts a metadados sem
validação independente no Xano nem marcar 2.1 completo por esse incremento.

Preparação incremental de 2.1/2.2: credenciais agora presentes e GET /usage
autenticado (Free, 0/25 créditos). Preparar executor opt-in de um PNG sintético,
recuperação por HTTPS e exclusão somente do asset criado nessa execução, com
journal privado anterior ao envio e sem retries de escrita. Validar com mocks;
execução remota aguarda autorização específica da prévia. Não conclui 2.1/2.2
nem ativa posts. Evidências: limites-alternativas-2026-11-11.md e
preflight-cloudinary-2026-11-11.md.

- [ ] 2.1 Com credenciais, detalhar e publicar contrato aditivo de URL/asset/provedor no Xano após backup/prévia, integrar criar/editar/excluir e compensação/reconciliação; testar autoria e legados.
- [ ] 2.2 Ativar configuração somente após ensaio real de upload/post/feed/substituição/exclusão e limpeza em conta/asset descartáveis, sem marcas do processamento Xano em imagens novas.

### Desdobramento de 2.1 — contrato, ciclo de vida e publicação

Cada subtarefa inclui testes e evidência no mesmo lote. 2.1 só é concluída após
validar o conjunto; aprovação documental não autoriza seus passos remotos.

- [ ] 2.1.1 Preparar localmente campos aditivos de post e registro durável de asset, índices/constraints e retenção do design; verificar fixtures legadas, ausência de cascata do journal e invariantes de propriedade/estado em testes, documentando contratos sem publicar.
- [ ] 2.1.2 Implementar localmente reserva e consulta por operação com sessão atual/conta ativa/autoria; testar visitante, conta desativada, sessão de recuperação, dono divergente, troca de editor/conta e reinício recuperável, registrando recibos sanitizados.
- [ ] 2.1.3 Adaptar upload à identidade reservada e implementar verificação independente server-side de assinatura/recurso/versão; testar replay, URL/asset_id/formato adulterados, limite 5 MiB, quota/429 e resposta incompleta, documentando escopo privado do verificador.
- [ ] 2.1.4 Implementar commit idempotente de criação com imagem e criação sem anexo; testar dois commits da mesma reserva, falha entre upload/commit, post sem Cloudinary e reconciliação após timeout/5xx sem duplicar, documentando estados e erros.
- [ ] 2.1.5 Implementar edição preservadora, substituição e remoção explícita de imagem com revisão atômica; testar concorrência, imagem antiga preservada na falha, corpo/obra/spoiler sem reupload e compatibilidade legada, registrando a matriz de comportamentos.
- [ ] 2.1.6 Integrar exclusão do post à fila durável sem destruir antecipadamente arquivos ou journal; testar transação, referências restantes, timeout da remoção e permissões de outra conta, preservando comentários/likes conforme regra existente e documentando limites.
- [ ] 2.1.7 Preparar executor supervisionado de reconciliação/prévia/limpeza com carência e limite propostos; testar identidade/propriedade/versão/referências/estado antes da execução, prévia envelhecida, resultado incerto e rejeição de legado/URL arbitrária; manter execução real bloqueada sem aprovação do lote.
- [ ] 2.1.8 Conectar localmente staging, salvar/remover e leitura de posts/feed ao contrato externo compatível, mantendo flag false; testar rascunho, invalidação de cache, editor/sessão tardios, rollback de leitura e ausência de fallback silencioso, compilando conforme skill Reflex e documentando a integração local.
- [ ] 2.1.9 Com destino disponível e aprovação específica, revisar backup/dry-run exato e configuração privada, publicar somente contratos aprovados no Xano e verificar schema/guards/projeções/legados por leitura independente; registrar IDs e limites sem copiar segredos ou dados reais. Manter aberta se não houver ambiente/autorização.

### Desdobramento de 2.2 — aceite e liberação

- [ ] 2.2.1 Após autorização do cenário e das fixtures, executar API integrada com duas contas controladas nos onze fluxos do design, incluindo falhas/concorrência/retomada e todos os candidatos próprios à limpeza; registrar resultados reais, autoria e retenção, sem inferir entrega por mocks.
- [ ] 2.2.2 Validar no navegador posts mistos/legados e externos, ausência de imagem, edição/substituição/remoção, foco/rascunho e feedback em 390/1440px; verificar imagem recuperada após nova sessão e rollback de uploads, distinguindo frontend, API e CDN.
- [ ] 2.2.3 Revisar cotas e pendências duráveis, confirmar limpeza autorizada/retidos, obter aprovação específica de ativação e aplicar flags somente após critérios completos; testar rollback preservando leitura/journal, revisar diff e validar esta change antes de recomendar conclusão.

## Workflow follow-up

- Aguardar aprovação das duas changes antes de iniciar implementação.
- Não fazer push, merge, sincronização de specs ou arquivamento nesta rodada.
- Manter abertas verificações de Xano/conta/limpeza/navegador sem evidência própria;
  o PNG descartável e os 632 testes anteriores não substituem aceite integrado.
