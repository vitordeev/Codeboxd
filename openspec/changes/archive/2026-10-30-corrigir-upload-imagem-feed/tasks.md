## Implementation

- [x] 1.1 Start image staging when a user selects/drops a photo and verify the picker binds its upload handler to `on_drop` while preserving preview and removal behavior.
- [x] 1.2 Prevent the post form from publishing while a selected image has not been staged; verify selection-state disables submit and provides a clear/reselect path after failure.

## Validation

- [x] 2.1 Add regression coverage that the picker auto-stages, multipart publication includes file and post fields, and a failed upload preserves the draft without a text-only write.
- [x] 2.2 Run focused tests, the complete local test suite, Reflex compile and OpenSpec validation; record results and any browser/remote limitations.
