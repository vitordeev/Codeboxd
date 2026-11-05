## MODIFIED Requirements

### Requirement: Display post information
The system SHALL display the author, associated media and available publication
information for each post. An attached personal photo SHALL be the main image.
Associated media SHALL use a compact thumbnail and title link, independently
of the photo, with a readable fallback when no cover is available.

#### Scenario: Viewing a post
- **WHEN** a user accesses a post
- **THEN** the system SHALL display the post author and associated media information

#### Scenario: Personal photo with an associated work
- **WHEN** a post has both an attached photo and an associated work
- **THEN** the system SHALL display the photo prominently and the work as a compact clickable thumbnail

#### Scenario: Work without a photo or cover
- **WHEN** a post references a work with no photo or no cover
- **THEN** the work SHALL remain recognizable and clickable without a broken or oversized image

## ADDED Requirements

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
