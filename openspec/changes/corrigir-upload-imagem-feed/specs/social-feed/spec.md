## MODIFIED Requirements

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
