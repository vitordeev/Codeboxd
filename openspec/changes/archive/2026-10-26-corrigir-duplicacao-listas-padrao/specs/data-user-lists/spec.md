## ADDED Requirements

### Requirement: Idempotent default list preparation
The system SHALL maintain one default list of each standard type per owner when preparing missing default lists, including concurrent requests. Existing custom lists and their items SHALL be preserved.

#### Scenario: Concurrent preparation
- **WHEN** concurrent requests prepare the same owner's default lists
- **THEN** each standard type SHALL resolve to a single persisted list for that owner

#### Scenario: Defaults outside the first page
- **WHEN** an owner's default list exists beyond the first page of results
- **THEN** preparation SHALL reuse it without creating another list

### Requirement: Non-destructive default list reconciliation
The system SHALL reconcile confirmed duplicate default lists only from a reviewed backup and owner-scoped plan, preserving the union of media items, custom lists and privacy. Without confirmed duplicates it SHALL perform no cleanup writes.

#### Scenario: No persisted duplicates
- **WHEN** inspection finds no duplicate default lists for an owner
- **THEN** reconciliation SHALL leave the owner's data unchanged

#### Scenario: Confirmed duplicates
- **WHEN** an approved reconciliation merges duplicate defaults
- **THEN** all distinct media items SHALL remain accessible in the canonical list without changing ownership or exposing private content
