"""CodeBoxd application routes for the current authentication milestone."""

import reflex as rx

from .pages.login import HEAD_COMPONENTS, login_page
from .pages.admin import admin_login_page, admin_dashboard_page, admin_users_page, admin_catalog_page, admin_reports_page
from .pages.admin_demo import admin_demo_page
from .pages.account import account_page, signup_page, password_reset_page
from .state.auth_state import AuthState
from .state.admin import AdminState
from .state.social import SocialState
from .pages.social import discovery_page, media_page, library_page, community_page, profile_page, feed_page, lists_page


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Redireciona a raiz do site direto pro login por enquanto.
    return rx.fragment(
        rx.script("window.location.href = '/login'"),
    )


def protected_admin() -> rx.Component:
    return rx.cond(AdminState.is_admin, admin_dashboard_page(), rx.center("Verificando acesso…", min_height="100vh"))


app = rx.App(head_components=HEAD_COMPONENTS, html_lang="pt-BR")
app.add_page(discovery_page, route="/", on_load=SocialState.visit('home'))
app.add_page(login_page, route="/login")
app.add_page(admin_login_page, route="/admin/login", title="Acesso administrativo | Codeboxd",
             on_load=AuthState.guard_admin_login)
app.add_page(signup_page, route="/cadastro")
app.add_page(password_reset_page, route="/redefinir-senha")
app.add_page(profile_page, route="/perfil/[profile_id]", on_load=SocialState.visit('profile'))
app.add_page(profile_page, route="/conta", on_load=SocialState.visit('profile'))
app.add_page(media_page, route="/obra/[media_id]", on_load=SocialState.visit('media'))
app.add_page(media_page, route="/obra", on_load=SocialState.visit('external'))
app.add_page(library_page, route="/biblioteca", on_load=SocialState.visit('library'))
app.add_page(community_page, route="/comunidade", on_load=SocialState.visit('community'))
app.add_page(feed_page, route="/feed", on_load=SocialState.visit('feed'))
app.add_page(lists_page, route="/listas", on_load=SocialState.visit('lists'))
app.add_page(protected_admin, route="/admin", on_load=AdminState.load_dashboard)
app.add_page(admin_users_page, route="/admin/users", on_load=AdminState.guard_users_page,
             title="Usuários | Administração | Codeboxd")
app.add_page(lambda: admin_catalog_page("movie"), route="/admin/catalog/movies",
             on_load=AdminState.load_catalog_movies, title="Filmes | Administração | Codeboxd")
app.add_page(lambda: admin_catalog_page("series"), route="/admin/catalog/series",
             on_load=AdminState.load_catalog_series, title="Séries | Administração | Codeboxd")
app.add_page(lambda: admin_catalog_page("book"), route="/admin/catalog/books",
             on_load=AdminState.load_catalog_books, title="Livros | Administração | Codeboxd")
app.add_page(lambda: admin_catalog_page("anime"), route="/admin/catalog/anime",
             on_load=AdminState.load_catalog_anime, title="Animes | Administração | Codeboxd")
app.add_page(admin_demo_page, route="/admin/demo", title="Amostra fictícia | Administração | Codeboxd")
app.add_page(admin_reports_page, route="/admin/reports", on_load=AdminState.load_reports,
             title="Reports | Administração | Codeboxd")
