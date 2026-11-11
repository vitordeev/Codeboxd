## 1. Preparação local

- [x] 1.1 Implementar gerador allowlist de contratos sem dados/env/envio, remover GUID/canonical herdados e verificar com testes e manifesto do pacote real.
- [x] 1.2 Implementar validação do destino protegido e configuração de exemplo separada; testar recusa de host/workspace da origem e configurações incompletas.
- [x] 1.3 Documentar comandos, evidências e limites; executar testes pertinentes, git diff --check e openspec validate preparar-homologacao-xano-admin --type change.

## 2. Ambiente remoto isolado

- [x] 2.1 Verificar disponibilidade de sandbox/workspace com credencial existente, registrando resultado sanitizado e distinguindo chamadas que criam recurso de leituras puras.
- [ ] 2.2 Obter ambiente isolado vazio no provedor sem alterar origem, resetar conteúdo existente ou adquirir plano; verificar identidade e estado vazio por leitura independente. Manter aberta se o provedor recusar.

## 3. Publicação e disponibilidade

- [ ] 3.1 Produzir dry-run limitado ao destino isolado vazio, sem records/env/delete/truncate; revisar delta exato e registrar a prévia antes de publicar.
- [ ] 3.2 Após aprovação específica da prévia, publicar contratos e verificar estrutura e ausência de registros copiados; não concluir por preparação local.
- [ ] 3.3 Configurar acesso privado separado e verificar rotas/grupos/proteções do backend de homologação sem dados reais; atualizar acompanhamento e executar validação OpenSpec.

O piloto de dados e a conta administrativa sintética pertencem às fases A2–A4
de gerenciamento-website após a disponibilidade do destino; não são executados
automaticamente por esta preparação. Sem push, merge, sincronização ou arquivo.

Evidência atual: [validation.md](validation.md). Preparação local 32 documentos,
sete testes específicos e 573 na suíte aprovados. Sandbox HTTP 500 e criação de
workspace HTTP 403/ERROR_CODE_ACCESS_DENIED; destino isolado não disponível pela
credencial atual. Não presumir plano contratado nem marcar 2.2/3.x por simulação.
