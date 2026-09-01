## Purpose

Definir como os usuários registram e gerenciam suas interações pessoais com filmes, séries, animes e livros, incluindo status de consumo, avaliações e reviews.

## ADDED Requirements

### Requirement: Media consumption status

The system SHALL allow authenticated users to associate a consumption status with a media item.

The supported consumption statuses SHALL include:

- Planned
- In Progress
- Completed
- Dropped

#### Scenario: Marking media as planned

- **WHEN** an authenticated user selects a media item and marks it as planned
- **THEN** the system SHALL associate the media item with the user's planned status

#### Scenario: Marking media as completed

- **WHEN** an authenticated user marks a media item as completed
- **THEN** the system SHALL associate the media item with the user's completed status

### Requirement: Update media consumption status

The system SHALL allow an authenticated user to update the consumption status associated with their own media interaction.

#### Scenario: Changing media status

- **WHEN** an authenticated user changes the status of a media item in their personal library
- **THEN** the system SHALL update the user's consumption status for that media item

### Requirement: Media rating

The system SHALL allow authenticated users to assign a rating to a media item.

Each user SHALL have no more than one active rating for the same media item.

#### Scenario: Rating a media item

- **WHEN** an authenticated user submits a valid rating for a media item
- **THEN** the system SHALL associate the rating with that user's interaction with the media item

#### Scenario: Updating a rating

- **WHEN** an authenticated user changes their rating for a media item
- **THEN** the system SHALL replace the previous rating with the updated rating

### Requirement: Media review

The system SHALL allow authenticated users to create a written review associated with a media item.

A user SHALL only be allowed to manage reviews created by that same user.

#### Scenario: Creating a review

- **WHEN** an authenticated user submits a valid review for a media item
- **THEN** the system SHALL associate the review with the user and the selected media item

#### Scenario: Editing a review

- **WHEN** an authenticated user edits their own review
- **THEN** the system SHALL update the review with the submitted content

#### Scenario: Editing another user's review

- **WHEN** an authenticated user attempts to edit a review created by another user
- **THEN** the system SHALL deny the modification

### Requirement: Independent media interactions

The system SHALL maintain each user's media interactions independently.

An interaction created by one user SHALL NOT modify the media interactions of another user.

#### Scenario: Multiple users interact with the same media

- **WHEN** multiple users interact with the same media item
- **THEN** the system SHALL maintain each user's status, rating and review independently

### Requirement: View personal media interaction

The system SHALL allow a user to view their recorded interaction with a media item.

#### Scenario: Viewing an existing interaction

- **WHEN** an authenticated user accesses a media item with an existing personal interaction
- **THEN** the system SHALL display the user's recorded status, rating and available review