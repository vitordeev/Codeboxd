## MODIFIED Requirements

### Requirement: Create media-related posts
The system SHALL allow authenticated users to create posts with an optional
association to a supported media item. A post MAY include written content and
media interaction information.

#### Scenario: Creating a media-related post
- **WHEN** an authenticated user submits valid content associated with a media item
- **THEN** the system SHALL create a new post associated with the user and the media item

#### Scenario: Creating a post without media
- **WHEN** an authenticated user submits valid content without selecting media
- **THEN** the system SHALL create a post without requiring a media reference

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
