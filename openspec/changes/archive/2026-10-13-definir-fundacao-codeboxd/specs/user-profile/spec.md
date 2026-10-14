## Purpose

Definir como os usuários possuem e gerenciam perfis públicos no Codeboxd, permitindo a identificação, apresentação de informações pessoais e visualização de suas atividades na plataforma.

## ADDED Requirements

### Requirement: Public user profile

The system SHALL provide each registered user with a public profile.

The public profile SHALL identify the user by their username.

#### Scenario: Viewing a user profile

- **WHEN** a user accesses another user's profile
- **THEN** the system SHALL display the public information associated with that profile

### Requirement: Profile information

The system SHALL allow users to maintain public profile information.

Profile information SHALL support:

- Username
- Display name
- Biography
- Profile image

#### Scenario: Updating profile information

- **WHEN** an authenticated user provides valid profile information
- **THEN** the system SHALL update the user's public profile

#### Scenario: Viewing profile information

- **WHEN** a user accesses a public profile
- **THEN** the system SHALL display the available public profile information

### Requirement: User activity display

The system SHALL allow a user's profile to display activities associated with that user.

Activities MAY include media interactions, reviews, posts and lists.

#### Scenario: Viewing user activity

- **WHEN** a user accesses a profile with recorded activities
- **THEN** the system SHALL display the activities associated with that profile

### Requirement: User profile statistics

The system SHALL display summary statistics related to a user's media activity.

The statistics SHALL only include information available within the Codeboxd platform.

#### Scenario: Viewing profile statistics

- **WHEN** a user accesses a profile
- **THEN** the system SHALL display the available summary statistics for that user

### Requirement: Profile ownership

The system SHALL allow authenticated users to modify their own profile information.

The system SHALL prevent users from modifying the profile information of another user.

#### Scenario: Editing own profile

- **WHEN** an authenticated user edits their own profile
- **THEN** the system SHALL allow the profile information to be updated

#### Scenario: Editing another user's profile

- **WHEN** an authenticated user attempts to modify another user's profile
- **THEN** the system SHALL deny the modification