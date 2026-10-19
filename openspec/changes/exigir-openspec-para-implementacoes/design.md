## Context

The repository already uses OpenSpec changes to capture proposals, specifications, designs, and implementation tasks. `AGENTS.md` currently contains project-specific Reflex setup guidance but does not require contributors to associate implementation work with an active change. See `proposal.md` for the motivation and scope.

## Goals / Non-Goals

**Goals:**
- Put a concise, durable workflow rule in the repository guidance that applies to future coding and maintenance work.
- Define how to proceed when a request is not covered by an existing active change.
- Make implementation completion include task status and relevant validation evidence.

**Non-Goals:**
- Change application features, runtime behavior, or OpenSpec CLI conventions.
- Rewrite or replace the existing Reflex-specific instructions.
- Require OpenSpec artifacts for questions, investigations, or other work that does not modify the project.

## Decisions

- Add a clearly separated OpenSpec workflow section to `AGENTS.md`, outside the Reflex-managed block. This file is already the repository's agent guidance and is referenced by the local workflow.
- Before editing code, identify an active change that covers the requested scope; if none does, create a new change with the OpenSpec CLI and prepare its required planning artifacts.
- Keep implementation tasks and validation evidence in that change's `tasks.md`, updating checkboxes only when the work and its evidence are complete.
- Treat documentation and configuration edits that implement the agreed request as implementation work and track them in the change; do not require a new change for unrelated read-only investigation.
- Preserve existing changes and do not broaden a change's scope silently. If work discovered during implementation falls outside its change, pause that work and create a separate change.

## Risks / Trade-offs

- [Small maintenance requests may feel heavier] → Reuse an existing change when it already covers the work; otherwise use a concise change rather than bypassing tracking.
- [Concurrent contributors may update the same tasks] → Check current change status and worktree before editing, and avoid overwriting unrelated changes.

## Migration Plan

Add the workflow guidance to `AGENTS.md`, validate the OpenSpec change, and use the rule for subsequent implementation requests. Rollback consists of reverting only the added guidance section if the project later adopts a different workflow.
