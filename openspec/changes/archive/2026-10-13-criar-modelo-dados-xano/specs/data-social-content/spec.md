## Purpose

Definir a persistência do conteúdo social do Codeboxd, incluindo posts, curtidas e comentários associados aos seus respectivos usuários e mídias.

## ADDED Requirements

### Requirement: Post persistence

The system SHALL persist social posts created by users.

#### Scenario: Creating a post

- **WHEN** a user creates a valid post
- **THEN** the system SHALL persist the post with its author

### Requirement: Media association with posts

The system SHALL persist the association between a post and its referenced media when applicable.

#### Scenario: Creating a media-related post

- **WHEN** a user creates a post associated with a media item
- **THEN** the system SHALL persist the association between the post and the media

### Requirement: Like persistence

The system SHALL persist likes associated with users and posts.

#### Scenario: Liking a post

- **WHEN** a user likes a post
- **THEN** the system SHALL persist the relationship between the user and the post

### Requirement: Unique post likes

The system SHALL prevent a user from having multiple active likes for the same post.

#### Scenario: Duplicate post like

- **WHEN** a user attempts to create another active like for the same post
- **THEN** the system SHALL prevent the duplicate like

### Requirement: Comment persistence

The system SHALL persist comments associated with users and posts.

#### Scenario: Creating a comment

- **WHEN** a user submits a valid comment on a post
- **THEN** the system SHALL persist the comment with its author and post