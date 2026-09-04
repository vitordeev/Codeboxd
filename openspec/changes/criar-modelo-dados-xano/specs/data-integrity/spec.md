## Purpose

Definir regras de integridade para os dados persistidos no Codeboxd, prevenindo duplicações e relações inválidas entre usuários, mídias e conteúdos.

## ADDED Requirements

### Requirement: Persistent relationship validity

The system SHALL only persist relationships that reference valid associated records.

#### Scenario: Creating a relationship with valid records

- **WHEN** all records referenced by a new relationship exist
- **THEN** the system SHALL allow the relationship to be persisted

#### Scenario: Creating a relationship with an invalid record

- **WHEN** a relationship references a record that does not exist
- **THEN** the system SHALL reject the relationship

### Requirement: External media duplication prevention

The system SHALL prevent duplicate persisted media identities for the same external source and external identifier.

#### Scenario: Duplicate external media

- **WHEN** media with an existing external source and external identifier is processed
- **THEN** the system SHALL preserve a single internal media representation

### Requirement: User data ownership integrity

The system SHALL preserve ownership relationships for user-created data.

#### Scenario: Accessing user-created data

- **WHEN** user-created data is retrieved
- **THEN** the system SHALL retain the identity of the user associated with that data

### Requirement: Referential consistency

The system SHALL maintain consistency between persisted records and their associated relationships.

#### Scenario: Retrieving associated data

- **WHEN** a persisted relationship is retrieved
- **THEN** the system SHALL provide the associated records consistently