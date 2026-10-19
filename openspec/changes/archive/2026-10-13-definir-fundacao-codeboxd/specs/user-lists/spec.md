## Purpose

Definir como os usuários criam e gerenciam listas personalizadas contendo filmes, séries, animes e livros dentro do Codeboxd.

## ADDED Requirements

### Requirement: Create custom lists

The system SHALL allow authenticated users to create personalized media lists.

A list SHALL have a title.

A list MAY include a description.

#### Scenario: Creating a list

- **WHEN** an authenticated user provides a valid title for a new list
- **THEN** the system SHALL create the list and associate it with the user

### Requirement: Add media to lists

The system SHALL allow users to add supported media items to their own lists.

A list MAY contain different supported media types.

#### Scenario: Adding media to a list

- **WHEN** an authenticated user selects a media item and one of their lists
- **THEN** the system SHALL add the media item to the selected list

### Requirement: Prevent duplicate list entries

The system SHALL prevent the same media item from being added multiple times to the same list.

#### Scenario: Adding duplicate media

- **WHEN** a user attempts to add a media item already present in a list
- **THEN** the system SHALL prevent the creation of a duplicate entry

### Requirement: Remove media from lists

The system SHALL allow users to remove media items from their own lists.

#### Scenario: Removing media from a list

- **WHEN** an authenticated user removes a media item from one of their lists
- **THEN** the system SHALL remove the media item from that list

### Requirement: Edit lists

The system SHALL allow users to update the information of lists created by themselves.

#### Scenario: Updating a list

- **WHEN** an authenticated user updates the title or description of one of their lists
- **THEN** the system SHALL update the list information

### Requirement: Delete lists

The system SHALL allow users to delete lists created by themselves.

#### Scenario: Deleting a list

- **WHEN** an authenticated user requests deletion of one of their lists
- **THEN** the system SHALL remove the list and its associated list entries

### Requirement: Protect list ownership

The system SHALL prevent users from modifying or deleting lists created by other users.

#### Scenario: Modifying another user's list

- **WHEN** an authenticated user attempts to modify a list created by another user
- **THEN** the system SHALL deny the modification