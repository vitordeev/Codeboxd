## Purpose

Definir um catálogo unificado que permita ao Codeboxd representar filmes, séries, animes e livros de forma consistente para os usuários da plataforma.

## ADDED Requirements

### Requirement: Support media types

The system SHALL support the following media types:

- Movies
- Series
- Anime
- Books

Each media item SHALL belong to one supported media type.

#### Scenario: Viewing a movie

- **WHEN** a user accesses a media item classified as a movie
- **THEN** the system SHALL identify the item as a movie

#### Scenario: Viewing an anime

- **WHEN** a user accesses a media item classified as an anime
- **THEN** the system SHALL identify the item as an anime

### Requirement: Identify media items

The system SHALL maintain an identifiable representation for each media item used within the platform.

Each media item SHALL include, when available:

- Title
- Media type
- Description
- Cover or poster image
- External source
- External identifier

#### Scenario: Viewing media information

- **WHEN** a user opens a media item
- **THEN** the system SHALL display the available identifying information for that media item

### Requirement: Display media-specific information

The system SHALL display information appropriate to the type of media being viewed.

#### Scenario: Viewing movie details

- **WHEN** a user views a movie
- **THEN** the system SHALL display available movie-specific information

#### Scenario: Viewing series details

- **WHEN** a user views a series
- **THEN** the system SHALL display available series-specific information

#### Scenario: Viewing anime details

- **WHEN** a user views an anime
- **THEN** the system SHALL display available anime-specific information

#### Scenario: Viewing book details

- **WHEN** a user views a book
- **THEN** the system SHALL display available book-specific information

### Requirement: Preserve external media identity

The system SHALL associate media obtained from an external data provider with its source and external identifier.

#### Scenario: Using externally sourced media

- **WHEN** a media item is obtained from an external data provider
- **THEN** the system SHALL retain the source and external identifier associated with that media item