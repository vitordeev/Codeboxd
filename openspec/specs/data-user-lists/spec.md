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
