"""Administrative sign-in page."""
import reflex as rx

from ..state.auth_state import AuthState
from ..state.admin import AdminState
from .login import _logo_icon


def admin_login_page() -> rx.Component:
    return rx.el.main(
        rx.el.section(
            rx.el.a(
                _logo_icon(),
                rx.el.span("code", rx.el.span("boxd", class_name="brand-yellow")),
                href="/",
                class_name="brand admin-login-brand",
                aria_label="Codeboxd — início",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("shield-check", size=22),
                    class_name="admin-login-icon",
                    aria_hidden="true",
                ),
                rx.el.p("ÁREA RESTRITA", class_name="admin-login-eyebrow"),
                rx.el.h1("Acesso administrativo", class_name="admin-login-title"),
                rx.el.p(
                    "Entre com uma conta autorizada para gerenciar o Codeboxd.",
                    class_name="admin-login-description",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("E-mail", html_for="admin_email", class_name="admin-login-label"),
                        rx.el.input(
                            id="admin_email", name="email", type="email", required=True,
                            auto_complete="username", placeholder="voce@exemplo.com",
                            class_name="admin-login-input",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Senha", html_for="admin_password", class_name="admin-login-label"),
                        rx.el.div(
                            rx.el.input(
                                id="admin_password", name="password",
                                type=rx.cond(AuthState.admin_password_visible, "text", "password"),
                                required=True, auto_complete="current-password",
                                placeholder="Sua senha", class_name="admin-login-input admin-password-input",
                            ),
                            rx.el.button(
                                rx.icon(rx.cond(AuthState.admin_password_visible, "eye-off", "eye"), size=18),
                                type="button", on_click=AuthState.toggle_admin_password,
                                aria_label=rx.cond(AuthState.admin_password_visible, "Ocultar senha", "Mostrar senha"),
                                class_name="admin-password-toggle",
                            ),
                            class_name="admin-password-field",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(type="checkbox", name="remember", default_checked=True),
                            " Manter sessão neste dispositivo",
                            class_name="admin-remember-label",
                        ),
                        rx.el.a("Esqueci minha senha", href="/redefinir-senha", class_name="admin-login-link"),
                        class_name="admin-login-options",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.p(AuthState.error_message, role="alert", class_name="admin-login-error"),
                    ),
                    rx.el.button(
                        rx.cond(AuthState.is_loading, "Verificando acesso…", "Entrar na administração"),
                        type="submit", disabled=AuthState.is_loading,
                        class_name="admin-login-submit",
                    ),
                    on_submit=AuthState.admin_login,
                    class_name="admin-login-form",
                ),
                class_name="admin-login-card",
            ),
            rx.el.a("Voltar ao login do Codeboxd", href="/login", class_name="admin-login-back"),
            class_name="admin-login-layout",
        ),
        class_name="admin-login-page",
    )


def _metric_card(title: str, key: str, icon: str, detail: str) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(rx.icon(icon, size=19), class_name="admin-metric-icon"),
            rx.el.span(title, class_name="admin-metric-label"),
            class_name="admin-metric-heading",
        ),
        rx.el.p(AdminState.dashboard_stats[key], class_name="admin-metric-value"),
        rx.el.p(detail, class_name="admin-metric-detail"),
        class_name="admin-metric-card",
    )


def _recent_post(item: dict[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.div(rx.icon("message-square-text", size=18), class_name="admin-activity-icon"),
            rx.el.div(
                rx.el.p("Publicação #" + item['id'], class_name="admin-activity-title"),
                rx.el.p("Usuário #" + item['user_id'], class_name="admin-activity-detail"),
            ),
            rx.el.time(item['created_at'], class_name="admin-activity-time"),
            class_name="admin-activity-row",
        ),
        class_name="admin-activity-item",
    )


def _pending_report(item: dict[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.p("Report #" + item["id"] + " · " + item["target_type"], class_name="admin-activity-title"),
            rx.el.p("Motivo: " + item["reason"], class_name="admin-activity-detail"),
            rx.el.time(item["created_at"], class_name="admin-activity-time"),
            class_name="admin-activity-row",
        ),
        class_name="admin-activity-item",
    )


