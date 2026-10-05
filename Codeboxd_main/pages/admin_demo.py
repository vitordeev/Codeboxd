"""Read-only local preview populated with synthetic admin API responses."""
import json

import reflex as rx

from .admin import _logo_icon


_NAMES = [
    "Ana Oliveira", "Bruno Santos", "Camila Costa", "Diego Ferreira", "Elisa Almeida",
    "Felipe Souza", "Giovana Martins", "Henrique Lima", "Isabela Rocha", "João Carvalho",
    "Karina Nunes", "Lucas Ribeiro", "Marina Barros", "Nicolas Freitas", "Olívia Gomes",
    "Paulo Teixeira", "Quezia Mendes", "Rafael Cardoso", "Sofia Azevedo", "Tiago Moreira",
    "Ursula Vieira", "Vitor Campos", "Wesley Dias", "Yasmin Monteiro", "Zeca Pires",
]
_TITLES = [
    ("movie", "A Cidade de Vidro", "tmdb"), ("series", "Arquivo Aurora", "tmdb"),
    ("book", "O Jardim das Horas", "openlibrary"), ("anime", "Estação Nebulosa", "jikan"),
    ("movie", "Maré de Inverno", "tmdb"), ("series", "Pequenos Astros", "tmdb"),
    ("book", "Cartas para o Amanhã", "openlibrary"), ("anime", "Círculo de Papel", "kitsu"),
    ("movie", "Última Sessão", "tmdb"), ("series", "Mapa das Nuvens", "tmdb"),
    ("book", "Manual das Coisas Impossíveis", "openlibrary"), ("anime", "Jardim Lunar", "jikan"),
    ("movie", "O Som do Horizonte", "tmdb"), ("series", "Quarto 204", "tmdb"),
    ("book", "Pequena História do Tempo", "openlibrary"), ("anime", "A Última Lanterna", "kitsu"),
    ("movie", "Sete Estações", "tmdb"), ("series", "Depois da Chuva", "tmdb"),
    ("book", "Receitas para Outros Mundos", "openlibrary"), ("anime", "Vento de Outubro", "jikan"),
    ("movie", "O Peso das Estrelas", "tmdb"), ("series", "Linha de Retorno", "tmdb"),
    ("book", "O Atlas das Pequenas Ilhas", "openlibrary"), ("anime", "Clube do Cometa", "kitsu"),
    ("movie", "A Última Página", "tmdb"),
]
_REPORT_TARGETS = ["post", "comment", "message", "profile", "media", "post", "comment", "message"]
_REPORT_REASONS = ["spam", "harassment", "inappropriate", "other", "spam", "other", "harassment", "inappropriate"]

DEMO_USERS = [
    {
        "id": 1201 + i,
        "name": _NAMES[i],
        "username": f"leitor_{i + 1:02}",
        "role": "admin" if i == 0 else "moderator" if i in (4, 16) else "member",
        "account_status": "disabled" if i in (7, 18) else "active",
        "created_at": f"2026-{(i % 8) + 1:02}-{(i % 27) + 1:02}",
    }
    for i in range(25)
]
DEMO_CATALOG = [
    {
        "id": 4301 + i,
        "identity_key": f"{source}:{media_type}:{71000 + i}",
        "external_source": source,
        "external_id": str(71000 + i),
        "media_type": media_type,
        "title": title,
        "description": f"Registro fictício de demonstração para {title.lower()}; metadados editáveis sem alterar a identidade externa.",
        "cover_url": "",
        "year": 1998 + (i % 28),
    }
    for i, (media_type, title, source) in enumerate(_TITLES)
]
DEMO_REPORTS = [
    {
        "id": 8701 + i,
        "created_at": f"2026-09-{26 - i:02} 1{(i % 9)}:20:00",
        "reporter_user_id": 1201 + i * 3,
        "target_type": target,
        "target_id": 5500 + i,
        "reason": reason,
        "description": "Este é um relato fictício para mostrar o contexto que a moderação recebe.",
        "target_snapshot": {
            "body": f"Conteúdo de exemplo relacionado ao report {8701 + i}.",
            "sender_name": _NAMES[(i + 3) % len(_NAMES)] if target == "message" else None,
            "sent_at": f"2026-09-{26 - i:02}T10:15:00Z" if target == "message" else None,
        },
        "status": ["pending", "reviewing", "pending", "resolved", "pending", "rejected", "pending", "reviewing"][i],
        "reviewer_user_id": None if i not in (1, 3, 5, 7) else 1201,
        "decision": None if i not in (3, 5) else ("Conteúdo revisado; ação registrada." if i == 3 else "Denúncia não confirmada."),
    }
    for i, (target, reason) in enumerate(zip(_REPORT_TARGETS, _REPORT_REASONS))
]
DEMO_DASHBOARD = {
    "users_total": 1284,
    "posts_total": 7632,
    "media_total": 486,
    "reports_pending": 4,
    "pending_reports": [
        {"id": row["id"], "target_type": row["target_type"], "reason": row["reason"], "created_at": row["created_at"]}
        for row in DEMO_REPORTS if row["status"] == "pending"
    ][:5],
    "recent_posts": [
        {"id": 9901 + i, "user_id": 1201 + i, "created_at": f"2026-09-26 1{2 + i}:10:00"}
        for i in range(5)
    ],
}


