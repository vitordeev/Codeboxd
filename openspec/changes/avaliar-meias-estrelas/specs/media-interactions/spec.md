## MODIFIED Requirements

### Requirement: Media rating

The system SHALL allow authenticated users to assign a rating to a media item.
Anonymous visitors MAY assign a personal rating stored only in that browser;
it SHALL NOT be published, associated with a profile, or sent to the social API.
Each user SHALL have no more than one active rating for the same media item.
Ratings SHALL support half-star steps from 0.5 to 5, with zero representing no
rating. The interface SHALL show half-filled stars for fractional ratings and
Portuguese decimal labels, such as 1,5. Submitted decimals using comma or dot
SHALL be normalized without truncation. Unsupported fractions SHALL be rejected.

#### Scenario: Rating a media item
- **WHEN** an authenticated user submits a valid rating for a media item
- **THEN** the system SHALL associate the rating with that user's interaction

#### Scenario: Visitor rates a media item
- **WHEN** an anonymous visitor rates a media item
- **THEN** the system SHALL save and restore that rating only in browser storage
- **AND** the rating SHALL NOT appear as a public or account rating

#### Scenario: Updating a rating
- **WHEN** an authenticated user changes their rating for a media item
- **THEN** the system SHALL replace the previous rating with the updated rating

#### Scenario: Half star selection
- **WHEN** a user selects 1,5 stars using a star half or the rating control
- **THEN** the interface SHALL show one complete star and one half star
- **AND** restoring or saving the rating SHALL preserve the numeric value 1.5

#### Scenario: Clear rating and preserve draft
- **WHEN** a user changes or clears a rating while editing a review
- **THEN** the review draft SHALL be preserved and zero SHALL show empty stars

#### Scenario: Invalid fraction
- **WHEN** a rating outside zero to five or not in half-star steps is submitted
- **THEN** the system SHALL reject it without persisting an interaction
