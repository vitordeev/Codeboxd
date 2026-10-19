## Purpose

Definir a persistência de listas personalizadas criadas pelos usuários e dos itens de mídia associados a cada lista.

## ADDED Requirements

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