def _json_details(title: str, payload: dict) -> rx.Component:
    return rx.el.details(
        rx.el.summary("Ver resposta JSON de exemplo", class_name="admin-demo-json-summary"),
        rx.el.pre(json.dumps(payload, ensure_ascii=False, indent=2), class_name="admin-report-snapshot admin-demo-json"),
        class_name="admin-report-context admin-demo-json-details",
    )


def _metric(title: str, value: str, note: str) -> rx.Component:
    return rx.el.article(
        rx.el.p(title, class_name="admin-metric-label"),
        rx.el.p(value, class_name="admin-metric-value"),
        rx.el.p(note, class_name="admin-metric-detail"),
        class_name="admin-metric-card",
    )


def _user_card(user: dict) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.p(user["name"], class_name="admin-user-name"),
            rx.el.p("@" + user["username"], class_name="admin-user-username"),
            rx.el.div(
                rx.el.span("ID " + str(user["id"]), class_name="admin-user-id"),
                rx.el.span(user["role"], class_name="admin-user-role"),
                rx.el.span("Suspensa" if user["account_status"] == "disabled" else "Ativa",
                    class_name="admin-status-disabled" if user["account_status"] == "disabled" else "admin-status-active"),
                class_name="admin-user-badges",
            ),
            class_name="admin-user-main",
        ),
        rx.el.p(user["created_at"], class_name="admin-user-username"),
        class_name="admin-user-row",
    )


def _catalog_card(item: dict) -> rx.Component:
    type_labels = {"movie": "Filme", "series": "Série", "book": "Livro", "anime": "Anime"}
    return rx.el.article(
        rx.el.div(rx.icon("clapperboard", size=20), class_name="admin-catalog-cover-empty"),
        rx.el.div(
            rx.el.p(item["title"], class_name="admin-user-name"),
            rx.el.p(type_labels[item["media_type"]] + " · " + item["external_source"] + ":" + item["external_id"],
                class_name="admin-user-username"),
            rx.el.p(item["description"], class_name="admin-catalog-description"),
            class_name="admin-catalog-copy",
        ),
        rx.el.span(str(item["year"]), class_name="admin-user-role"),
        class_name="admin-catalog-row",
    )


def _report_card(report: dict) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.p(f"Report #{report['id']} · {report['created_at']}", class_name="admin-user-name"),
                rx.el.p(f"Alvo: {report['target_type']} #{report['target_id']} · Denunciante #{report['reporter_user_id']}",
                    class_name="admin-user-username"),
                class_name="admin-report-header-copy",
            ),
            rx.el.span(report["status"], class_name="admin-user-role"),
            class_name="admin-report-heading",
        ),
        rx.el.div(
            rx.el.p("Motivo: " + report["reason"], class_name="admin-report-reason"),
            rx.el.p(report["description"], class_name="admin-report-description"),
            rx.el.details(
                rx.el.summary("Contexto salvo no envio do report"),
                rx.el.pre(json.dumps(report["target_snapshot"], ensure_ascii=False, indent=2), class_name="admin-report-snapshot"),
                class_name="admin-report-context",
            ),
            class_name="admin-report-copy",
        ),
        rx.el.p("Amostra somente para leitura; nenhuma decisão será enviada.", class_name="admin-page-description"),
        class_name="admin-report-card",
    )


