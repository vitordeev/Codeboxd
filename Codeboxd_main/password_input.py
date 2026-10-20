"""Password input with an independent visibility control."""

import reflex as rx


class PasswordInput(rx.ComponentState):
    visible: bool = False

    @rx.event
    def toggle_visibility(self):
        self.visible = not self.visible

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        input_class = props.pop('class_name', '')
        return rx.el.div(
            rx.el.input(
                type=rx.cond(cls.visible, 'text', 'password'),
                class_name=input_class,
                style={'padding_right': '3.25rem'},
                **props,
            ),
            rx.el.button(
                rx.icon(rx.cond(cls.visible, 'eye-off', 'eye'), size=19),
                type='button',
                on_click=cls.toggle_visibility,
                aria_label=rx.cond(cls.visible, 'Ocultar senha', 'Mostrar senha'),
                aria_pressed=cls.visible,
                class_name='password-visibility-toggle',
            ),
            class_name='password-visibility-field',
        )


password_input = PasswordInput.create