def _admin_sidebar(active: str) -> rx.Component:
    return rx.el.aside(
        rx.el.p("GERENCIAMENTO", class_name="admin-sidebar-label"),
        rx.el.a(
            rx.icon("layout-dashboard", size=17), "Dashboard", href="/admin",
            class_name=rx.cond(active == "dashboard", "admin-sidebar-active", ""),
        ),
        rx.el.a(
            rx.icon("users-round", size=17), "Usuários", href="/admin/users",
            class_name=rx.cond(active == "users", "admin-sidebar-active", ""),
        ),
        rx.el.a("Filmes", href="/admin/catalog/movies",
            class_name=rx.cond(active == "movie", "admin-sidebar-active", "")),
        rx.el.a("Séries", href="/admin/catalog/series",
            class_name=rx.cond(active == "series", "admin-sidebar-active", "")),
        rx.el.a("Livros", href="/admin/catalog/books",
            class_name=rx.cond(active == "book", "admin-sidebar-active", "")),
        rx.el.a("Animes", href="/admin/catalog/anime",
            class_name=rx.cond(active == "anime", "admin-sidebar-active", "")),
        rx.el.a("Reports", href="/admin/reports",
            class_name=rx.cond(active == "reports", "admin-sidebar-active", "")),
        rx.el.a("Voltar ao website", href="/", class_name="admin-sidebar-home"),
        class_name="admin-sidebar",
    )


def admin_dashboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.a(
                _logo_icon(),
                rx.el.span("code", rx.el.span("boxd", class_name="brand-yellow")),
                href="/",
                class_name="brand admin-dashboard-brand",
                aria_label="Codeboxd — início",
            ),
            rx.el.div(
                rx.el.span("Administração", class_name="admin-header-label"),
                rx.el.button("Sair", type="button", on_click=AdminState.logout,
                    class_name="quiet-button admin-logout-button"),
                class_name="admin-header-actions",
            ),
            class_name="admin-dashboard-header",
        ),
        rx.el.main(
            _admin_sidebar("dashboard"),
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        rx.el.p("VISÃO GERAL", class_name="admin-page-eyebrow"),
                        rx.el.h1("Dashboard", class_name="admin-page-title"),
                        rx.el.p("Acompanhe a atividade atual do Codeboxd.", class_name="admin-page-description"),
                        rx.cond(
                            AdminState.dashboard_updated_at != "",
                            rx.el.p("Atualizado em " + AdminState.dashboard_updated_at,
                                class_name="admin-dashboard-updated"),
                            rx.fragment(),
                        ),
                    ),
                    rx.el.button(
                        rx.icon("refresh-cw", size=16),
                        rx.el.span(rx.cond(AdminState.dashboard_loading, "Atualizando…", "Atualizar")),
                        type="button", on_click=AdminState.load_dashboard,
                        disabled=AdminState.dashboard_loading,
                        class_name="quiet-button admin-refresh-button",
                    ),
                    class_name="admin-page-heading",
                ),
                rx.cond(
                    AdminState.dashboard_error != "",
                    rx.el.div(
                        rx.icon("triangle-alert", size=18),
                        rx.el.p(AdminState.dashboard_error),
                        role="alert", class_name="admin-dashboard-error",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.dashboard_loading,
                    rx.el.p("Carregando os indicadores…", role="status", class_name="admin-loading-message"),
                    rx.fragment(),
                ),
                rx.el.div(
                    _metric_card("Usuários", "users_total", "users-round", "Contas cadastradas"),
                    _metric_card("Publicações", "posts_total", "messages-square", "Histórias compartilhadas"),
                    _metric_card("Obras no catálogo", "media_total", "clapperboard", "Filmes, séries, livros e animes"),
                    _metric_card("Reports pendentes", "reports_pending", "flag", "Aguardando análise"),
                    class_name="admin-metrics-grid",
                ),
                rx.el.section(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2("Reports pendentes", class_name="admin-section-title"),
                            rx.el.p("Denúncias que aguardam revisão.", class_name="admin-section-description"),
                        ),
                        rx.el.a("Abrir fila", href="/admin/reports", class_name="admin-activity-link"),
                        class_name="admin-section-heading",
                    ),
                    rx.cond(
                        AdminState.pending_reports.length() > 0,
                        rx.el.ul(rx.foreach(AdminState.pending_reports, _pending_report), class_name="admin-activity-list"),
                        rx.el.div(rx.icon("inbox", size=24), rx.el.p("Nenhum report pendente."), class_name="admin-activity-empty"),
                    ),
                    class_name="admin-activity-card",
                ),
                rx.el.section(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2("Publicações recentes", class_name="admin-section-title"),
                            rx.el.p("Atividade recente da comunidade.", class_name="admin-section-description"),
                        ),
                        class_name="admin-section-heading",
                    ),
                    rx.cond(
                        AdminState.recent_posts.length() > 0,
                        rx.el.ul(rx.foreach(AdminState.recent_posts, _recent_post), class_name="admin-activity-list"),
                        rx.el.div(
                            rx.icon("inbox", size=25),
                            rx.el.p("Nenhuma publicação recente para exibir."),
                            class_name="admin-activity-empty",
                        ),
                    ),
                    class_name="admin-activity-card",
                ),
                class_name="admin-dashboard-content",
            ),
            class_name="admin-dashboard-layout",
        ),
        class_name="admin-dashboard-page",
    )


