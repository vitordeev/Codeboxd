## 1. Contratos e implementação

- [x] 1.1 Inventariar rotas/emissores remotos e confirmar delta mínimo, registrando cobertura e backup privado sem valores nos relatórios.
- [x] 1.2 Implementar versão por conta, claims e guarda em todas as rotas protegidas; validar cobertura local, finalidade e preservação das verificações existentes.
- [x] 1.3 Implementar atualização atômica de senha/versão e captura da versão na recuperação; validar corrida/reuso e caminhos de erro.

## 2. Publicação e validação

- [x] 2.1 Executar dry-run sem exclusões, revisar escopo por operação e publicar somente o delta previsto; conferir export remoto publicado.
- [x] 2.2 Comprovar remotamente rejeição de tokens legados/anteriores, login novo, troca e outra conta preservada, incluindo acessos diretos de leitura/mutação e finalidade de recuperação, sem dados sociais alterados incidentalmente.
- [x] 2.3 Executar testes locais relevantes e navegador, reconciliar a tarefa 2.3 da change de credenciais, documentos centrais e validar ambas as changes; fornecer comandos de commit/push sem executá-los.

## Evidências — 26/10/2026

- 1.1: remote-inventory.json, 78 documentos e 39 queries autenticadas, três emissores; baseline privado sem env/records em .local/session-revocation.
- 1.2: guarda em 39 rotas publicadas e 40 locais (inclui /likes local não publicado); claims nos três emissores; quatro testes locais específicos executam a política JavaScript real e verificam cobertura e ordem transacional.
- 1.3: remote-validation.json, alteração concorrente com exatamente um sucesso e uma rejeição; sessão anterior e credencial de recuperação usadas rejeitadas. Código de recuperação captura a versão sob transação.
- 2.1: preview.json, deployment.json e published-inspection.json: tabela aditiva, uma função nova, 42 queries atualizadas; 40 chamadas de guarda; zero documentos alheios alterados e única adição prevista. Nenhum env, record, delete ou truncate importado.
- 2.2: 29 checks remotos aprovados, incluindo outra conta preservada e finalidade de recuperação; geração de código por função privada sem e-mail. unusable-account-inspection.json confirma quinta identidade histórica ausente, sem exclusão executada nesta rodada.
- 2.3: 392 testes locais aprovados; browser-validation.json passou para token legado → login e sessão nova → conta/biblioteca. Checklists e documentos centrais reconciliados; comandos manuais em manual-git.md. Nenhum git add, commit ou push executado no projeto.
