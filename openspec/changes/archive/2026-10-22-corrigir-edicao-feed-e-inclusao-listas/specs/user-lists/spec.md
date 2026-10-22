## MODIFIED Requirements

### Requirement: Add media to lists
The system SHALL allow users to add supported media items to their own lists.
A list MAY contain different supported media types. The system SHALL offer
catalog search inside a list and list selection from the media details page.
Only lists owned by the authenticated user SHALL be eligible destinations.

#### Scenario: Adding media to a list
- **WHEN** an authenticated user selects a media item and one of their lists
- **THEN** the system SHALL add the media item to the selected list

#### Scenario: Search from a list
- **WHEN** the list owner searches by title
- **THEN** the system SHALL show matching supported movies, series, anime and books and allow explicit addition of a result

#### Scenario: Add from media details
- **WHEN** an authenticated user opens a media details page and chooses to add it to a list
- **THEN** the system SHALL offer their own public and private lists and add the current work to the selected destination after confirmation

#### Scenario: External media identity
- **WHEN** a selected catalog work has no local record
- **THEN** the system SHALL resolve its local identity without duplicating the work before adding it to the chosen list

#### Scenario: Failure or obsolete results
- **WHEN** search or addition fails, or the account, query, list or work changes during loading
- **THEN** the system SHALL preserve usable content, report applicable errors and prevent obsolete results or writes from affecting the new context
