## 1. Reformulação autorizada

- [x] 1.1 Reconciliar a estratégia anterior como supersedida, preservar seus IDs e evidências e documentar matriz por change sem obrigar novo workspace; verificar os artefatos e os apontadores centrais.
- [x] 1.2 Implementar planejador local de lote no workspace atual com destino exato, baseline, recibos, snapshots, limite, digest e prazo; testar rejeição de alvo preexistente, destino ambíguo, conta protegida, payload/fixture alterados e aprovação expirada.
- [x] 1.3 Preparar CLI offline e exemplo sintético sanitizado; verificar saída sem dados privados, nenhuma chamada de rede e nenhum efeito remoto mesmo com aprovação válida.
- [x] 1.4 Executar regressões pertinentes, suíte local, validação OpenSpec e revisão de diff; registrar evidências e limitações sem concluir aceite remoto por mocks.

## 2. Aceite remoto no destino existente

Retomada de 17/11: [prévia concreta do piloto](piloto-revisao-2026-11-17.md), backup sem env/records, inventário real de 14 tabelas e roteamento v1/live conferidos. Coletor de leitura com oito testes novos e 18 regressões do planejador aprovados. Detalhes de listas ainda não publicados; piloto proposto usa coleções existentes. Sem criação de fixtures, IDs/recibos ou aprovação mutável; 2.1 parcialmente preparada e 2.2 não executada, **4/6** preservado.

- [ ] 2.1 Preparar lote real com backup de contratos, inventário independente, recibos de fixtures, IDs/destino e limpeza revisados; apresentar prévia e aprovação do lote antes de publicação ou mutação. Não exige outro workspace.
- [ ] 2.2 Após aprovação concreta, executar piloto limitado de persistência/autoria/privacidade no Xano atual e verificar limpeza e auditoria; registrar API/navegador/limpeza separadamente e manter aberta a verificação sem evidência.
