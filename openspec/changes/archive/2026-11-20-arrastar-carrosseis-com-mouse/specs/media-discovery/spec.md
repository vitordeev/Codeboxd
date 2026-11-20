# Spec Delta

## ADDED Requirements

### Requirement: Drag horizontal discovery shelves with a mouse
The system SHALL allow users to scroll a horizontal discovery shelf by dragging it with the primary mouse button.

#### Scenario: Drag a shelf horizontally
- **WHEN** a user presses and moves the primary mouse button horizontally beyond the drag threshold over a discovery shelf
- **THEN** the visible shelf content SHALL follow the pointer's horizontal movement

#### Scenario: Click a media card without dragging
- **WHEN** a user clicks a media card without moving the pointer beyond the drag threshold
- **THEN** the system SHALL open that media item's details

#### Scenario: Suppress the click from a completed drag
- **WHEN** a user completes a drag over a media card
- **THEN** the system SHALL NOT open that card as a result of the same pointer gesture
- **AND** subsequent pointer clicks and keyboard activation SHALL continue to open media details

### Requirement: Preserve other discovery shelf interactions
Mouse dragging SHALL NOT interfere with vertical page scrolling, native touch or trackpad scrolling, keyboard navigation, or scroll-triggered loading of additional results.

#### Scenario: Vertical movement over a shelf
- **WHEN** a user's pointer movement over a shelf is predominantly vertical
- **THEN** the page SHALL retain its normal vertical scrolling behavior

#### Scenario: Vertical movement does not activate a card
- **WHEN** a user's pointer moves predominantly vertically beyond the drag threshold over a media card
- **THEN** the system SHALL NOT open that card as a result of the same pointer gesture
- **AND** subsequent clicks and keyboard activation SHALL continue to open media details

#### Scenario: Use touch, trackpad, or keyboard
- **WHEN** a user scrolls a shelf using touch, a trackpad, or supported keyboard navigation
- **THEN** the shelf SHALL retain its existing navigation behavior

#### Scenario: Scroll to load more results
- **WHEN** the user drags or otherwise scrolls a shelf to its load-more threshold
- **THEN** the existing mechanism SHALL append additional results without replacing or duplicating current items
