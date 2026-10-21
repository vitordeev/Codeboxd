## Purpose

Padronizar listas iniciais e executar reset único autorizado sem restringir listas futuras.

## ADDED Requirements

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
