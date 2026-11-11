## MODIFIED Requirements

### Requirement: Public lists grouped by owner
The public list directory SHALL group lists by owner, displaying each owner's avatar and name as a profile link above their lists. Missing profile data SHALL use a neutral fallback without misattributing ownership or hiding public lists. Public search results SHALL be allowed to rank individual lists by relevance, provided every result visibly identifies its owner and links to that profile.

#### Scenario: Multiple owners with identical list titles
- **WHEN** public lists from multiple owners are displayed in the public directory
- **THEN** each owner's lists SHALL appear beneath that owner's linked name and avatar

#### Scenario: Missing profile or failed lookup
- **WHEN** an owner's public profile is unavailable
- **THEN** the group SHALL retain its lists and correct profile destination with a neutral name and avatar

#### Scenario: Owner name beside avatar
- **WHEN** the public owner header is displayed at desktop or mobile width, including a long name
- **THEN** the name SHALL remain in the column to the right of the avatar, wrapping within that column when necessary

#### Scenario: Ranked list search results
- **WHEN** the user searches public lists and results are ranked individually
- **THEN** every result SHALL display its correct creator and profile link without requiring grouping that would obscure relevance

## ADDED Requirements

### Requirement: Addressable list details
The system SHALL provide an addressable details view for an accessible list, with title, description, creator/profile link and paginated contents. Opening a list SHALL NOT depend on finding it in the currently loaded directory page.

#### Scenario: Open a public list directly
- **WHEN** a visitor opens a valid public list URL not present in the current directory page
- **THEN** the system SHALL show its public details and contents with the correct creator and links to its works

#### Scenario: Open an owned private list
- **WHEN** an authenticated owner opens the URL of their private list
- **THEN** the system SHALL provide its details within the authenticated personal context and keep it excluded from public discovery

#### Scenario: Large list or empty list
- **WHEN** the list has more than one page of items or no items
- **THEN** the details SHALL provide access to all permitted pages or an explicit empty state without treating the first page as the entire collection

### Requirement: Public detail privacy
Public detail requests for private or nonexistent lists SHALL be indistinguishable and SHALL NOT disclose list metadata, creator, contents or counts. Privacy changes SHALL invalidate previously public application state and caches; protected owner access SHALL remain separate.

#### Scenario: Private URL from another account
- **WHEN** a visitor or non-owner requests a private list through a public detail URL or endpoint
- **THEN** the response SHALL expose no list data and be indistinguishable from a nonexistent list

#### Scenario: Public list becomes private
- **WHEN** a list is made private after a link was shared
- **THEN** subsequent public detail and item requests SHALL reject access and not recover the prior content from application caches

### Requirement: Public link sharing
The details of a public list SHALL provide its stable URL for copying or sharing without making a private list public. Failure of optional clipboard or native sharing mechanisms SHALL leave an accessible way to obtain the link.

#### Scenario: Copy a public list link
- **WHEN** the user requests the share action of a public list
- **THEN** the application SHALL offer its stable public URL and confirm copying only after success, otherwise showing a selectable link

#### Scenario: Private list share controls
- **WHEN** the owner views a private list
- **THEN** the application SHALL NOT present it as publicly shareable or change visibility as a side effect of obtaining its address

### Requirement: Existing list management preserved
Owners SHALL retain create/edit/delete and add/remove-work actions with server authorization, default-list identity and privacy preserved. Moving discovery to Search SHALL NOT remove personal list management or require publishing list activity in the feed.

#### Scenario: Manage a list from personal navigation
- **WHEN** an authenticated owner opens their lists and selects a custom list
- **THEN** they SHALL retain editing and content management without depending on a feed entry

#### Scenario: Another user's result
- **WHEN** a user opens someone else's public list from Search
- **THEN** they SHALL have read access but no ability to mutate it by UI controls or direct API calls
