## 1. Proteção de arquivos

- [x] 1.1 Criar regras de ignore e retirar arquivos privados/gerados do índice sem apagar cópias locais; verificar lista rastreada vazia e hashes locais preservados.
- [x] 1.2 Verificar existência de arquivos privados no histórico compartilhado sem imprimir valores; registrar ação externa necessária em relatório sem segredos.

## 2. Ambiente e erros de upload

- [x] 2.1 Padronizar `.venv`, fixar dependências diretas e documentar setup; verificar imports, versões e `pip check`.
- [x] 2.2 Corrigir mensagens do transporte de upload; verificar erros de rede, HTTP e resposta inválida com testes controlados.
- [x] 2.3 Corrigir a URL de banner no backend; testar URL concreta, arquivo salvo e limpeza após falha de API.

## 3. Escopo retirado por decisão do usuário

Os IDs 3.1 (volume Docker) e 3.2 (recriação de contêiner) foram retirados do checklist por pedido explícito do usuário para continuar sem Docker. Os ajustes desta rodada em Dockerfile/Compose foram revertidos. Esses itens não são entregas concluídas; o histórico permanece no relatório.

## 4. Validação e contexto

- [x] 4.1 Executar suíte completa, compilação Reflex e validação OpenSpec; registrar resultados e limites.
- [x] 4.2 Atualizar contexto, relatório, pendências e checkpoints atuais com as correções e ações restantes; verificar links locais e diff sem erros.

## Evidência e tarefa restante

7/7 tarefas do escopo atual concluídas. [Relatório](validation/correcoes-2026-10-13.md) e [resultados](validation/results-2026-10-13.json) registram as verificações. Docker foi excluído do escopo por decisão do usuário; o teste de recriação não será executado. Administração, rotação de credenciais antigas e testes remotos continuam nos respectivos tópicos de `openspec/PENDENCIAS.md`.
