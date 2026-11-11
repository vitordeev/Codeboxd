## 1. Preparação autorizada

11/11/2026: [revisão de prontidão e testes](aceite-2026-11-11.md). Credenciais
locais ausentes, flag false e contrato externo de post ainda incompleto.
22 testes locais passaram; nenhum asset real acessado ou alterado. Mantido 3/5.

- [x] 1.1 Preparar variáveis privadas ausentes, exemplos sem valores e flag desativada, verificar presença/ignore sem expor segredos e pip check na .venv.
- [x] 1.2 Implementar adaptador assinado com guardas e erros sanitizados; verificar configuração, assinatura/transporte, limites e respostas com testes simulados sem rede real.
- [x] 1.3 Registrar uso e limites, validar OpenSpec e git diff --check.

Evidências em [validation.md](validation.md), configuração em [setup.md](setup.md). Preparação 3/3 concluída; integração/ativação 2.1/2.2 pendentes.

## 2. Integração e ativação posteriores

- [ ] 2.1 Com credenciais, detalhar e publicar contrato aditivo de URL/asset/provedor no Xano após backup/prévia, integrar criar/editar/excluir e compensação/reconciliação; testar autoria e legados.
- [ ] 2.2 Ativar configuração somente após ensaio real de upload/post/feed/substituição/exclusão e limpeza em conta/asset descartáveis, sem marcas do processamento Xano em imagens novas.
