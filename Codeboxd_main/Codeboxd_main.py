"""CodeBoxd application routes for the current authentication milestone."""

import reflex as rx

from .pages.login import HEAD_COMPONENTS, login_page
from .pages.account import account_page, signup_page
from .state.auth_state import AuthState
from .state.social import SocialState
from .pages.social import discovery_page, media_page, library_page, community_page, profile_page, feed_page, lists_page


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Redireciona a raiz do site direto pro login por enquanto.
    return rx.fragment(
        rx.script("window.location.href = '/login'"),
    )


def admin_placeholder() -> rx.Component:
    # Página temporária só pra confirmar que o login -> redirect está funcionando.
    # O agente de IA vai substituir isso pelas telas reais do admin (tasks.md).
    return rx.center(
        rx.vstack(
            rx.heading("Administração do CodeBoxd", color="#F5C518"),
            rx.text("Sessão administrativa verificada. O painel está em desenvolvimento."),
            rx.link("Minha conta", href="/conta"),
            rx.button(
                "Sair",
                on_click=AuthState.logout,
                bg="#3A2F16",
                color="#F3F2ED",
                margin_top="1em",
            ),
            spacing="4",
        ),
        height="100vh",
        width="100%",
        bg="#0D0D0D",
        color="#F3F2ED",
    )


def protected_admin() -> rx.Component:
    return rx.cond(AuthState.is_admin, admin_placeholder(), rx.center("Verificando acesso…", min_height="100vh"))


app = rx.App(head_components=HEAD_COMPONENTS, html_lang="pt-BR")
app.add_page(discovery_page, route="/", on_load=SocialState.visit('home'))
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/cadastro")
app.add_page(profile_page, route="/perfil/[profile_id]", on_load=SocialState.visit('profile'))
app.add_page(profile_page, route="/conta", on_load=SocialState.visit('profile'))
app.add_page(media_page, route="/obra/[media_id]", on_load=SocialState.visit('media'))
app.add_page(media_page, route="/obra", on_load=SocialState.visit('external'))
app.add_page(library_page, route="/biblioteca", on_load=SocialState.visit('library'))
app.add_page(community_page, route="/comunidade", on_load=SocialState.visit('community'))
app.add_page(feed_page, route="/feed", on_load=SocialState.visit('feed'))
app.add_page(lists_page, route="/listas", on_load=SocialState.visit('lists'))
app.add_page(protected_admin, route="/admin", on_load=AuthState.guard_admin)
