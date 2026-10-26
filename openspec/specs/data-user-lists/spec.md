# data-user-lists Specification

## Purpose

Definir a persistência de listas personalizadas criadas pelos usuários e dos itens de mídia associados a cada lista.

## Requirements

### Requirement: User list persistence

The system SHALL persist custom lists created by users.

#### Scenario: Creating a custom list

- **WHEN** a user creates a valid custom list
- **THEN** the system SHALL persist the list with its owner

### Requirement: List item persistence

The system SHALL persist the relationship between a list and each media item added to it.

#### Scenario: Adding media to a list

- **WHEN** a user adds a media item to one of their lists
- **THEN** the system SHALL persist the relationship between the list and the media item

### Requirement: Unique list entries

The system SHALL prevent the same media item from being persisted more than once in the same list.

#### Scenario: Duplicate media in a list

- **WHEN** a user attempts to add an existing media item to the same list
- **THEN** the system SHALL prevent the duplicate list entry

### Requirement: List ownership persistence

The system SHALL preserve the ownership relationship between a user and each list created by that user.

#### Scenario: Retrieving user lists

- **WHEN** lists belonging to a user are requested
- **THEN** the system SHALL return the lists associated with that user

### Requirement: Default lists at signup

The system SHALL create two empty lists owned by every new user: "Quero ver / ler" and "Já assisti / li", atomically with signup.

#### Scenario: New account

- **WHEN** a user completes signup
- **THEN** the account SHALL own both empty default lists before signup succeeds

### Requirement: One-time authorized list reset

The migration SHALL back up existing lists and entries before deleting them and SHALL recreate the two empty default lists for every existing user, without changing media or interactions.

#### Scenario: Existing accounts

- **WHEN** the explicitly authorized migration runs once
- **THEN** each existing user SHALL own exactly the two empty default lists
- **AND** previous lists and their entries SHALL be removed
- **AND** ratings, reviews, accounts and catalog records SHALL remain unchanged

#### Scenario: Subsequent customization

- **WHEN** a user creates a custom list after the reset
- **THEN** the system SHALL persist the list and SHALL NOT delete it on login or navigation

#### Scenario: Missing backup or repeated execution

- **WHEN** the backup is incomplete or the migration has already started
- **THEN** the migration SHALL refuse automatic destructive execution and preserve recovery evidence

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
