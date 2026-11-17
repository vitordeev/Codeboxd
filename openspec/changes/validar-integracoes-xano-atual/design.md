## Context

Ver `proposal.md`. Workspace conhecido 147717, branch v1/live, Xano como autoridade de dados. A preparação isolada anterior permanece em 4/8, sem destino disponível. Existem guardas administrativos e ensaios exclusivamente locais; eles não serão convertidos silenciosamente em executores live. A última suíte tem 718 testes aprovados. Reflex 0.9.11.post1/.venv, sem Docker; TMDB, Kitsu, Open Library e identidade Jikan preservados.

## Goals / Non-Goals

Oferecer um caminho verificável de validação no backend existente e continuar ferramentas locais necessárias. Não reproduzir todo o Xano localmente, criar outro ambiente, comprar plano ou transformar simulação em aceite. Esta rodada implementa planejamento e verificação local; não inclui executor de transporte live nem publicação.

## Decisions

Atualização de execução em 17/11, tarefa 2.1: preparar coletor estritamente de leitura para backup sem env/records, inventário paginado independente e conferência dos contratos publicados do piloto. Gerar manifesto de provisionamento separado do plano mutável: duas contas novas via signup (cada uma cria perfil e duas listas padrão), duas listas customizadas vazias via API, testes de leitura com visitante/dono/outra conta, limpeza somente das customizadas e desativação das duas contas pelo administrador existente. Contas/perfis/listas padrão e auditoria ficam retidos, sem exclusão administrativa de contas. Ainda não existem IDs/recibos; não simular sua existência nem considerar o manifesto um lote executável/revisado pelo planejador. Provisionamento e executor live exigem lote e autorização concretos antes de implementação/execução, respeitando os limites anteriores.

1. Separar três camadas: testes de contrato/estado/concorrência/falha locais; inspeção remota e prévias sem publicação; piloto real pequeno sobre fixtures próprias após lote revisado. Nenhuma camada exige novo workspace.
2. Nova change substitui a intenção de provisionamento de `preparar-homologacao-xano-admin`. Os quatro itens remotos anteriores permanecem abertos como descontinuados; não são pré-requisitos da nova estratégia, não serão marcados entregues nem apagados. IDs/evidências e ferramentas isoladas permanecem históricos.
3. Ferramenta nova importa apenas hash/erro genéricos das guardas existentes e não altera suas restrições. Recebe JSON privado com destino, execução, baseline anterior, recibos, snapshots atuais e ações. Limite máximo dez ações; IDs positivos estritos, sem bool; run_id `cbshared_` + 12 hex; hashes SHA-256 canônicos.
4. Aceitar somente PUTs administrativos com os mesmos campos restritos pelas guardas existentes e DELETE de posts/listas próprios de fixtures. Reutilizar hash e projeção de identidade, mantendo as guardas históricas inalteradas; a ferramenta nova usa seu próprio namespace `cbshared_` e recusa alterar o próprio operador/admin. Para posts/listas, conferir dono em contas de fixture comprovadas e campos de identidade/markers. Proibir remoção de contas, env, schema e resets. Deletar fixtures de outras tabelas exige roteiro específico futuro.
5. Confirmar baseline anterior sem o ID e recibo de criação, além de snapshot atual; marcador por si é insuficiente. Comparação antes de executar pertence ao futuro transporte: planejamento offline não torna esses dados confiáveis por si. Digest do plano abrange todos os dados de entrada e destino. Aprovação vincula digest/referência/prazo; validade máxima de 30 min. Resultados públicos contêm contagens/hashes, sem registros ou payloads.
6. Ações de limpeza são operações separadas no mesmo manifesto e não são disparadas automaticamente. O planejador inicial permite DELETE apenas de post/lista com inventário explícito de referências vazio; dependentes, inclusive comentários/likes de terceiros, bloqueiam esse caso e exigem roteiro específico. Inspecionar relações reais antes da limpeza; auditoria permanece. Timeout de escrita exige reconciliação do ID exato, nunca retry cego. Nem aprovação válida do plano chama a rede nesta ferramenta.

## Risks / Trade-offs

- Mesmo no piloto, schema/contratos afetam todo o workspace: exigir backup e prévia restritos, compatibilidade e rollback antes de publicação. Não prometer isolamento por prefixo.
- Fixtures podem ser confundidas com dados anteriores: baseline, recibos e identidade completa devem vir de inventário independente. A ferramenta valida coerência, não descobre nem autentica a origem dos recibos.
- Proteção de tempo limita reuso de aprovação, mas não elimina TOCTOU: futuro executor precisa revalidar imediatamente antes de cada ação e verificar resultado após a chamada.
- Algumas provas de falha/concorrência não são adequadas ao live: executar localmente e preservar ensaio real de caminho feliz/autoria/privacidade, sem teste de carga.

## Migration Plan

Preparar artefatos; documentar supersessão e matriz por change; implementar ferramenta e regressões offline; gerar exemplo sintético sanitizado; validar OpenSpec e suíte. Retomar leituras/prévias pelos mecanismos existentes. Publicação e piloto real permanecem tarefas abertas até lote e dados concretos revisados. Rollback da estratégia preserva histórico e guardas; nunca exige reset do workspace.
