# Design

## Context

See `proposal.md` for motivation and `specs/media-discovery/spec.md` for behavior. The current catalog shelves use native horizontal overflow and scroll snapping, are keyboard-focusable, and use an `on_scroll` callback to load more results; they do not currently render arrow controls. The earlier UI/UX implementation was canceled and reverted; its artifacts are historical references, not active code.

## Goals / Non-Goals

**Goals:**
- Add mouse dragging to the existing catalog shelf without changing its data flow or loading behavior.
- Keep pointer movement and scrolling in the browser, independent of Reflex server state.
- Preserve clicks, keyboard access, touch/trackpad scrolling, and vertical page scrolling.

**Non-Goals:**
- Change catalog layout, card actions, pagination, or loading more results.
- Add dragging to unrelated feed or recommendation components that do not use the catalog shelf.
- Add dependencies or change APIs, Xano contracts, or persistent state.

## Decisions

- Implement the gesture as a small client-side behavior attached to the existing catalog rail. Use Pointer Events and the rail's native horizontal scroll position rather than introducing a carousel library or sending per-movement events to Reflex.
- Start only for the primary mouse button. Require at least 8 CSS pixels of predominantly horizontal movement before entering drag mode; this lets ordinary clicks and vertical page scrolling proceed normally.
- Capture the pointer only after drag intent is established. While dragging, update the rail scroll position and apply a temporary dragging style; restore transient state on pointer up, cancellation, lost capture, blur, or teardown.
- Suppress only the click associated with a completed horizontal drag or a rejected vertical-intent gesture that crossed the threshold. Do not suppress keyboard-generated activation or a later click. Keep keyboard focus behavior as an alternative; do not add new controls.
- Avoid global `preventDefault`, touch-specific gesture overrides, and permanent text-selection changes so native touch, trackpad, and page scrolling remain intact.
- Validate the interaction with focused browser tests for drag direction, click threshold, click suppression, keyboard/control use, vertical intent, cancellation, and repeated initialization. Confirm pointer movement does not create Reflex application events.

Alternatives considered: retaining arrows alone does not meet the requested direct manipulation; implementing drag in Reflex handlers would add server events and latency; a carousel dependency would be disproportionate to the existing native overflow rail.

## Risks / Trade-offs

- [A drag can accidentally open a card] → Start only after a horizontal intent threshold and suppress only the click from that gesture.
- [Mouse capture can leave transient styles or selection state behind] → Centralize cleanup for pointer completion, cancellation, lost capture, blur, and component removal.
- [Gesture handling can interfere with vertical scroll or touch input] → Restrict custom handling to primary mouse input and do not alter global or touch scrolling behavior.
- [A repeated script load can install duplicate listeners] → Make initialization idempotent and verify it after rerender/reinitialization.

## Migration Plan

No persistent data or backend migration is needed. Add the client behavior and its styles behind the existing catalog rail, validate locally, and remove only the behavior if rollback is needed; retain the native rail and its current controls.
