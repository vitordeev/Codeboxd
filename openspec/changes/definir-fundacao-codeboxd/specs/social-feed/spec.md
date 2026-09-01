## Purpose

Definir o feed social do Codeboxd, permitindo que usuários visualizem e publiquem atividades relacionadas às mídias e interajam com o conteúdo publicado por outros usuários.

## ADDED Requirements

### Requirement: Create media-related posts

The system SHALL allow authenticated users to create posts associated with media items.

A post MAY include written content and media interaction information.

#### Scenario: Creating a media-related post

- **WHEN** an authenticated user submits valid content associated with a media item
- **THEN** the system SHALL create a new post associated with the user and the media item

### Requirement: Display followed user activity

The system SHALL display posts and supported activities created by users followed by the authenticated user.

#### Scenario: Viewing followed user activity

- **WHEN** an authenticated user accesses the social feed
- **THEN** the system SHALL display available posts and activities from followed users

### Requirement: Display post information

The system SHALL display the author, associated media and available publication information for each post.

#### Scenario: Viewing a post

- **WHEN** a user accesses a post
- **THEN** the system SHALL display the post author and the associated media information

### Requirement: Like posts

The system SHALL allow authenticated users to like posts created by other users.

A user SHALL have no more than one active like for the same post.

#### Scenario: Liking a post

- **WHEN** an authenticated user likes a post they have not previously liked
- **THEN** the system SHALL register the user's like for that post

#### Scenario: Liking an already liked post

- **WHEN** an authenticated user attempts to like a post they have already liked
- **THEN** the system SHALL prevent the creation of a duplicate like

### Requirement: Remove post likes

The system SHALL allow authenticated users to remove their own likes from posts.

#### Scenario: Removing a like

- **WHEN** an authenticated user removes their existing like from a post
- **THEN** the system SHALL remove the user's like from that post

### Requirement: Comment on posts

The system SHALL allow authenticated users to create comments on posts.

#### Scenario: Creating a comment

- **WHEN** an authenticated user submits valid comment content on a post
- **THEN** the system SHALL associate the comment with the user and the selected post

### Requirement: Manage own social content

The system SHALL allow users to modify or remove content created by themselves.

The system SHALL prevent users from modifying or removing content created by other users.

#### Scenario: Editing own post

- **WHEN** an authenticated user edits a post created by themselves
- **THEN** the system SHALL update the post with the submitted content

#### Scenario: Editing another user's post

- **WHEN** an authenticated user attempts to modify a post created by another user
- **THEN** the system SHALL deny the modification