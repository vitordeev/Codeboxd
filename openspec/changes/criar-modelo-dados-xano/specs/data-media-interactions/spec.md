## Purpose

Definir a persistência das interações individuais dos usuários com filmes, séries, animes e livros, mantendo os registros pessoais separados entre os usuários.

## ADDED Requirements

### Requirement: User-media relationship persistence

The system SHALL persist the relationship between a user and a media item when the user creates an interaction.

#### Scenario: Creating a media interaction

- **WHEN** a user creates an interaction with a media item
- **THEN** the system SHALL associate the interaction with both the user and the media item

### Requirement: Consumption status persistence

The system SHALL persist the consumption status associated with a user's media interaction.

#### Scenario: Updating consumption status

- **WHEN** a user updates the status of a media interaction
- **THEN** the system SHALL persist the updated status

### Requirement: Rating persistence

The system SHALL persist a user's rating for a media item.

#### Scenario: Saving a rating

- **WHEN** a user provides a valid rating for a media item
- **THEN** the system SHALL associate the rating with that user's interaction

### Requirement: Review persistence

The system SHALL persist written reviews associated with users and media items.

#### Scenario: Saving a review

- **WHEN** a user submits a review for a media item
- **THEN** the system SHALL persist the review with its associated user and media item

### Requirement: Independent user interactions

The system SHALL maintain media interactions independently for each user.

#### Scenario: Multiple users interact with the same media

- **WHEN** multiple users create interactions for the same media item
- **THEN** the system SHALL preserve each user's interaction independently