# user-lists Specification

## Purpose

Definir como os usuários criam e gerenciam listas personalizadas contendo filmes, séries, animes e livros dentro do Codeboxd.

## Requirements

### Requirement: Create custom lists

The system SHALL allow authenticated users to create personalized media lists.

A list SHALL have a title.

A list MAY include a description.

#### Scenario: Creating a list

- **WHEN** an authenticated user provides a valid title for a new list
- **THEN** the system SHALL create the list and associate it with the user

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

### Requirement: Prevent duplicate list entries

The system SHALL prevent the same media item from being added multiple times to the same list.

#### Scenario: Adding duplicate media

- **WHEN** a user attempts to add a media item already present in a list
- **THEN** the system SHALL prevent the creation of a duplicate entry

### Requirement: Remove media from lists

The system SHALL allow users to remove media items from their own lists.

#### Scenario: Removing media from a list

- **WHEN** an authenticated user removes a media item from one of their lists
- **THEN** the system SHALL remove the media item from that list

### Requirement: Edit lists

The system SHALL allow users to update the information of lists created by themselves.

#### Scenario: Updating a list

- **WHEN** an authenticated user updates the title or description of one of their lists
- **THEN** the system SHALL update the list information

### Requirement: Delete lists

The system SHALL allow users to delete lists created by themselves.

#### Scenario: Deleting a list

- **WHEN** an authenticated user requests deletion of one of their lists
- **THEN** the system SHALL remove the list and its associated list entries

### Requirement: Protect list ownership

The system SHALL prevent users from modifying or deleting lists created by other users.

#### Scenario: Modifying another user's list

- **WHEN** an authenticated user attempts to modify a list created by another user
- **THEN** the system SHALL deny the modification

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
