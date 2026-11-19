"""Canonical fixture-only state, registered before the application is created."""
import reflex as rx
import asyncio


class ControlsFixture(rx.State):
    message: str = ''
    opened: bool = False
    working: bool = False

    @rx.event
    def fail(self, form: dict):
        self.message = 'Não foi possível salvar. Seu texto foi preservado para tentar novamente.'

    @rx.event
    def open_editor(self):
        self.opened = True

    @rx.event
    def set_opened(self, value: bool):
        self.opened = value

    @rx.event
    def no_operation(self):
        pass

    @rx.event
    async def simulate_loading(self):
        self.working = True
        yield
        await asyncio.sleep(0.8)
        self.working = False
