## Context

Consulte `proposal.md` para a motivação e o escopo. A revisão de 14/11/2026 encontrou sete changes funcionais ativas, mas os resumos centrais ainda exibem valores antigos. Os checklists atuais totalizam 47 tarefas concluídas e 64 abertas, em 111 tarefas. A própria change documental criada para reconciliar esses registros não deve entrar nesses totais funcionais.

## Goals / Non-Goals

**Goals:**

- Apresentar um único quadro atual das sete changes funcionais, com números obtidos de seus checklists.
- Registrar bloqueios como bloqueios, com referências às evidências mais recentes e sem transformar preparação ou simulação em aceite.
- Preservar registros históricos, IDs, estados das tasks e a separação entre validação local, simulada, remota e de navegador.

**Non-Goals:**

- Fechar tarefas, sincronizar requisitos funcionais, arquivar changes ou resolver os bloqueios externos.
- Alterar código, contratos Xano, dados, credenciais, branches ou configuração de execução.
- Atualizar resumos históricos datados como se fossem estado atual.

## Decisions

1. **Fonte de verdade por tipo de informação:** usar `openspec list --json` para identificar changes ativas e estado do CLI; usar o `tasks.md` de cada change para as contagens; consultar evidências recentes para explicar pendências e bloqueios. Se houver divergência, registrar e investigar em vez de ajustar checkboxes para fazer os números coincidirem.
2. **Escopo do quadro:** incluir as sete changes funcionais presentes na linha de base desta reconciliação. Excluir do total funcional a change documental `reconciliar-estado-changes-abertas`, evitando contagem circular; ela será acompanhada pelo próprio checklist e status OpenSpec.
3. **Atualização cirúrgica:** editar somente os resumos de estado atual em `README.md`, `CONTEXTO.md`, `PENDENCIAS.md` e `RELATORIO_STATUS.md`. Preservar texto histórico, links e evidências; substituir somente tabelas e passagens atuais contraditas pelas fontes de verdade.
4. **Tratamento de bloqueios:** representar separadamente dependências de conta/caixa e credencial de recuperação, autenticação de domínio de e-mail e ambiente Xano isolado. Não executar pedidos de recuperação, escritas remotas ou configuração externa durante esta reconciliação.
5. **Sem delta de especificação:** os documentos descrevem estado e evidência, não comportamento do produto. Por isso, `.openspec.yaml` declara `skip_specs: true`; não será inventado requisito funcional para esta mudança documental.

## Risks / Trade-offs

- **Um checklist ou evidência pode mudar durante a atualização** → reconsultar `openspec list --json`, os sete `tasks.md` e as evidências citadas imediatamente antes de editar; manter data de corte explícita.
- **Resumos históricos podem parecer atuais por estarem no topo de documentos longos** → inserir data/identificação de estado atual e preservar as entradas datadas sem reescrevê-las.
- **A mudança documental aparece como uma change ativa adicional no CLI** → excluí-la explicitamente dos totais de trabalho funcional, mas não ocultá-la do status OpenSpec.
- **Diferença entre aceite local e remoto pode ser apagada por síntese curta** → manter bloqueadores e limites explícitos no quadro, com links para a evidência específica.

## Migration Plan

1. Antes de editar, verificar `git status --short` e garantir que as alterações pré-existentes permaneçam intactas.
2. Revalidar os números e os bloqueios pela fonte de verdade e atualizar somente as quatro seções centrais definidas na proposta.
3. Conferir os totais contra os checklists, verificar os links locais citados, revisar o diff e executar `openspec validate reconciliar-estado-changes-abertas --type change`.
4. Se a atualização introduzir erro, reverter apenas os hunks desta change, sem substituir arquivos inteiros nem afetar alterações preexistentes.

Não há implantação ou alteração remota nesta mudança.
