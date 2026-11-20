## ADDED Requirements

### Requirement: Login brand mark returns to the home page
The Codeboxd mark and wordmark on the login page MUST be a single accessible link to the public home page at `/`.

#### Scenario: Visitor returns home from login
- **WHEN** a visitor activates the Codeboxd mark on `/login`
- **THEN** the application navigates to `/`

#### Scenario: Assistive technology identifies the home link
- **WHEN** a visitor navigates the login page by accessible controls
- **THEN** the combined Codeboxd mark and wordmark expose an accessible name identifying the home page
