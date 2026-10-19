## Purpose

Definir como o Codeboxd obtém e utiliza informações de fontes externas para disponibilizar dados sobre filmes, séries, animes e livros dentro da plataforma.

## ADDED Requirements

### Requirement: Retrieve external media data

The system SHALL retrieve media information from supported external data sources when external information is required.

#### Scenario: Retrieving available media data

- **WHEN** the system requests information for a media item available from a supported external source
- **THEN** the system SHALL retrieve the available information from that source

### Requirement: Associate media with its source

The system SHALL preserve the source and external identifier associated with externally obtained media information.

#### Scenario: Storing external media identity

- **WHEN** externally sourced media is used within the platform
- **THEN** the system SHALL retain the associated source and external identifier

### Requirement: Support media source categories

The system SHALL support external data sources appropriate for the supported media categories.

The supported categories SHALL include:

- Movies
- Series
- Anime
- Books

#### Scenario: Retrieving movie information

- **WHEN** information about a movie is requested
- **THEN** the system SHALL use an available supported source for movie information

#### Scenario: Retrieving series information

- **WHEN** information about a series is requested
- **THEN** the system SHALL use an available supported source for series information

#### Scenario: Retrieving anime information

- **WHEN** information about an anime is requested
- **THEN** the system SHALL use an available supported source for anime information

#### Scenario: Retrieving book information

- **WHEN** information about a book is requested
- **THEN** the system SHALL use an available supported source for book information

### Requirement: Handle unavailable external sources

The system SHALL handle temporary failures from external data sources without corrupting existing Codeboxd data.

#### Scenario: External source temporarily unavailable

- **WHEN** a required external data source is temporarily unavailable
- **THEN** the system SHALL inform the user that the requested external information could not be retrieved

### Requirement: Preserve existing user data during external failures

The system SHALL preserve existing user interactions and social data when an external media source is unavailable.

#### Scenario: Viewing existing interaction during external failure

- **WHEN** an external media source is unavailable and a user accesses an existing Codeboxd interaction
- **THEN** the system SHALL continue to provide the available internally stored interaction data