## ADDED Requirements

### Requirement: Separate personal and public list discovery
The system SHALL display only the authenticated owner's lists in the personal list collection. Other users' public lists SHALL be shown in a separately identified discovery context with ownership distinguishable. Visitors SHALL receive only public discovery content.

#### Scenario: Identical standard titles across owners
- **WHEN** an authenticated user opens their personal lists and other profiles have public lists with identical titles
- **THEN** the personal collection SHALL contain only the authenticated user's lists
- **AND** public discovery SHALL remain separate and SHALL distinguish ownership

#### Scenario: Account switch
- **WHEN** the session changes to another account during list loading
- **THEN** previous account results SHALL NOT populate the new account's personal collection

#### Scenario: Visitor
- **WHEN** a visitor opens list discovery
- **THEN** only public lists SHALL be accessible and no personal collection SHALL be attributed to that visitor

### Requirement: Public lists grouped by owner
The system SHALL group public lists by owner, displaying each owner's avatar and name as a profile link above their lists. Missing profile data SHALL use a neutral fallback without misattributing ownership or hiding public lists.

#### Scenario: Multiple owners with identical list titles
- **WHEN** public lists from multiple owners are displayed
- **THEN** each owner's lists SHALL appear beneath that owner's linked name and avatar

#### Scenario: Missing profile or failed lookup
- **WHEN** an owner's public profile is unavailable
- **THEN** the group SHALL retain its lists and correct profile destination with a neutral name and avatar

#### Scenario: Owner name beside avatar
- **WHEN** the public owner header is displayed at desktop or mobile width, including a long name
- **THEN** the name SHALL remain in the column to the right of the avatar, wrapping within that column when necessary
