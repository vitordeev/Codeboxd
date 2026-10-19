## Purpose

Definir como os usuários descobrem, pesquisam e filtram filmes, séries, animes e livros disponíveis para visualização e interação dentro do Codeboxd.

## ADDED Requirements

### Requirement: Search for media

The system SHALL allow users to search for media using a textual search term.

The search SHALL support results from all media types available in the platform.

#### Scenario: Successful media search

- **WHEN** a user enters a valid search term
- **THEN** the system SHALL display media results that correspond to the search term

#### Scenario: No search results found

- **WHEN** a user searches for a term with no matching media
- **THEN** the system SHALL inform the user that no results were found

### Requirement: Display mixed media results

The system SHALL allow search results to contain movies, series, anime and books.

Each displayed result SHALL identify its media type.

#### Scenario: Search returns different media types

- **WHEN** a search matches media from multiple supported types
- **THEN** the system SHALL display the matching media and identify the type of each result

### Requirement: Filter media discovery results

The system SHALL allow users to browse discovery catalogs by media type.

Text searches SHALL always query all supported media types, independently of the previously selected discovery category. Category controls SHALL be separate from the search form.

The supported filters SHALL include:

- Movies
- Series
- Anime
- Books

#### Scenario: Filtering by media type

- **WHEN** a user selects a media type filter
- **THEN** the system SHALL display only results matching the selected media type

#### Scenario: Search after browsing a category

- **WHEN** a user browses Movies and submits a textual search
- **THEN** the system SHALL search movies, series, anime and books
- **AND** loading additional results SHALL preserve the submitted query even if the input has an unsent edit

### Requirement: Access media from discovery results

The system SHALL allow users to access the details of a media item from a search or discovery result.

#### Scenario: Opening a discovered media item

- **WHEN** a user selects a media item from a search or discovery result
- **THEN** the system SHALL display the details of the selected media item

### Requirement: Handle unavailable external search data

The system SHALL handle situations where an external media data source is unavailable.

The system SHALL inform the user when requested results cannot be retrieved due to a temporary external data source failure.

#### Scenario: External source unavailable

- **WHEN** a media search depends on an unavailable external data source
- **THEN** the system SHALL inform the user that the results could not be retrieved
### Requirement: Browse beyond the initial catalog

The system SHALL display popular movies and series in responsive grids that grow vertically, with no horizontal scrolling inside the home catalogs. Users SHALL be able to append additional pages to each section without entering a search term.

#### Scenario: More titles

- **WHEN** a user chooses to see more popular movies or series
- **THEN** the system SHALL append additional results below the existing cards in that home section without duplicating identities or replacing the other section

### Requirement: Stable media covers

Media cards SHALL reserve a consistent poster area while images load and display a fallback when a cover is missing or fails.

#### Scenario: Broken cover

- **WHEN** a provider image fails to load
- **THEN** the card SHALL retain its poster dimensions, title and navigation and display a cover-unavailable placeholder

### Requirement: Relevant title search

The system SHALL match significant search words against media titles, original titles or edition titles, ignoring case, accents and punctuation. Matches only in author, subject or description metadata SHALL NOT qualify. Exact title matches SHALL precede less exact matches.

The system SHALL normalize the common Portuguese misspelling "homen" to "homem" for provider queries while preserving the input shown to the user.

#### Scenario: Misspelled Spider-Man search

- **WHEN** a user searches for "homen aranha"
- **THEN** the system SHALL query all supported media types for "homem aranha"
- **AND** matching Spider-Man works SHALL appear without unrelated books such as "Proverbios 11"

#### Scenario: Matching books remain discoverable

- **WHEN** a book title or edition title matches all significant search words
- **THEN** it SHALL remain eligible alongside matching movies, series and anime

#### Scenario: Blank category browsing

- **WHEN** a user browses a category without a search term
- **THEN** title relevance filtering SHALL NOT remove the provider's popular items
