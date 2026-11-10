"""Approved Lume scenes, rendered inline so theme variables are inherited."""
from functools import lru_cache
from itertools import count
from pathlib import Path
import xml.etree.ElementTree as ET
import reflex as rx

SCENES = ("onboarding", "empty", "not-found", "error", "success", "loading", "offline", "no-results")
_ASSETS = Path(__file__).resolve().parents[1] / "assets" / "illustrations" / "lume"
_INSTANCES = count()
_TAGS = {"svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}


@lru_cache(maxsize=8)
def _scene(name: str) -> ET.Element:
    return ET.parse(_ASSETS / (name + ".svg")).getroot()


def Illustration(name: str, size: str = "md", *, label: str | None = None, class_name: str = "") -> rx.Component:
    """Decorative by default; provide label for an informative illustration.

    Unknown scene names safely use the empty scene. Only repository-owned,
    whitelisted SVG elements are loaded; no user-provided markup is accepted.
    """
    scene = name if name in SCENES else "empty"
    if size not in {"sm", "md", "lg"}:
        raise ValueError("Illustration size must be sm, md or lg")
    if label is not None and not label.strip():
        raise ValueError("An informative illustration needs a nonempty label")
    prefix = "lume-" + str(next(_INSTANCES)) + "-"

    def component(node):
        tag = node.tag.rsplit("}", 1)[-1]
        if tag not in _TAGS:
            raise ValueError("Unsupported illustration element: " + tag)
        attrs = {key: value for key, value in node.attrib.items() if key != "xmlns"}
        if "id" in attrs:
            attrs["id"] = prefix + attrs["id"]
        if tag == "svg":
            attrs.update({"width": "320", "height": "240", "focusable": "false"})
            if label is None:
                attrs["aria-hidden"] = "true"
            else:
                attrs.update({"role": "img", "aria-label": label})
        factory = rx.el.svg if tag == "svg" else getattr(rx.el.svg, tag)
        return factory(*[component(child) for child in node], custom_attrs=attrs)

    return rx.el.span(component(_scene(scene)),
        class_name=("cb-illustration cb-illustration-" + size + " " + class_name).strip(),
        custom_attrs={"data-illustration": scene})


def empty_state(message, *actions, name: str = "empty") -> rx.Component:
    return rx.el.div(Illustration(name, "sm"), rx.el.p(message), *actions,
                     class_name="empty-state cb-illustrated-state")
