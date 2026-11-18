## Reconciliação do run interrompido

- [x] 1. Confirmar por leitura as identidades de 50/51, listas 125/126, zero referências e estado privado; abortar em divergência.
- [x] 2. Excluir listas 125/126, desativar contas 51/50, verificar preservação das linhas não alvo e os eventos administrativos.
- [x] 3. Registrar recibos e limitações na change funcional; validar ambas as changes OpenSpec.

Evidência: cleanup-execution-after-read-429.json registra duas exclusões HTTP 200; admin-resume-execution.json confirma ausência das listas, preservação de todo o restante, desativação 50/51 e dois eventos administrativos. A primeira reconciliação parou sem escrita após 429 de leitura; a retomada espaçada não repetiu exclusões.