def admin_demo_page() -> rx.Component:
    users_payload = {"items": DEMO_USERS, "total": 1284, "page": 1, "next_page": 2, "per_page": 25}
    catalog_payload = {"items": DEMO_CATALOG, "total": 486, "page": 1, "next_page": 2, "per_page": 25}
    reports_payload = {"items": DEMO_REPORTS, "total": 8, "page": 1, "next_page": 0, "per_page": 25}
    return rx.el.div(
        rx.el.header(
            rx.el.a(_logo_icon(), rx.el.span("code", rx.el.span("boxd", class_name="brand-yellow")),
                href="/", class_name="brand admin-dashboard-brand", aria_label="Codeboxd — início"),
            rx.el.div(
                rx.el.span("AMOSTRA LOCAL · DADOS FICTÍCIOS", class_name="admin-header-label"),
                rx.el.a("Login administrativo", href="/admin/login", class_name="admin-activity-link"),
                class_name="admin-header-actions",
            ),
            class_name="admin-dashboard-header",
        ),
        rx.el.main(
            rx.el.section(
                rx.el.div(
                    rx.el.p("DEMONSTRAÇÃO DO PAINEL", class_name="admin-page-eyebrow"),
                    rx.el.h1("Prévia com massa de dados", class_name="admin-page-title"),
                    rx.el.p("Estes registros são sintéticos e mostram os formatos esperados das respostas administrativas. Nenhuma ação altera o Xano.",
                        class_name="admin-page-description"),
                    class_name="admin-demo-heading",
                ),
                rx.el.div(
                    _metric("Usuários", "1.284", "25 itens nesta página"),
                    _metric("Publicações", "7.632", "Indicador agregado"),
                    _metric("Obras no catálogo", "486", "25 itens nesta página"),
                    _metric("Reports pendentes", "4", "4 de 8 reports na amostra"),
                    class_name="admin-metrics-grid",
                ),
                rx.el.section(
                    rx.el.div(
                        rx.el.div(rx.el.h2("Usuários", class_name="admin-section-title"),
                            rx.el.p("Página 1 de 52 · 25 resultados · campos seguros da resposta.", class_name="admin-section-description")),
                        class_name="admin-section-heading",
                    ),
                    rx.el.div(*[_user_card(row) for row in DEMO_USERS], class_name="admin-users-list"),
                    _json_details("users", users_payload),
                    class_name="admin-activity-card admin-demo-section",
                ),
                rx.el.section(
                    rx.el.div(
                        rx.el.div(rx.el.h2("Catálogo", class_name="admin-section-title"),
                            rx.el.p("Filmes, séries, livros e animes · Página 1 de 20 · identidade externa preservada.", class_name="admin-section-description")),
                        class_name="admin-section-heading",
                    ),
                    rx.el.div(*[_catalog_card(row) for row in DEMO_CATALOG], class_name="admin-catalog-list"),
                    _json_details("catalog", catalog_payload),
                    class_name="admin-activity-card admin-demo-section",
                ),
                rx.el.section(
                    rx.el.div(
                        rx.el.div(rx.el.h2("Reports", class_name="admin-section-title"),
                            rx.el.p("Amostra com os quatro estados, cinco tipos de alvo e snapshots contextuais.", class_name="admin-section-description")),
                        class_name="admin-section-heading",
                    ),
                    rx.el.div(*[_report_card(row) for row in DEMO_REPORTS], class_name="admin-reports-list"),
                    _json_details("reports", reports_payload),
                    class_name="admin-activity-card admin-demo-section",
                ),
                rx.el.section(
                    rx.el.div(rx.el.h2("Resposta do dashboard", class_name="admin-section-title"),
                        rx.el.p("Indicadores, reports pendentes e atividade recente.", class_name="admin-section-description"),
                        class_name="admin-section-heading"),
                    _json_details("dashboard", DEMO_DASHBOARD),
                    class_name="admin-activity-card admin-demo-section",
                ),
                class_name="admin-demo-content",
            ),
            class_name="admin-demo-main",
        ),
        class_name="admin-dashboard-page admin-demo-page",
    )
