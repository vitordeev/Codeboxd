## Context

See `proposal.md` for the user-visible failure. `rx.upload` currently renders a
separate “Carregar imagem” button. The form's `on_submit` only passes ordinary
form fields; the existing state stages the image locally and later sends it as
`image_upload` to the existing multipart endpoint.

## Goals / Non-Goals

**Goals:** choosing a photo starts the existing staging flow automatically;
the post form cannot submit while a selected photo has not finished staging;
users can remove a staged or rejected selection and retain the current preview
and draft behavior.

**Non-Goals:** changing Xano endpoints, storage, image formats/size limits,
authentication, or feed rendering.

## Decisions

- Bind `rx.upload_files` to the upload component's `on_drop` trigger, as
  documented by Reflex for uploads from a form. This removes the extra manual
  button that currently allows users to publish without the selected image.
- Use the browser's selected-file state together with the staged filename to
  disable post submission until a selected image has been staged. The server
  continues to send the staged image and post fields together using the
  existing multipart helper.
- Keep an explicit clear-selection action and the existing remove-image action
  so a failed/rejected selection does not trap the user in the editor.

## Risks / Trade-offs

- A browser may reject an image before the state handler receives it; expose a
  clear/reselect path and test invalid and failed uploads.
- Staging may finish after the user attempts to submit; the submit guard must
  use both selected-file and staged-file state, rather than relying only on a
  loading label.

## Migration Plan

No backend migration or remote publication is required. Validate locally with
mocked multipart responses and a Reflex compile. Roll back the UI trigger and
submit guard if the upload component does not emit the expected event in the
installed Reflex version.
