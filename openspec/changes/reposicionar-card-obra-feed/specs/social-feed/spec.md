## MODIFIED Requirements

### Requirement: Display post information

The system SHALL display the author, associated media and available publication information for each post. When a post has an associated work, its compact linked card SHALL appear in the post header alongside the author's identity. A personal photo SHALL remain the main image below the header.

#### Scenario: Viewing a post

- **WHEN** a user accesses a post
- **THEN** the system SHALL display the post author and the associated media information

#### Scenario: Post with associated work

- **WHEN** a post has an associated work
- **THEN** the system SHALL show the compact linked work card beside the author's identity in the header

#### Scenario: Post with personal photo and associated work

- **WHEN** a post has both a personal photo and an associated work
- **THEN** the system SHALL show the work card in the header and the personal photo as the main content image below it

#### Scenario: Narrow screen

- **WHEN** the post is shown in a narrow viewport
- **THEN** the author identity and work card SHALL wrap or shrink without horizontal overflow, while keeping the work link accessible
