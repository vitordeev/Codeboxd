## 1. Feed

- [x] 1.1 Fixar a identidade da edição e manter referência opcional; verificar atualização do mesmo ID com/sem obra, troca/remoção da referência, falha, suspensão, envio repetido e imagem sem POST substituto.

## 2. Listas

- [x] 2.1 Substituir inclusão restrita ao catálogo carregado por busca de obras e inclusão explícita; verificar quatro tipos, persistência externa, lista própria, duplicatas, vazio/falha e resultado tardio.
- [x] 2.2 Adicionar seletor de listas próprias na ficha e confirmar inclusão da obra atual; verificar públicas/privadas, autoria, troca de ficha/conta, falha e preservação dos atalhos existentes.

## 3. Validação e evidências

- [x] 3.1 Executar regressões locais e compilação Reflex na .venv; registrar comandos/resultados e corrigir falhas pertinentes.
- [x] 3.2 Verificar feed/listas/ficha no navegador em desktop/celular com backend fictício, incluindo edição sem duplicatas e inclusão dos dois pontos; registrar evidências e limites sem confundir simulação com Xano real.
- [x] 3.3 Reconciliar documentação central e evidências, conferir checklist e validar a change OpenSpec; manter abertas verificações sem evidência.

Concluída em 22/10/2026 (6/6). 13 regressões específicas, suíte final de 298
testes e compilação aprovados. Navegador: oito cenários fictícios em produção
isolada, 1440/390px, sem erro JS ou overflow. Regressão original reproduzida
com serviços simulados. Nenhum contrato ou registro Xano alterado nesta change;
sem teste autenticado remoto nesta rodada. [Evidência completa](validation/implementacao-2026-10-22.md).
