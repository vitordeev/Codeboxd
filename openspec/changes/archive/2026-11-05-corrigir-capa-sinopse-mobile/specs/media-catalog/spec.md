## ADDED Requirements

### Requirement: Readable mobile media details

The system SHALL display the cover, title and full description of a media item
without overlapping the cover and text on mobile screens from 320px to 640px.
The detail card SHALL fit the viewport without horizontal scrolling.

#### Scenario: Book with a long description on mobile

- **WHEN** a user views a book with a cover and long title and description on a mobile screen
- **THEN** the cover SHALL occupy a separate area from the title and description
- **AND** the complete description SHALL remain readable without horizontal scrolling

#### Scenario: Other supported media and missing covers

- **WHEN** a user views a movie, series or anime, or an item without a cover, on mobile
- **THEN** its cover or placeholder SHALL remain separate from the title and description