def _admin_user_row(user: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.p(user["name"], class_name="admin-user-name"),
                rx.el.p("@" + user["username"], class_name="admin-user-username"),
            ),
            rx.el.div(
                rx.el.span("ID " + user["id"], class_name="admin-user-id"),
                rx.el.span(user["role"], class_name="admin-user-role"),
                rx.el.span(
                    rx.cond(user["account_status"] == "disabled", "Suspensa", "Ativa"),
                    class_name=rx.cond(user["account_status"] == "disabled", "admin-status-disabled", "admin-status-active"),
                ),
                class_name="admin-user-badges",
            ),
            class_name="admin-user-main",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button("Detalhes", type="button", on_click=AdminState.toggle_user_details(user["id"]),
                    class_name="quiet-button admin-user-details-toggle",
                    aria_expanded=AdminState.user_details_id == user["id"]),
                rx.el.button(
                    rx.cond(user["account_status"] == "disabled", "Reativar", "Suspender"),
                    type="button",
                    on_click=AdminState.open_user_status_dialog(
                        user["id"], rx.cond(user["account_status"] == "disabled", "active", "disabled")
                    ),
                    class_name=rx.cond(
                        user["account_status"] == "disabled", "quiet-button admin-user-activate", "quiet-button admin-user-disable"
                    ),
                ),
                class_name="admin-user-actions",
            ),
            rx.cond(
                AdminState.user_details_id == user["id"],
                rx.el.div(
                    rx.el.span("Identificador: " + user["id"]),
                    rx.el.span("Criada em: " + rx.cond(user["created_at"] != "", user["created_at"], "Não informado")),
                    rx.el.span("Papel: " + user["role"]),
                    rx.el.span("Acesso: " + rx.cond(user["account_status"] == "disabled", "Suspenso", "Ativo")),
                    class_name="admin-user-details",
                ),
                rx.fragment(),
            ),
            class_name="admin-user-controls",
        ),
        class_name="admin-user-row",
    )


