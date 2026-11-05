# social-feed Specification

## Purpose

Definir o feed social do Codeboxd, permitindo que usuários visualizem e publiquem atividades relacionadas às mídias e interajam com o conteúdo publicado por outros usuários.

## Requirements

### Requirement: Create media-related posts
The system SHALL allow authenticated users to create posts with an optional
association to a supported media item. A post MAY include written content and
media interaction information. When a user selects a personal photo, the system
SHALL include that photo with the post or prevent submission until the photo
upload succeeds; it SHALL NOT silently publish the text and media association
without the selected photo.

#### Scenario: Creating a media-related post
- **WHEN** an authenticated user submits valid content associated with a media item
- **THEN** the system SHALL create a new post associated with the user and the media item

#### Scenario: Creating a post without media
- **WHEN** an authenticated user submits valid content without selecting media
- **THEN** the system SHALL create a post without requiring a media reference

#### Scenario: Publishing a selected personal photo
- **WHEN** an authenticated user selects a valid personal photo and submits the post
- **THEN** the system SHALL attach the photo to the same post without requiring a separate manual upload action

#### Scenario: Publishing while the selected photo is not ready
- **WHEN** a selected photo is still uploading or its upload has failed
- **THEN** the system SHALL prevent the post from being published without that photo and SHALL show the upload state or error

### Requirement: Display followed user activity

The system SHALL display posts and supported activities created by users followed by the authenticated user.

#### Scenario: Viewing followed user activity

- **WHEN** an authenticated user accesses the social feed
- **THEN** the system SHALL display available posts and activities from followed users

### Requirement: Display post information

The system SHALL display the author, associated media and available publication information for each post. When a post has an associated work, its compact linked card SHALL appear in the post header alongside the author's identity. A personal photo SHALL remain the main image below the header. The work SHALL keep a readable fallback when no cover is available.

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

#### Scenario: Personal photo with an associated work
- **WHEN** a post has both an attached photo and an associated work
- **THEN** the system SHALL display the photo prominently and the work as a compact clickable thumbnail

#### Scenario: Work without a photo or cover
- **WHEN** a post references a work with no photo or no cover
- **THEN** the work SHALL remain recognizable and clickable without a broken or oversized image

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
The system SHALL prevent users from modifying or removing content created by
other users. Editing SHALL preserve the original post ID, authorship and
publication identity, without creating another post. Media association SHALL
be optional and editable independently of the post identity.

#### Scenario: Editing own post
- **WHEN** an authenticated user edits a post created by themselves
- **THEN** the system SHALL update the post with the submitted content

#### Scenario: Editing another user's post
- **WHEN** an authenticated user attempts to modify a post created by another user
- **THEN** the system SHALL deny the modification

#### Scenario: Editing with or without media
- **WHEN** the author keeps, replaces or removes the media association while editing
- **THEN** the system SHALL update only the original post without duplicating it or losing an unchanged image

#### Scenario: Lost edit context or repeated submission
- **WHEN** edit context changes during submission or a save is submitted twice
- **THEN** the system SHALL never turn the edit into creation and SHALL prevent simultaneous duplicate submissions

#### Scenario: Failed edit
- **WHEN** saving fails without a session rejection
- **THEN** the system SHALL retain the editable draft and provide an error without creating a replacement post

### Requirement: Contextual post interactions
The system SHALL provide accessible like controls with visible confirmed state
and available counts. Comments SHALL open in a dedicated panel for the selected
post with avatar, author, loading, error, empty state and an editable composer.
Existing authorship restrictions SHALL remain enforced.

#### Scenario: Opening and closing comments
- **WHEN** a user opens comments on a post
- **THEN** its discussion panel SHALL appear without scrolling to the end of the feed and SHALL allow accessible dismissal

#### Scenario: Repeated interaction while pending
- **WHEN** the same like or comment is submitted repeatedly while pending
- **THEN** only one mutation SHALL be sent and the interface SHALL show its pending state

#### Scenario: Failed comment submission
- **WHEN** a comment fails to save
- **THEN** the composer SHALL retain the draft and display an error without claiming success

#### Scenario: Discussion or account changes during a request
- **WHEN** an old discussion response arrives after another post is selected, closed or the account changes
- **THEN** the response SHALL NOT replace the active discussion or send a comment to another post

#### Scenario: Legacy likes endpoint
- **WHEN** the workspace has no /likes route
- **THEN** post interactions SHALL remain compatible through discussion without introducing per-post reads during feed loading

### Requirement: Feed independent of own publishing
O feed SHALL consultar posts dos seguidos independentemente de publicação ou
registro prévio de timeline do leitor. Falha SHALL ser distinguida de vazio.

#### Scenario: New reader follows an author
- **WHEN** uma conta sem posts segue um perfil que tem posts e abre o feed
- **THEN** os posts existentes do perfil SHALL aparecer imediatamente

#### Scenario: Feed request failure
- **WHEN** a consulta do feed falha
- **THEN** a interface SHALL apresentar erro e opção de tentar novamente em vez de afirmar ausência de conteúdo

#### Scenario: Ancillary read failure
- **WHEN** posts dos seguidos foram recebidos e a consulta opcional de posts próprios ou likes falha transitoriamente
- **THEN** os posts recebidos SHALL permanecer disponíveis com aviso da falha parcial
