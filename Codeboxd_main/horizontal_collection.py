"""Native horizontal regions. Pointer movement stays entirely in the browser."""
import re
import reflex as rx


def _identity(rail_id: str):
    if not re.fullmatch(r'[a-z][a-z0-9_-]*', rail_id):
        raise ValueError('Use a stable, unique horizontal collection id')
    return rail_id


def rail_controls(rail_id: str, label: str) -> rx.Component:
    rail_id = _identity(rail_id)
    return rx.el.div(*[
        rx.el.button(rx.icon('chevron-left' if direction < 0 else 'chevron-right', size=19),
            type='button', class_name='shelf-arrow',
            aria_label=('Anteriores: ' if direction < 0 else 'Próximos: ') + label,
            aria_controls=rail_id, custom_attrs={'data-rail-direction': str(direction)})
        for direction in (-1, 1)], class_name='shelf-controls')


def horizontal_rail(*children, rail_id: str, label: str, class_name='catalog-rail') -> rx.Component:
    return rx.el.div(*children, id=_identity(rail_id), class_name=class_name,
        role='region', aria_label=label, tab_index=0,
        custom_attrs={'data-codeboxd-rail': 'true'})
