"""Shared, presentation-only feedback driven by existing loading flags."""
import reflex as rx
from .illustrations import Illustration


def loading_icon() -> rx.Component:
    return rx.el.span(class_name="cb-loading-wheel", aria_hidden=True)


def skeletons(variant: str = "cards", count: int = 3) -> rx.Component:
    if variant not in {"cards", "rows"}:
        raise ValueError("Skeleton variant must be cards or rows")
    return rx.el.div(
        *[rx.el.div(
            rx.el.span(class_name="cb-skeleton-picture"),
            rx.el.div(rx.el.span(class_name="cb-skeleton-line"),
                      rx.el.span(class_name="cb-skeleton-line cb-skeleton-short"),
                      class_name="cb-skeleton-copy"),
            class_name="cb-skeleton-item", key=str(index))
          for index in range(max(1, min(count, 6)))],
        class_name="cb-skeletons cb-skeletons-" + variant,
        aria_hidden=True,
    )


def loading_status(message: str = "Carregando…", *, variant: str = "inline", count: int = 3) -> rx.Component:
    return rx.el.div(
        rx.el.div(loading_icon(), rx.el.span(message), class_name="cb-loading-label",
                  role="status", aria_live="polite", aria_atomic=True),
        Illustration("loading", "sm") if variant == "rows" else rx.fragment(),
        skeletons(variant, count) if variant != "inline" else rx.fragment(),
        class_name="cb-loading cb-loading-" + variant,
    )