def admin_users_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.a(
                _logo_icon(), rx.el.span("code", rx.el.span("boxd", class_name="brand-yellow")),
                href="/", class_name="brand admin-dashboard-brand", aria_label="Codeboxd — início",
            ),
            rx.el.div(
                rx.el.span("Administração", class_name="admin-header-label"),
                rx.el.button("Sair", type="button", on_click=AdminState.logout,
                    class_name="quiet-button admin-logout-button"),
                class_name="admin-header-actions",
            ),
            class_name="admin-dashboard-header",
        ),
        rx.el.main(
            _admin_sidebar("users"),
            rx.el.section(
                rx.el.p("GERENCIAMENTO DE CONTAS", class_name="admin-page-eyebrow"),
                rx.el.h1("Usuários", class_name="admin-page-title"),
                rx.el.p("Pesquise contas e gerencie seu acesso ao Codeboxd.", class_name="admin-page-description"),
                rx.el.form(
                    rx.el.label("Buscar por nome, usuário ou ID", html_for="admin-user-search",
                        class_name="admin-search-label"),
                    rx.el.div(
                        rx.el.input(
                            id="admin-user-search", name="search", type="search", required=True,
                            placeholder="Ex.: nome de usuário ou 123", class_name="admin-search-input",
                            default_value=AdminState.users_query,
                        ),
                        rx.el.select(
                            rx.el.option("Todos os estados", value=""),
                            rx.el.option("Ativas", value="active"),
                            rx.el.option("Suspensas", value="disabled"),
                            name="account_status", default_value=AdminState.users_status_filter,
                            class_name="admin-search-select",
                        ),
                        rx.el.select(
                            rx.el.option("Todos os papéis", value=""),
                            rx.el.option("Membro", value="member"),
                            rx.el.option("Moderador", value="moderator"),
                            rx.el.option("Admin", value="admin"),
                            name="role", default_value=AdminState.users_role_filter,
                            class_name="admin-search-select",
                        ),
                        rx.el.button(
                            rx.cond(AdminState.users_loading, "Buscando…", "Pesquisar"),
                            type="submit", disabled=AdminState.users_loading,
                            class_name="admin-search-submit",
                        ),
                        class_name="admin-search-controls",
                    ),
                    on_submit=AdminState.search_users,
                    class_name="admin-users-search",
                ),
                rx.cond(
                    AdminState.users_error != "",
                    rx.el.div(rx.icon("triangle-alert", size=18), rx.el.p(AdminState.users_error),
                        role="alert", class_name="admin-dashboard-error"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.users_notice != "",
                    rx.el.p(AdminState.users_notice, role="status", class_name="admin-users-notice"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.users_loading,
                    rx.el.p("Carregando contas…", role="status", class_name="admin-loading-message"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.users.length() > 0,
                    rx.el.section(
                        rx.el.p("Resultados: " + AdminState.users_total.to_string(), class_name="admin-users-count"),
                        rx.el.div(rx.foreach(AdminState.users, _admin_user_row), class_name="admin-users-list"),
                        rx.el.div(
                            rx.el.button("Anterior", type="button",
                                on_click=AdminState.change_users_page(AdminState.users_page - 1),
                                disabled=AdminState.users_page <= 1, class_name="quiet-button"),
                            rx.el.span("Página " + AdminState.users_page.to_string(), class_name="admin-page-number"),
                            rx.el.button("Próxima", type="button",
                                on_click=AdminState.change_users_page(AdminState.users_next_page),
                                disabled=AdminState.users_next_page == 0, class_name="quiet-button"),
                            class_name="admin-pagination",
                        ),
                        class_name="admin-users-results",
                    ),
                    rx.cond(
                        AdminState.users_query != "",
                        rx.el.div(rx.icon("user-round-search", size=24),
                            rx.el.p("Nenhuma conta encontrada para esta pesquisa."),
                            class_name="admin-activity-empty"),
                        rx.el.div(rx.icon("search", size=24),
                            rx.el.p("Pesquise por nome, usuário ou identificador para consultar contas."),
                            class_name="admin-activity-empty"),
                    ),
                ),
                class_name="admin-dashboard-content admin-users-content",
            ),
            class_name="admin-dashboard-layout",
        ),
        rx.cond(
            AdminState.user_action_id != "",
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(AdminState.user_action_status == "disabled", "Suspender conta?", "Reativar conta?"),
                        class_name="admin-dialog-title",
                    ),
                    rx.el.p(
                        rx.cond(
                            AdminState.user_action_status == "disabled",
                            "A pessoa deixará de acessar as operações protegidas até ser reativada.",
                            "A pessoa poderá voltar a acessar a conta após a próxima autenticação.",
                        ),
                        class_name="admin-dialog-copy",
                    ),
                    rx.el.label("Motivo (opcional)", html_for="admin-user-action-reason",
                        class_name="admin-search-label"),
                    rx.el.textarea(
                        id="admin-user-action-reason", value=AdminState.user_action_reason,
                        on_change=AdminState.set_user_action_reason,
                        max_length=500, class_name="admin-user-reason",
                    ),
                    rx.el.div(
                        rx.el.button("Cancelar", type="button", on_click=AdminState.close_user_status_dialog,
                            disabled=AdminState.user_action_loading, class_name="quiet-button"),
                        rx.el.button(
                            rx.cond(AdminState.user_action_loading, "Salvando…", "Confirmar"),
                            type="button", on_click=AdminState.confirm_user_status_change,
                            disabled=AdminState.user_action_loading,
                            class_name=rx.cond(AdminState.user_action_status == "disabled",
                                "admin-dialog-confirm-danger", "admin-dialog-confirm"),
                        ),
                        class_name="admin-dialog-actions",
                    ),
                    class_name="admin-confirm-dialog",
                    role="dialog", aria_modal="true", aria_label="Confirmar alteração de conta",
                ),
                class_name="admin-dialog-overlay",
            ),
            rx.fragment(),
        ),
        class_name="admin-dashboard-page",
    )


