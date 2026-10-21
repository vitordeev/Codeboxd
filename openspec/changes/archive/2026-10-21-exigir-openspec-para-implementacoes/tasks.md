## 1. Repository workflow guidance

- [x] 1.1 Add an OpenSpec workflow section to `AGENTS.md` outside the Reflex-managed block and verify it requires an active covering change before any implementation edits.
- [x] 1.2 Document creating a new OpenSpec change when no active change covers the request and verify the rule distinguishes implementation from read-only investigation.

## 2. Completion and validation

- [x] 2.1 Document tracking implementation tasks and validation evidence in the change and verify checkboxes are completed only when supported by evidence.
- [x] 2.2 Validate the OpenSpec change and verify the workflow instructions do not alter application behavior or existing Reflex requirements.

4/4 verificadas em 21/10. [Evidências](validation/conclusao-2026-10-21.md).
## Validation evidence — 2026-10-19

- Added `OpenSpec workflow` after the Reflex-managed end marker in `AGENTS.md`.
- Reviewed coverage: active change before implementation, documentation/configuration included, read-only investigation exempt, CLI scaffolding and planning required when no covering change exists, task tracking with validation evidence, and separate changes for work outside the selected scope.
- Compared the Reflex-managed content against `git show HEAD:AGENTS.md`, normalizing only line endings: unchanged. Confirmed the new section appears after the managed block and explicitly preserves all Reflex requirements.
- `openspec validate exigir-openspec-para-implementacoes --type change --strict`: passed. `skip_specs: true` is intentional because this changes contributor guidance only.
- `git diff --check -- AGENTS.md openspec/changes/exigir-openspec-para-implementacoes`: passed.
- Only repository guidance and this task/evidence document were edited in this step. No application, API, dependency, or runtime configuration changes were made; application tests and compilation were not repeated for this documentation-only change.
- The change remains available for review; synchronization is unnecessary because it has no delta specs. Archiving was not performed in this step.
