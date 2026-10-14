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

- Antes de alterar arquivos, ler `openspec/README.md` e os documentos centrais pertinentes; identificar a change ou pendência relacionada ao trabalho.
- Alterações de código, configuração, infraestrutura e documentação devem ter contexto e resultado registrados em `openspec/`, na change correspondente ou nos documentos centrais, conforme o escopo.
- Atualizar tarefas e evidências na mesma rodada, distinguindo implementação local, testes simulados, validação remota e navegador. Não marcar como concluído o que depende de verificação.
- Centralizar a documentação de acompanhamento em `openspec/`; referenciar e reconciliar documentos técnicos existentes fora dela quando afetados.
- Preservar histórico e IDs. Evoluções posteriores de changes arquivadas devem ser acompanhadas por trabalho ativo, sem sobrescrever silenciosamente a entrega histórica.
- Esta regra exige vínculo documental com OpenSpec; arquivos de implementação continuam nos diretórios próprios do projeto.

## Execução local sem Docker

Por decisão explícita do usuário, manter execução local com `.venv`, sem introduzir, iniciar ou utilizar Docker nesta etapa. Não tratar testes Docker como pendência obrigatória. Registrar qualquer mudança dessa decisão em `openspec/`.
