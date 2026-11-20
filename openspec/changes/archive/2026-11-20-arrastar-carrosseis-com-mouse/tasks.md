# Tasks

## 1. Implement mouse dragging

- [x] 1.1 Add idempotent client-side pointer handling to the catalog rail, with a horizontal-intent threshold, pointer capture and cleanup; add focused browser tests for drag direction, click threshold, same-gesture click suppression, vertical intent, cancellation and reinitialization, verifying pointer movement does not emit Reflex application events. [Evidence](validation.md#1-implementation-and-browser-interaction).

## 2. Validate shelf integration

- [x] 2.1 Verify in the app that dragging does not break card clicks, keyboard navigation, native touch/trackpad scrolling, or scroll-triggered load-more behavior, including a shelf without overflow; run the targeted tests, Reflex compile, `openspec validate arrastar-carrosseis-com-mouse --type change` and `git diff --check`, recording results and limitations in the change. [Evidence](validation.md#2-integration-and-regressions).

## 3. Sync the main specification

- [x] 3.1 Add both drag and interaction-preservation requirements to the consolidated `media-discovery` spec and validate the main specs. [Evidence](validation.md#3-main-specification-sync).
