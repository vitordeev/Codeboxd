from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch
import unittest
import reflex as rx
from pathlib import Path

from Codeboxd_main.state.admin import AdminState


ROOT = Path(__file__).resolve().parents[1]
XANO = ROOT / "xano" / "api" / "codeboxd"


def source_text(path):
    return path.read_bytes().decode("utf-8", errors="replace")


class CatalogPaginationTests(IsolatedAsyncioTestCase):
    def setUp(self):
        path = AdminState.get_full_name().split(".")
        self.state = rx.State(_reflex_internal_init=True).get_substate(path)
        self.state.session_token = "admin-token"
        self.state.catalog_type = "series"

    async def test_catalog_returns_existing_counts_with_35_per_page(self):
        for kind in ("movie", "series", "anime", "book"):
            for count in (5, 35, 0):
                self.state.catalog_type = kind
                with self.subTest(kind=kind, count=count), patch(
                        "Codeboxd_main.state.admin.request", new=AsyncMock(return_value={
                            "items": [{"id": i, "identity_key": f"{kind}:{i}", "title": str(i)}
                                      for i in range(count)],
                            "total": count, "page": 1, "next_page": 2 if count == 35 else 0,
                        })) as request, patch(
                        "Codeboxd_main.state.admin.catalog.search_one", new=AsyncMock(return_value=[])):
                    await self.state._fetch_catalog()

                self.assertEqual(len(self.state.catalog_items), count)
                self.assertEqual(self.state.catalog_total, count)
                self.assertEqual(request.await_args.kwargs["params"]["per_page"], 35)

    async def test_external_results_fill_first_page_without_writes_and_skip_saved_identities(self):
        for kind, source in (("series", "tmdb"), ("anime", "kitsu"), ("book", "openlibrary")):
            self.state.catalog_type = kind
            self.state.catalog_query = "Dune"
            saved = {
                "id": "1", "identity_key": f"{source}:{kind}:saved", "external_source": source,
                "external_id": "saved", "media_type": kind, "title": "Saved",
                "description": "", "cover_url": "", "year": "2020",
            }
            candidates = [{
                "identity_key": f"{source}:{kind}:{identifier}", "external_source": source,
                "external_id": identifier, "media_type": kind, "title": f"External {identifier}",
                "description": "Provider result", "cover_url": "https://example.test/cover.jpg",
                "year": 2021,
            } for identifier in ("saved", "one")]
            with self.subTest(kind=kind), patch(
                    "Codeboxd_main.state.admin.request", new=AsyncMock(return_value={
                        "items": [saved], "total": 1, "page": 1, "next_page": 0,
                    })) as request, patch(
                    "Codeboxd_main.state.admin.catalog.search_one", new=AsyncMock(
                        side_effect=[candidates, []])) as search:
                await self.state._fetch_catalog()

            self.assertEqual(len(self.state.catalog_items), 2)
            self.assertEqual(self.state.catalog_total, 1)
            self.assertEqual(sum(item["id"] == "" for item in self.state.catalog_items), 1)
            self.assertEqual(self.state.catalog_items[-1]["id"], "")
            self.assertEqual(self.state.catalog_items[-1]["title"], "External one")
            self.assertEqual(search.await_args_list[0].args, ("Dune", kind, 1))
            self.assertEqual(request.await_count, 1)
            self.assertEqual(request.await_args.args[0], "GET")

    async def test_provider_failure_keeps_results_received_and_persisted_items(self):
        candidate = {
            "identity_key": "kitsu:anime:external", "external_source": "kitsu",
            "external_id": "external", "media_type": "anime", "title": "External anime",
        }
        with patch("Codeboxd_main.state.admin.request", new=AsyncMock(return_value={
                "items": [], "total": 0, "page": 1, "next_page": 0,
            })), patch("Codeboxd_main.state.admin.catalog.search_one", new=AsyncMock(
                side_effect=[[candidate], RuntimeError("provider unavailable")])):
            self.state.catalog_type = "anime"
            await self.state._fetch_catalog()

        self.assertEqual(sum(item["id"] == "" for item in self.state.catalog_items), 1)
        self.assertEqual(self.state.catalog_items[0]["title"], "External anime")
        self.assertIn("fonte externa falhou", self.state.catalog_external_notice)

    async def test_combined_first_page_is_capped_at_35(self):
        saved = [{
            "id": str(index), "identity_key": f"tmdb:series:saved-{index}",
            "external_source": "tmdb", "external_id": f"saved-{index}",
            "media_type": "series", "title": f"Saved {index}",
        } for index in range(5)]
        candidates = [{
            "identity_key": f"tmdb:series:external-{index}", "external_source": "tmdb",
            "external_id": f"external-{index}", "media_type": "series",
            "title": f"External {index}",
        } for index in range(40)]
        self.state.catalog_type = "series"
        with patch("Codeboxd_main.state.admin.request", new=AsyncMock(return_value={
                "items": saved, "total": 5, "page": 1, "next_page": 2,
            })) as request, patch(
                "Codeboxd_main.state.admin.catalog.search_one", new=AsyncMock(
                    return_value=candidates)) as search:
            await self.state._fetch_catalog()

        self.assertEqual(len(self.state.catalog_items), 35)
        self.assertEqual(sum(item["id"] == "" for item in self.state.catalog_items), 30)
        self.assertEqual(search.await_count, 1)
        self.assertEqual(request.await_count, 1)

