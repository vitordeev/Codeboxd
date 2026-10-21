<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** � up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above � do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs � components, state management, events, styling, database, routing, authentication � use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available � always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->

## Registro obrigatório no OpenSpec

Por orientação do usuário, toda modificação no projeto deve estar relacionada ao OpenSpec. A pasta `openspec/` centraliza planejamento, tarefas, decisões, contexto, evidências e pendências.

- Antes de qualquer implementação ou ajuste, ler `openspec/README.md` e os documentos centrais pertinentes e identificar uma change ativa que cubra o trabalho, com planejamento e tarefas definidos antes de editar arquivos.
- Se nenhuma change ativa cobrir o pedido, criar uma nova com `openspec new change <nome>` e preparar os artefatos exigidos pelo schema antes da implementação. Não usar uma change arquivada como autorização para trabalho novo.
- Perguntas, análises e investigações somente de leitura não exigem criar uma change. Quando a investigação levar a alterações de código, configuração, infraestrutura ou documentação, vincular essas alterações a uma change ativa antes de editar.
- Alterações de código, configuração, infraestrutura e documentação devem ter contexto e resultado registrados em `openspec/`, na change correspondente ou nos documentos centrais, conforme o escopo.
- Atualizar `tasks.md` e as evidências da change na mesma rodada, distinguindo implementação local, testes simulados, validação remota e navegador. Marcar uma tarefa como concluída somente quando seus critérios tiverem evidência; manter abertas verificações não executadas ou sem acesso.
- Centralizar a documentação de acompanhamento em `openspec/`; referenciar e reconciliar documentos técnicos existentes fora dela quando afetados.
- Preservar histórico e IDs. Evoluções posteriores de changes arquivadas devem ser acompanhadas por trabalho ativo, sem sobrescrever silenciosamente a entrega histórica.
- Esta regra exige vínculo documental com OpenSpec; arquivos de implementação continuam nos diretórios próprios do projeto.

## Execução local sem Docker

Por decisão explícita do usuário, manter execução local com `.venv`, sem introduzir, iniciar ou utilizar Docker nesta etapa. Não tratar testes Docker como pendência obrigatória. Registrar qualquer mudança dessa decisão em `openspec/`.