def _catalog_item_row(item: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.cond(
            item["cover_url"] != "",
            rx.el.img(src=item["cover_url"], alt="Capa de " + item["title"], class_name="admin-catalog-cover"),
            rx.el.div(rx.icon("clapperboard", size=20), class_name="admin-catalog-cover-empty"),
        ),
        rx.el.div(
            rx.el.p(item["title"], class_name="admin-user-name"),
            rx.el.p(
                rx.cond(item["year"] != "", item["year"] + " · ", "")
                + item["external_source"] + ":" + item["external_id"],
                class_name="admin-user-username",
            ),
            rx.el.p(item["description"], class_name="admin-catalog-description"),
            class_name="admin-catalog-copy",
        ),
        rx.el.button(
            "Editar", type="button", on_click=AdminState.open_catalog_editor(item),
            class_name="quiet-button admin-catalog-edit",
        ),
        class_name="admin-catalog-row",
    )


def admin_catalog_page(media_type: str) -> rx.Component:
    labels = {"movie": "Filmes", "series": "Séries", "book": "Livros", "anime": "Animes"}
    label = labels[media_type]
    return rx.el.div(
        rx.el.header(
            rx.el.a(
                _logo_icon(), rx.el.span("code", rx.el.span("boxd", class_name="brand-yellow")),
                href="/", class_name="brand admin-dashboard-brand", aria_label="Codeboxd — início",
            ),
            rx.el.div(
                rx.el.span("Administração", class_name="admin-header-label"),
                rx.el.button("Sair", type="button", on_click=AdminState.logout,
                    class_name="quiet-button admin-logout-button"),
                class_name="admin-header-actions",
            ),
            class_name="admin-dashboard-header",
        ),
        rx.el.main(
            _admin_sidebar(media_type),
            rx.el.section(
                rx.el.p("GERENCIAMENTO DO CATÁLOGO", class_name="admin-page-eyebrow"),
                rx.el.h1(label, class_name="admin-page-title"),
                rx.el.p("Pesquise e corrija os dados locais das obras sem alterar suas referências externas.",
                    class_name="admin-page-description"),
                rx.el.nav(
                    rx.el.a("Filmes", href="/admin/catalog/movies", class_name="admin-catalog-tab"),
                    rx.el.a("Séries", href="/admin/catalog/series", class_name="admin-catalog-tab"),
                    rx.el.a("Livros", href="/admin/catalog/books", class_name="admin-catalog-tab"),
                    rx.el.a("Animes", href="/admin/catalog/anime", class_name="admin-catalog-tab"),
                    class_name="admin-catalog-tabs",
                    aria_label="Tipo de obra",
                ),
                rx.el.details(
                    rx.el.summary("Adicionar obra", class_name="admin-catalog-create-summary"),
                    rx.el.p("Informe a fonte e o identificador externo. Se a identidade já existir, abriremos o registro atual.",
                        class_name="admin-page-description"),
                    rx.el.form(
                        rx.el.input(name="external_source", required=True, max_length=40,
                            placeholder=rx.cond(AdminState.catalog_type == "movie", "Fonte: tmdb",
                                rx.cond(AdminState.catalog_type == "series", "Fonte: tmdb",
                                    rx.cond(AdminState.catalog_type == "book", "Fonte: openlibrary", "Fonte: jikan ou kitsu"))),
                            class_name="admin-search-input"),
                        rx.el.input(name="external_id", required=True, max_length=100,
                            placeholder="Identificador externo (ex.: 329865)", class_name="admin-search-input"),
                        rx.el.input(name="title", required=True, max_length=500, placeholder="Título",
                            class_name="admin-search-input"),
                        rx.el.input(name="year", type="number", min=1800, max=2200, placeholder="Ano",
                            class_name="admin-search-input"),
                        rx.el.input(name="cover_url", type="url", max_length=1000,
                            placeholder="URL https da capa (opcional)", class_name="admin-search-input"),
                        rx.el.textarea(name="description", max_length=20000,
                            placeholder="Descrição (opcional)", class_name="admin-user-reason"),
                        rx.el.button(rx.cond(AdminState.catalog_create_loading, "Cadastrando…", "Validar e cadastrar"),
                            type="submit", disabled=AdminState.catalog_create_loading,
                            class_name="admin-search-submit"),
                        on_submit=AdminState.create_catalog_item,
                        class_name="admin-catalog-create-grid",
                    ),
                    class_name="admin-catalog-create",
                ),
                rx.el.form(
                    rx.el.label("Pesquisar título", html_for="admin-catalog-search", class_name="admin-search-label"),
                    rx.el.div(
                        rx.el.input(
                            id="admin-catalog-search", name="search", type="search",
                            placeholder="Digite o título da obra", class_name="admin-search-input",
                            default_value=AdminState.catalog_query,
                        ),
                        rx.el.button(
                            rx.cond(AdminState.catalog_loading, "Buscando…", "Pesquisar"),
                            type="submit", disabled=AdminState.catalog_loading, class_name="admin-search-submit",
                        ),
                        class_name="admin-catalog-search-controls",
                    ),
                    on_submit=AdminState.search_catalog,
                    class_name="admin-users-search",
                ),
                rx.cond(
                    AdminState.catalog_error != "",
                    rx.el.div(rx.icon("triangle-alert", size=18), rx.el.p(AdminState.catalog_error),
                        role="alert", class_name="admin-dashboard-error"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.catalog_notice != "",
                    rx.el.p(AdminState.catalog_notice, role="status", class_name="admin-users-notice"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.catalog_loading,
                    rx.el.p("Carregando catálogo…", role="status", class_name="admin-loading-message"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.catalog_items.length() > 0,
                    rx.el.section(
                        rx.el.p("Resultados: " + AdminState.catalog_total.to_string(), class_name="admin-users-count"),
                        rx.el.div(rx.foreach(AdminState.catalog_items, _catalog_item_row), class_name="admin-catalog-list"),
                        rx.el.div(
                            rx.el.button("Anterior", type="button",
                                on_click=AdminState.change_catalog_page(AdminState.catalog_page - 1),
                                disabled=AdminState.catalog_page <= 1, class_name="quiet-button"),
                            rx.el.span("Página " + AdminState.catalog_page.to_string(), class_name="admin-page-number"),
                            rx.el.button("Próxima", type="button",
                                on_click=AdminState.change_catalog_page(AdminState.catalog_next_page),
                                disabled=AdminState.catalog_next_page == 0, class_name="quiet-button"),
                            class_name="admin-pagination",
                        ),
                        class_name="admin-users-results",
                    ),
                    rx.cond(
                        AdminState.catalog_query != "",
                        rx.el.div(rx.icon("search-x", size=24), rx.el.p("Nenhuma obra encontrada para esta pesquisa."),
                            class_name="admin-activity-empty"),
                        rx.el.div(rx.icon("search", size=24), rx.el.p("Pesquise um título para carregar obras desta seção."),
                            class_name="admin-activity-empty"),
                    ),
                ),
                class_name="admin-dashboard-content admin-users-content",
            ),
            class_name="admin-dashboard-layout",
        ),
        rx.cond(
            AdminState.catalog_edit_id != "",
            rx.el.div(
                rx.el.form(
                    rx.el.h2("Editar obra", class_name="admin-dialog-title"),
                    rx.el.label("Título", html_for="catalog-edit-title", class_name="admin-search-label"),
                    rx.el.input(id="catalog-edit-title", value=AdminState.catalog_edit_title,
                        on_change=AdminState.set_catalog_edit_title, max_length=500, class_name="admin-search-input"),
                    rx.el.label("Descrição", html_for="catalog-edit-description", class_name="admin-search-label"),
                    rx.el.textarea(id="catalog-edit-description", value=AdminState.catalog_edit_description,
                        on_change=AdminState.set_catalog_edit_description, max_length=20000,
                        class_name="admin-user-reason"),
                    rx.el.label("URL segura da capa (HTTPS)", html_for="catalog-edit-cover", class_name="admin-search-label"),
                    rx.el.input(id="catalog-edit-cover", type="url", value=AdminState.catalog_edit_cover,
                        on_change=AdminState.set_catalog_edit_cover, max_length=1000, class_name="admin-search-input"),
                    rx.el.label("Ano", html_for="catalog-edit-year", class_name="admin-search-label"),
                    rx.el.input(id="catalog-edit-year", type="text", input_mode="numeric", max_length=4,
                        value=AdminState.catalog_edit_year, on_change=AdminState.set_catalog_edit_year,
                        class_name="admin-search-input"),
                    rx.el.p("ID local e identidade externa são preservados.", class_name="admin-dialog-copy"),
                    rx.el.div(
                        rx.el.button("Cancelar", type="button", on_click=AdminState.close_catalog_editor,
                            disabled=AdminState.catalog_edit_loading, class_name="quiet-button"),
                        rx.el.button(rx.cond(AdminState.catalog_edit_loading, "Salvando…", "Salvar alterações"),
                            type="button", on_click=AdminState.save_catalog_edit,
                            disabled=AdminState.catalog_edit_loading, class_name="admin-dialog-confirm"),
                        class_name="admin-dialog-actions",
                    ),
                    class_name="admin-confirm-dialog admin-catalog-editor",
                    role="dialog", aria_modal="true", aria_label="Editar obra do catálogo",
                ),
                class_name="admin-dialog-overlay",
            ),
            rx.fragment(),
        ),
        class_name="admin-dashboard-page",
    )


def _report_card(report: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.p("Report #" + report["id"], class_name="admin-user-name"),
                rx.el.p(
                    "Alvo: " + report["target_type"] + " #" + report["target_id"]
                    + " · Denunciante #" + report["reporter_user_id"],
                    class_name="admin-user-username",
                ),
                class_name="admin-report-header-copy",
            ),
            rx.el.span(report["status"], class_name="admin-user-role"),
            class_name="admin-report-heading",
        ),
        rx.el.div(
            rx.el.p("Motivo: " + report["reason"], class_name="admin-report-reason"),
            rx.cond(report["description"] != "", rx.el.p(report["description"], class_name="admin-report-description"), rx.fragment()),
            rx.cond(
                report["target_snapshot"] != "",
                rx.el.details(
                    rx.el.summary("Contexto salvo no envio do report"),
                    rx.el.pre(report["target_snapshot"], class_name="admin-report-snapshot"),
                    class_name="admin-report-context",
                ),
                rx.el.p("Sem snapshot disponível.", class_name="admin-report-description"),
            ),
            rx.cond(report["decision"] != "", rx.el.p("Decisão registrada: " + report["decision"], class_name="admin-report-decision"), rx.fragment()),
            class_name="admin-report-copy",
        ),
        rx.el.div(
            rx.el.button("Em análise", type="button",
                on_click=AdminState.open_report_review(report["id"], "reviewing"),
                disabled=AdminState.reports_loading, class_name="quiet-button"),
            rx.el.button("Resolver", type="button",
                on_click=AdminState.open_report_review(report["id"], "resolved"),
                disabled=AdminState.reports_loading, class_name="admin-dialog-confirm"),
            rx.el.button("Rejeitar", type="button",
                on_click=AdminState.open_report_review(report["id"], "rejected"),
                disabled=AdminState.reports_loading, class_name="admin-dialog-confirm-danger"),
            class_name="admin-report-actions",
        ),
        class_name="admin-report-card",
    )


def admin_reports_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.a(
                _logo_icon(), rx.el.span("code", rx.el.span("boxd", class_name="brand-yellow")),
                href="/", class_name="brand admin-dashboard-brand", aria_label="Codeboxd — início",
            ),
            rx.el.div(
                rx.el.span("Administração", class_name="admin-header-label"),
                rx.el.button("Sair", type="button", on_click=AdminState.logout,
                    class_name="quiet-button admin-logout-button"),
                class_name="admin-header-actions",
            ),
            class_name="admin-dashboard-header",
        ),
        rx.el.main(
            _admin_sidebar("reports"),
            rx.el.section(
                rx.el.p("MODERAÇÃO", class_name="admin-page-eyebrow"),
                rx.el.h1("Reports", class_name="admin-page-title"),
                rx.el.p("Revise o contexto salvo e registre uma decisão explícita. Abrir um report não altera o conteúdo alvo.",
                    class_name="admin-page-description"),
                rx.el.form(
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Pendentes", value="pending"),
                            rx.el.option("Em análise", value="reviewing"),
                            rx.el.option("Resolvidos", value="resolved"),
                            rx.el.option("Rejeitados", value="rejected"),
                            rx.el.option("Todos os estados", value=""),
                            name="status", default_value=AdminState.reports_status_filter,
                            class_name="admin-search-select",
                        ),
                        rx.el.select(
                            rx.el.option("Todos os tipos", value=""),
                            rx.el.option("Mensagens", value="message"),
                            rx.el.option("Publicações", value="post"),
                            rx.el.option("Comentários", value="comment"),
                            rx.el.option("Perfis", value="profile"),
                            rx.el.option("Obras", value="media"),
                            name="target_type", default_value=AdminState.reports_type_filter,
                            class_name="admin-search-select",
                        ),
                        rx.el.select(
                            rx.el.option("Todos os motivos", value=""),
                            rx.el.option("Spam", value="spam"),
                            rx.el.option("Assédio", value="harassment"),
                            rx.el.option("Conteúdo impróprio", value="inappropriate"),
                            rx.el.option("Outro", value="other"),
                            name="reason", default_value=AdminState.reports_reason_filter,
                            class_name="admin-search-select",
                        ),
                        rx.el.button("Filtrar", type="submit", disabled=AdminState.reports_loading,
                            class_name="admin-search-submit"),
                        class_name="admin-report-filters",
                    ),
                    on_submit=AdminState.search_reports,
                    class_name="admin-users-search",
                ),
                rx.cond(
                    AdminState.reports_error != "",
                    rx.el.div(rx.icon("triangle-alert", size=18), rx.el.p(AdminState.reports_error),
                        role="alert", class_name="admin-dashboard-error"),
                    rx.fragment(),
                ),
                rx.cond(AdminState.reports_notice != "",
                    rx.el.p(AdminState.reports_notice, role="status", class_name="admin-users-notice"), rx.fragment()),
                rx.cond(AdminState.reports_loading,
                    rx.el.p("Carregando reports…", role="status", class_name="admin-loading-message"), rx.fragment()),
                rx.cond(
                    AdminState.reports.length() > 0,
                    rx.el.section(
                        rx.el.p("Resultados: " + AdminState.reports_total.to_string(), class_name="admin-users-count"),
                        rx.el.div(rx.foreach(AdminState.reports, _report_card), class_name="admin-reports-list"),
                        rx.el.div(
                            rx.el.button("Anterior", type="button",
                                on_click=AdminState.change_reports_page(AdminState.reports_page - 1),
                                disabled=AdminState.reports_page <= 1, class_name="quiet-button"),
                            rx.el.span("Página " + AdminState.reports_page.to_string(), class_name="admin-page-number"),
                            rx.el.button("Próxima", type="button",
                                on_click=AdminState.change_reports_page(AdminState.reports_next_page),
                                disabled=AdminState.reports_next_page == 0, class_name="quiet-button"),
                            class_name="admin-pagination",
                        ),
                        class_name="admin-users-results",
                    ),
                    rx.el.div(rx.icon("inbox", size=24), rx.el.p("Nenhum report corresponde aos filtros."),
                        class_name="admin-activity-empty"),
                ),
                class_name="admin-dashboard-content admin-users-content",
            ),
            class_name="admin-dashboard-layout",
        ),
        rx.cond(
            AdminState.report_review_id != "",
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(AdminState.report_review_status == "reviewing", "Iniciar análise?",
                            rx.cond(AdminState.report_review_status == "resolved", "Resolver report?", "Rejeitar report?")),
                        class_name="admin-dialog-title",
                    ),
                    rx.el.p("Registre a justificativa. A alteração é auditada com o estado anterior, o novo e o ator autenticado.",
                        class_name="admin-dialog-copy"),
                    rx.el.label("Decisão ou nota de análise", html_for="admin-report-decision", class_name="admin-search-label"),
                    rx.el.textarea(id="admin-report-decision", value=AdminState.report_review_decision,
                        on_change=AdminState.set_report_review_decision, max_length=2000, class_name="admin-user-reason"),
                    rx.el.div(
                        rx.el.button("Cancelar", type="button", on_click=AdminState.close_report_review,
                            disabled=AdminState.report_review_loading, class_name="quiet-button"),
                        rx.el.button(rx.cond(AdminState.report_review_loading, "Salvando…", "Confirmar decisão"),
                            type="button", on_click=AdminState.save_report_review,
                            disabled=AdminState.report_review_loading, class_name="admin-dialog-confirm"),
                        class_name="admin-dialog-actions",
                    ),
                    class_name="admin-confirm-dialog", role="dialog", aria_modal="true",
                    aria_label="Registrar decisão de moderação",
                ),
                class_name="admin-dialog-overlay",
            ),
            rx.fragment(),
        ),
        class_name="admin-dashboard-page",
    )
