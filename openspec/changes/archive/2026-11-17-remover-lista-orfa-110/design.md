## Context

See `proposal.md`. A current read-only inventory identifies the candidate row; its public state, zero owner, empty text fields and creation timestamp are recorded separately. The Xano metadata API supports the same row-level `PUT`/`DELETE` routes used by existing project tools.

## Goals / Non-Goals

**Goals:** ensure the candidate has not changed, prove there are no list items referencing it, issue exactly one row-level delete, and verify all other list/item records remain unchanged.

**Non-Goals:** change application contracts, alter privacy or ownership of other rows, remove accounts/profiles/default lists, or retry an uncertain delete.

## Decisions

- Use the live metadata API for only table `user_list` row `110`, because the app has no owner session for `user_id=0`. Before deleting, compare the current row digest with the captured post-reconciliation baseline and verify exact expected fields.
- Read the complete `user_list_item` table and require no `list_id=110` references. A missing or incomplete read stops the operation.
- Write a local intent receipt before DELETE. Accept only a successful response, then read again and require row 110 absent, every other list hash unchanged, and every item hash unchanged.
- On timeout, unexpected response or failed verification, stop without retry. Keep the report free of row payloads, credentials and tokens.

## Risks / Trade-offs

- A concurrent edit between preflight and DELETE can invalidate the snapshot. Re-read the exact row and references immediately before the single request; any difference aborts.
- Metadata deletion does not create the app's `event_log` audit record. Preserve a local OpenSpec receipt containing time, row ID, request status and before/after hashes.

## Migration Plan

Capture exact row/reference state, issue one DELETE, verify absence and preservation. No rollback is attempted: restoring an orphan with `user_id=0` could recreate the public artifact; if verification is ambiguous, stop and report it.
