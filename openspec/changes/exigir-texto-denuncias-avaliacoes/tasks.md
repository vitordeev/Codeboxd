## 1. Implementação local

- [x] 1.1 Exigir descrição na denúncia e crítica no formulário de avaliação, com trim e mensagem, antes de qualquer requisição.
- [x] 1.2 Ajustar HTML e contratos XanoScript preservando atalhos de status sem nota.
- [x] 1.3 Verificar ausente/vazio/espaços/texto válido, nota positiva por atalho, identidade e rascunho; executar regressões e compilação.

## 2. Integração

- [ ] 2.1 Publicar somente os dois contratos após backup e conferência de delta; validar rejeição remota sem criar registros inválidos.
- [ ] 2.2 Reiniciar app com rede e verificar formulário no navegador, registrando evidência e limites.

Implementação local: 269 testes e compile --dry passaram. Dois endpoints
publicados após backup de 78 documentos e dry-run limitado; export posterior
confirmou somente os dois arquivos alterados, referências de tabelas preservadas.
2.1 permanece aberta por falta de conta de teste disponível para rejeição autenticada.
Browser: 0/12 casos, falha no build/prerender por timeout, não no teste do formulário.
Usuário pediu retomar a otimização; pendências preservadas nesta change separada.
[Evidência](validation/implementacao-2026-10-20.md).
