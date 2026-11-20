## MODIFIED Requirements

### Requirement: Separate personal and public list discovery
The system SHALL display only the authenticated owner's lists in the personal list collection. Other users' public lists SHALL be shown in a separately identified discovery context with ownership distinguishable. Visitors SHALL receive only public discovery content. The authenticated `/listas` page MUST NOT show an “Explorar listas públicas” button; it MUST retain the personal lists control and visitors MUST continue to see public lists.

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

#### Scenario: Authenticated list page omits public exploration control
- **WHEN** an authenticated user opens `/listas`
- **THEN** the page shows the personal lists control without an “Explorar listas públicas” button

#### Scenario: Personal list actions appear beside each other
- **WHEN** an authenticated user opens their personal list collection
- **THEN** “Minhas listas” and “Criar lista” SHALL appear in the same responsive action row
- **AND** “Criar lista” SHALL remain unavailable outside the personal collection
