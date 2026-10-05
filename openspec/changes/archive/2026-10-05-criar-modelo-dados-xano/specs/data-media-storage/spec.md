## Purpose

Definir a persistência unificada de filmes, séries, animes e livros, permitindo que diferentes categorias de mídia sejam identificadas e utilizadas pelo Codeboxd.

## ADDED Requirements

### Requirement: Persistent media identity

The system SHALL persist a unique internal identity for each stored media item.

#### Scenario: Storing a media item

- **WHEN** a media item is registered in the system
- **THEN** the system SHALL assign or maintain a unique internal identity

### Requirement: Supported media categories

The system SHALL persist the category associated with every media item.

Supported categories SHALL include:

- Movie
- Series
- Anime
- Book

#### Scenario: Storing a supported media category

- **WHEN** a supported media item is stored
- **THEN** the system SHALL associate the item with its media category

### Requirement: External media identity

The system SHALL persist the external source and external identifier for media originating from external sources.

#### Scenario: Storing externally sourced media

- **WHEN** media information is obtained from an external source
- **THEN** the system SHALL preserve the source and external identifier

### Requirement: Media information persistence

The system SHALL persist the available identifying information required to represent a media item.

#### Scenario: Retrieving stored media

- **WHEN** a stored media item is requested
- **THEN** the system SHALL provide its available persisted identifying information