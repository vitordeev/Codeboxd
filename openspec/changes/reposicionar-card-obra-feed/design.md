## Context

See `proposal.md` for the visual goal. The post renderer currently places the
author row first, the personal image second and the linked work card after the
image.

## Goals / Non-Goals

**Goals:** group author identity and associated work in a responsive header;
keep the personal image and post body prominent and in their current order.

**Non-Goals:** changing feed data, card destinations, image-upload behavior,
likes, comments or backend contracts.

## Decisions

- Place the work card on the opposite side of the author identity in the same
  flex header row. This makes the association visible at a glance without
  inserting catalog content into the author's name or avatar.
- Keep the thumbnail compact and the title truncatable; use wrapping on narrow
  screens so the card remains reachable without forcing horizontal scrolling.
- Remove the duplicate card from below the photo so each post shows one work
  card only.

## Risks / Trade-offs

- Long author or work names may compete for header width → let the row wrap and
  constrain the card title while retaining the full work title as image/link
  accessible text.

## Migration Plan

No migration or rollback of data is required. Reverting the post component
restores the previous placement.
