## Why

Implementation work can otherwise begin without an agreed scope or leave code changes disconnected from project decisions. Requiring an active OpenSpec change for every implementation or adjustment makes the scope, acceptance criteria, and completion status reviewable before work proceeds.

## What Changes

- Establish a repository-level workflow rule that every code implementation, bug fix, or behavioral adjustment must be covered by an active OpenSpec change before editing application code.
- Require creation of a new OpenSpec change when no active change covers the requested work.
- Require implementation tasks to be tracked and completed in that change, with validation evidence updated before considering the work finished.
- Record this as a contributor/agent process rule; it does not change application behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None.

## Impact

- Repository contribution guidance (`AGENTS.md`) and the OpenSpec workflow used by contributors and coding agents.
- No application APIs, runtime behavior, or dependencies change.
- This is a process/documentation change and intentionally has `skip_specs: true`.
