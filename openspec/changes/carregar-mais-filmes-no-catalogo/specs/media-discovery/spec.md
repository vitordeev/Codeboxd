## MODIFIED Requirements

### Requirement: Browse beyond the initial catalog

The system SHALL display discovery collections grouped by media type in vertically stacked sections with independently scrollable horizontal shelves. Text search and category catalogs SHALL remain independently paginated. Every home shelf SHALL load and append the next page from its own collection when the user approaches the horizontal end. Home shelves SHALL NOT show horizontal scrollbars, navigation arrows, or separate manual load buttons. Loading SHALL preserve the collection's category and order, avoid duplicate identities, and stop when the provider has no more unique items. Search and category result pages SHALL retain their existing pagination controls.

#### Scenario: More titles
- **WHEN** a user reaches the end of a home shelf with another page of results available
- **THEN** the system SHALL append additional results to that shelf without duplicating identities or replacing another section

#### Scenario: More titles load at the end of any home shelf
- **WHEN** a user scrolls a home shelf of movies, series, books, or anime close to its horizontal end and another page is available
- **THEN** the system SHALL load and append results from that shelf's own collection without requiring an arrow or separate button
- **AND** it SHALL preserve the horizontal scrolling position, existing cards, and collection category

#### Scenario: Home shelf reaches the end of available results
- **WHEN** the provider has no further unique results for a home shelf
- **THEN** the system SHALL stop requesting pages and SHALL NOT repeatedly trigger requests while the user remains at the end

#### Scenario: Home shelves have no visible navigation controls
- **WHEN** a user views any home shelf
- **THEN** its horizontal scrolling SHALL remain available through touch, trackpad, or keyboard without a visible scrollbar, arrow controls, or manual load button