class ReportTargetRemovalTests(IsolatedAsyncioTestCase):
    def setUp(self):
        path = AdminState.get_full_name().split(".")
        self.state = rx.State(_reflex_internal_init=True).get_substate(path)
        self.state.session_token = "admin-token"
        self.state.reports = [{"id": "41", "target_type": "post", "target_id": "12", "status": "pending"}]

    async def test_confirmed_removal_sends_reason_and_refreshes_reports(self):
        self.state.open_report_target_removal("41")
        self.state.set_report_removal_decision("Violates content policy")
        with patch("Codeboxd_main.state.session.request", new=AsyncMock(
                return_value={"id": 1, "role": "admin"})), \
                patch("Codeboxd_main.state.admin.request", new=AsyncMock(side_effect=[
                    {"success": True}, {"items": [], "total": 0, "page": 1, "next_page": 0},
                ])) as request:
            async for _ in self.state.confirm_report_target_removal():
                pass

        self.assertEqual(request.await_args_list[0].args,
            ("POST", "/admin/reports/41/remove-target"))
        self.assertEqual(request.await_args_list[0].kwargs["group"], "social")
        self.assertEqual(request.await_args_list[0].kwargs["token"], "admin-token")
        self.assertEqual(request.await_args_list[0].kwargs["data"], {
            "decision": "Violates content policy",
        })
        self.assertEqual(request.await_args_list[1].args[:2], ("GET", "/admin/reports"))
        self.assertEqual(self.state.report_removal_id, "")
        self.assertIn("Publicacao removida", self.state.reports_notice)

    async def test_comment_and_review_reports_open_the_matching_removal(self):
        for target_type in ("media", "comment", "review"):
            self.state.reports[0].update(target_type=target_type, status="pending")
            self.state.open_report_target_removal("41")

            self.assertEqual(self.state.report_removal_id, "41")
            self.assertEqual(self.state.report_removal_type, target_type)
            self.state.close_report_target_removal()

    async def test_message_and_profile_reports_cannot_open_removal(self):
        for target_type in ("message", "profile"):
            self.state.reports[0].update(target_type=target_type, status="pending")
            self.state.open_report_target_removal("41")

            self.assertEqual(self.state.report_removal_id, "")
            self.assertEqual(self.state.report_removal_type, "")

    async def test_finalized_report_cannot_open_removal_again(self):
        self.state.reports[0]["status"] = "resolved"
        self.state.open_report_target_removal("41")

        self.assertEqual(self.state.report_removal_id, "")
        self.assertEqual(self.state.report_removal_type, "")

    async def test_empty_reason_does_not_send_a_write(self):
        self.state.open_report_target_removal("41")
        async for _ in self.state.confirm_report_target_removal():
            pass

        self.assertEqual(self.state.report_removal_id, "41")
        self.assertIn("reason are required", self.state.reports_error)


