## Purpose

Definir a persistência das relações sociais entre usuários do Codeboxd, permitindo representar seguidores e usuários seguidos.

## ADDED Requirements

### Requirement: Follow relationship persistence

The system SHALL persist a relationship when one user follows another user.

#### Scenario: Creating a follow relationship

- **WHEN** a user follows another user
- **THEN** the system SHALL persist the follower and followed user relationship

### Requirement: Unique follow relationships

The system SHALL prevent duplicate follow relationships between the same follower and followed user.

#### Scenario: Duplicate follow relationship

- **WHEN** a follow relationship already exists between two users
- **THEN** the system SHALL prevent another identical relationship from being persisted

### Requirement: Follow relationship removal

The system SHALL remove a persisted follow relationship when a user unfollows another user.

#### Scenario: Removing a follow relationship

- **WHEN** a user unfollows another user
- **THEN** the system SHALL remove the corresponding persisted relationship

### Requirement: Follow direction preservation

The system SHALL preserve the direction of each follow relationship.

#### Scenario: User A follows User B

- **WHEN** User A follows User B
- **THEN** the system SHALL distinguish User A as the follower and User B as the followed user