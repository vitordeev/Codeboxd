from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
XANO = ROOT / "xano" / "api" / "codeboxd"


class AdminReportContractTests(unittest.TestCase):
    def test_dashboard_metrics_point_to_existing_admin_pages(self):
        page = (ROOT / "Codeboxd_main" / "pages" / "admin.py").read_text(encoding="utf-8")
        routes = (ROOT / "Codeboxd_main" / "Codeboxd_main.py").read_text(encoding="utf-8")

        self.assertIn('"Contas cadastradas",\n                        href="/admin/users"', page)
        self.assertIn('"Filmes, s\u00e9ries, livros e animes", href="/admin/catalog/movies"', page)
        self.assertIn('"Aguardando an\u00e1lise",\n                        href="/admin/reports"', page)
        dashboard = page.split("def admin_dashboard_page", 1)[1].split("def _admin_user_row", 1)[0]
        metric_positions = [
            dashboard.index('_metric_card("Usu\u00e1rios"'),
            dashboard.index('_metric_card("Obras no cat\u00e1logo"'),
            dashboard.index('_metric_card("Reports pendentes"'),
            dashboard.index('_metric_card("Publica\u00e7\u00f5es"'),
        ]
        self.assertEqual(metric_positions, sorted(metric_positions))
        self.assertIn('"Hist\u00f3rias compartilhadas",\n                        href="/feed"', dashboard)
        self.assertIn('"/admin/users"', routes)
        self.assertIn('"/admin/catalog/movies"', routes)
        self.assertIn('"/admin/reports"', routes)
        self.assertIn('route="/feed"', routes)

    def test_report_creation_snapshots_each_supported_target_without_mutating_it(self):
        source = (XANO / "reports_POST.xs").read_text(encoding="utf-8")

        self.assertIn('values = ["message", "post", "comment", "profile", "media"]', source)
        self.assertIn("db.add report", source)
        self.assertIn("target_snapshot: $safe_snapshot", source)
        self.assertNotIn("db.del", source)
        self.assertNotIn("db.edit post", source)
        self.assertNotIn("db.edit comment", source)
        self.assertNotIn("db.edit media", source)
        for target_type in ("message", "post", "comment", "profile"):
            with self.subTest(target_type=target_type):
                self.assertIn(f'$input.target_type == "{target_type}"', source)
        # Media is the final validated branch, so it is represented by the fallback.
        self.assertIn("db.get media", source)

    def test_report_review_updates_only_report_and_audit_log(self):
        source = (XANO / "admin_reports_id_PUT.xs").read_text(encoding="utf-8")

        self.assertIn("db.transaction", source)
        self.assertIn("db.edit report", source)
        self.assertIn("db.add event_log", source)
        self.assertIn('action: "admin_report_status_changed"', source)
        self.assertNotIn("db.del", source)
        self.assertNotIn("db.edit post", source)
        self.assertNotIn("db.edit comment", source)
        self.assertNotIn("db.edit media", source)

    def test_admin_identity_contract_is_authenticated_and_minimal(self):
        source = (XANO / "admin_me_GET.xs").read_text(encoding="utf-8")

        self.assertIn('auth = "user"', source)
        self.assertIn('"Security/require_current_session"', source)
        self.assertIn('$actor.account_status == "active" && $actor.role == "admin"', source)
        for field in ("id", "username", "name", "display_name", "avatar_url", "role"):
            with self.subTest(field=field):
                self.assertIn(f"{field}:", source)
        self.assertNotIn("followers", source)
        self.assertNotIn("following", source)


if __name__ == "__main__":
    unittest.main()