class ReportRemovalContractTests(unittest.TestCase):
    def test_xano_removal_is_admin_only_audited_and_preserves_report(self):
        source = (XANO / "admin_reports_id_remove_target_POST.xs").read_text(encoding="utf-8")

        self.assertIn('auth = "user"', source)
        self.assertIn('"Security/require_current_session"', source)
        self.assertIn('$locked_actor.role == "admin"', source)
        self.assertIn('($report.status == "pending" || $report.status == "reviewing")', source)
        for target_type in ("post", "media", "comment", "review"):
            self.assertIn(f'$report.target_type == "{target_type}"', source)
        self.assertIn('status: "resolved"', source)
        self.assertIn('action: "admin_report_target_removed"', source)
        self.assertIn('field_name = "id"\n          field_value = $input.id\n          data = {\n            status:', source)
        self.assertIn("db.del comment", source)
        self.assertIn("db.del post_like", source)
        self.assertIn("db.edit media", source)
        self.assertNotIn("db.del media", source)
        self.assertNotIn("db.del report", source)
        self.assertIn('db.edit user_media_interaction', source)
        self.assertIn('data = {rating: null, review: null, spoiler: false}', source)
        self.assertIn('if ($report.target_type == "comment")', source)
        self.assertIn('field_value = $target_id\n                    }', source)
        self.assertGreaterEqual(source.count("lock = true"), 3)

    def test_review_reports_validate_owner_and_capture_snapshot(self):
        report_create = source_text(XANO / "reports_POST.xs")
        report_table = source_text(ROOT / "xano" / "table" / "report.xs")
        admin_page = source_text(ROOT / "Codeboxd_main" / "pages" / "admin.py")
        social_page = source_text(ROOT / "Codeboxd_main" / "pages" / "social.py")

        self.assertIn('"review"', report_create)
        self.assertIn('$target.user_id != $auth.id', report_create)
        self.assertIn('rating: $target.rating, review: $target.review', report_create)
        self.assertIn('"review"', report_table)
        self.assertIn("S.open_report('review'", social_page)
        self.assertIn('value="review"', admin_page)

    def test_catalog_external_results_have_no_status_badge_or_duplicate_top_tabs(self):
        admin_page = source_text(ROOT / "Codeboxd_main" / "pages" / "admin.py")
        self.assertNotIn("Externo", admin_page)
        self.assertNotIn("admin-catalog-tabs", admin_page)

    def test_hidden_media_is_excluded_and_rejected_for_new_references(self):
        media_list = (XANO / "media_GET.xs").read_text(encoding="utf-8")
        media_detail = (XANO / "media_id_GET.xs").read_text(encoding="utf-8")
        interaction = (XANO / "interactions_PUT.xs").read_text(encoding="utf-8")
        list_add = (XANO / "lists_id_items_POST.xs").read_text(encoding="utf-8")
        post_create = (XANO / "posts_POST.xs").read_text(encoding="utf-8")
        post_update = (XANO / "posts_id_PUT.xs").read_text(encoding="utf-8")
        list_status = (ROOT / "xano" / "function" / "Lists" / "set_media_list_status.xs").read_text(encoding="utf-8")

        self.assertIn("moderation_hidden != true", media_list)
        self.assertIn("moderation_hidden != true", media_detail)
        self.assertIn("moderation_hidden != true", interaction)
        self.assertIn("moderation_hidden != true", list_add)
        self.assertIn("moderation_hidden != true", post_create)
        self.assertIn("moderation_hidden != true", post_update)
        self.assertIn("moderation_hidden != true", list_status)


if __name__ == "__main__":
    unittest.main()
