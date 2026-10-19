## Purpose

Definir como os usuários estabelecem conexões sociais no Codeboxd por meio das funcionalidades de seguir e deixar de seguir outros usuários.

## ADDED Requirements

### Requirement: Follow users

The system SHALL allow authenticated users to follow other registered users.

#### Scenario: Successfully following a user

- **WHEN** an authenticated user chooses to follow another registered user
- **THEN** the system SHALL create a connection between the follower and the followed user

### Requirement: Prevent duplicate follows

The system SHALL prevent a user from following the same user more than once.

#### Scenario: Attempting to follow an already followed user

- **WHEN** a user attempts to follow another user they already follow
- **THEN** the system SHALL prevent the creation of a duplicate connection

### Requirement: Unfollow users

The system SHALL allow authenticated users to stop following users they currently follow.

#### Scenario: Successfully unfollowing a user

- **WHEN** an authenticated user chooses to unfollow a user they currently follow
- **THEN** the system SHALL remove the connection between the two users

### Requirement: View followers

The system SHALL allow users to view the users who follow a public profile.

#### Scenario: Viewing followers

- **WHEN** a user accesses the followers section of a profile
- **THEN** the system SHALL display the available users following that profile

### Requirement: View followed users

The system SHALL allow users to view the users followed by a public profile.

#### Scenario: Viewing followed users

- **WHEN** a user accesses the following section of a profile
- **THEN** the system SHALL display the available users followed by that profile

### Requirement: Prevent self-following

The system SHALL prevent a user from following their own profile.

#### Scenario: Attempting to follow own profile

- **WHEN** an authenticated user attempts to follow their own profile
- **THEN** the system SHALL deny the connection