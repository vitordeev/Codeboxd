## 1. Implementação local

- [x] 1.1 Exigir descrição na denúncia e crítica no formulário de avaliação, com trim e mensagem, antes de qualquer requisição.
- [x] 1.2 Ajustar HTML e contratos XanoScript preservando atalhos de status sem nota.
- [x] 1.3 Verificar ausente/vazio/espaços/texto válido, nota positiva por atalho, identidade e rascunho; executar regressões e compilação.

## 2. Integração

- [x] 2.1 Publicar somente os dois contratos após backup e conferência de delta; validar rejeição remota sem criar registros inválidos.
- [x] 2.2 Reiniciar app com rede e verificar formulário no navegador, registrando evidência e limites.

Implementação local: 269 testes e compile --dry passaram. Dois endpoints
publicados após backup de 78 documentos e dry-run limitado; export posterior
confirmou somente os dois arquivos alterados, referências de tabelas preservadas.
2.1 permanece aberta por falta de conta de teste disponível para rejeição autenticada.
Browser: 0/12 casos, falha no build/prerender por timeout, não no teste do formulário.
Usuário pediu retomar a otimização; pendências preservadas nesta change separada.
[Evidência](validation/implementacao-2026-10-20.md).

Retomada 21/10: 12/12 casos de navegador aprovados em produção isolada, com
backend fictício, quatro tipos e 1440/390px; app existente em 3000 preservado.
18 testes pertinentes passaram. 2.2 concluída na camada de interface; 2.1
continua aberta por falta de login para rejeição autenticada na API real.
Estado atual 4/5. [Resultado e limites](validation/retomada-2026-10-21.md).

Retomada adicional em 21/10: preparado `tools/required_content_remote.py` para
oito rejeições autenticadas (ausente/null/vazio/espaços nos dois endpoints),
com leitura e comparação em memória dos registros antes/depois, sem registrar
credenciais ou conteúdo privado. Arquivo histórico de contas continua ausente;
aguarda autenticação privada de conta de teste. `--help`, validação OpenSpec
e `git diff --check` passaram. A API real não foi executada nesta retomada;
2.1 permanece aberta e a change continua em 4/5. Não houve republicação.

Continuação: executor recebeu `--interactive-login`, com janela local de senha
oculta e sessão mantida em memória. Janela iniciada e aguardando login manual;
`--help`, OpenSpec e diff verificados novamente. Login pendente não constitui
evidência de execução remota; não encerrar 2.1 antes do relatório aprovado.

Conclusão em 21/10 (22/10 UTC): login manual realizado e oito rejeições reais
aprovadas, HTTP 400 com erro de entrada pertinente, para ausente/null/vazio/
espaços em POST reports e PUT interactions com nota 4,5. Comparação de todos
os registros paginados antes/depois confirmou report e user_media_interaction
inalterados. Sem republicação ou limpeza de dados. Change concluída em 5/5.
[Evidência final e comandos](validation/conclusao-api-real-2026-10-21.md).
