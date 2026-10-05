import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.admin import AdminState


class AdminDashboardTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        path = AdminState.get_full_name().split(".")
        self.state = rx.State(_reflex_internal_init=True).get_substate(path)

    async def collect(self):
        return [event async for event in self.state.load_dashboard()]

    async def test_guest_is_redirected_before_dashboard_request(self):
        with patch("Codeboxd_main.state.session.request", new=AsyncMock()) as auth_request, patch(
            "Codeboxd_main.state.admin.request", new=AsyncMock()
        ) as dashboard_request:
            events = await self.collect()

        auth_request.assert_not_awaited()
        dashboard_request.assert_not_awaited()
        self.assertTrue(events)
        payload = {str(key): str(value) for key, value in events[-1].args}
        self.assertEqual(payload["path"], '"/admin/login"')

    async def test_member_is_redirected_and_never_requests_admin_data(self):
        self.state.session_token = "member-token"
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 7, "role": "member", "username": "member"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as dashboard_request:
            events = await self.collect()

        dashboard_request.assert_not_awaited()
        self.assertTrue(events)
        payload = {str(key): str(value) for key, value in events[-1].args}
        self.assertEqual(payload["path"], '"/"')

    async def test_admin_loads_real_metrics_and_recent_posts(self):
        self.state.session_token = "admin-token"
        payload = {
            "users_total": 12,
            "posts_total": 31,
            "media_total": 8,
            "reports_pending": 2,
            "pending_reports": [{"id": 3, "target_type": "post", "reason": "spam", "created_at": "2026-09-26"}],
            "recent_posts": [{"id": 9, "user_id": 4, "created_at": "2026-09-26 12:00:00"}],
        }
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin", "username": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock(return_value=payload)) as request:
            await self.collect()

        request.assert_awaited_once_with("GET", "/admin/dashboard", group="social", token="admin-token")
        self.assertEqual(self.state.dashboard_stats, {
            "users_total": "12", "posts_total": "31", "media_total": "8", "reports_pending": "2"
        })
        self.assertEqual(self.state.recent_posts[0]["id"], "9")
        self.assertEqual(self.state.pending_reports[0]["id"], "3")
        self.assertTrue(self.state.dashboard_updated_at)
        self.assertEqual(self.state.dashboard_error, "")

    async def test_unavailable_dashboard_keeps_placeholders_and_shows_error(self):
        self.state.session_token = "admin-token"
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin", "username": "admin"}),
        ), patch(
            "Codeboxd_main.state.admin.request", new=AsyncMock(side_effect=APIError("Service unavailable", 503))
        ):
            await self.collect()

        self.assertEqual(set(self.state.dashboard_stats.values()), {"—"})
        self.assertEqual(self.state.dashboard_error, "Service unavailable")
        self.assertFalse(self.state.dashboard_updated_at)

    async def test_user_search_uses_server_pagination_and_discards_unapproved_fields(self):
        self.state.session_token = "admin-token"
        search_result = {
            "items": [{
                "id": 22,
                "username": "viewer",
                "name": "Viewer Name",
                "role": "member",
                "account_status": "active",
                "created_at": "2026-09-01 00:00:00",
                "email": "private@example.com",
                "password": "must-not-render",
            }],
            "total": 1,
            "page": 1,
            "next_page": 0,
        }
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock(return_value=search_result)) as request:
            async for _ in self.state.search_users({
                "search": "22", "account_status": "active", "role": "member"
            }):
                pass

        request.assert_awaited_once_with(
            "GET", "/admin/users", group="social", token="admin-token",
            params={"search": "22", "page": 1, "per_page": 25,
                    "account_status": "active", "role": "member", "user_id": 22},
        )
        self.assertEqual(self.state.users[0]["username"], "viewer")
        self.assertNotIn("email", self.state.users[0])
        self.assertNotIn("password", self.state.users[0])
        self.assertEqual(self.state.users_total, 1)

    async def test_user_search_rejects_member_before_reading_accounts(self):
        self.state.session_token = "member-token"
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 7, "role": "member"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            async for _ in self.state.search_users({"search": "viewer"}):
                pass

        request.assert_not_awaited()
        self.assertEqual(self.state.users, [])

    def test_user_details_panel_toggles_per_account(self):
        self.state.toggle_user_details("22")
        self.assertEqual(self.state.user_details_id, "22")
        self.state.toggle_user_details("22")
        self.assertEqual(self.state.user_details_id, "")
        self.state.toggle_user_details("23")
        self.assertEqual(self.state.user_details_id, "23")

    async def test_canceling_account_status_dialog_does_not_write(self):
        self.state.open_user_status_dialog("22", "disabled")
        self.state.close_user_status_dialog()
        self.assertEqual(self.state.user_action_id, "")
        with patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            async for _ in self.state.confirm_user_status_change():
                pass
        request.assert_not_awaited()

    async def test_confirmed_account_status_change_uses_target_and_refreshes_users(self):
        self.state.session_token = "admin-token"
        self.state.users_query = "viewer"
        self.state.users_status_filter = ""
        self.state.users_role_filter = ""
        self.state.open_user_status_dialog("22", "disabled")
        self.state.set_user_action_reason("Repeated abuse reports")
        listed = {"items": [], "total": 0, "page": 1, "next_page": 0}
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch(
            "Codeboxd_main.state.admin.request", new=AsyncMock(side_effect=[None, listed])
        ) as request:
            async for _ in self.state.confirm_user_status_change():
                pass

        self.assertEqual(request.await_args_list[0].args, ("PUT", "/admin/users/22/status"))
        self.assertEqual(request.await_args_list[0].kwargs["data"], {
            "account_status": "disabled", "reason": "Repeated abuse reports"
        })
        self.assertNotIn("actor_id", request.await_args_list[0].kwargs["data"])
        self.assertEqual(len(request.await_args_list), 2)
        self.assertEqual(self.state.user_action_id, "")
        self.assertEqual(self.state.users_notice, "Estado da conta atualizado e ação registrada.")

    async def test_catalog_load_filters_by_section_and_uses_server_pagination(self):
        self.state.session_token = "admin-token"
        self.state.catalog_query = "Arrival"
        catalog_result = {
            "items": [{
                "id": 42,
                "identity_key": "tmdb:movie:329865",
                "external_source": "tmdb",
                "external_id": "329865",
                "media_type": "movie",
                "title": "Arrival",
                "description": "A local description",
                "cover_url": "https://images.example/arrival.jpg",
                "year": 2016,
                "details": {"private_provider_data": "not used"},
            }],
            "total": 1,
            "page": 1,
            "next_page": 0,
        }
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock(return_value=catalog_result)) as request:
            async for _ in self.state.load_catalog_movies():
                pass

        request.assert_awaited_once_with(
            "GET", "/admin/catalog", group="social", token="admin-token",
            params={"media_type": "movie", "search": "Arrival", "page": 1, "per_page": 25},
        )
        self.assertEqual(self.state.catalog_items[0]["identity_key"], "tmdb:movie:329865")
        self.assertNotIn("details", self.state.catalog_items[0])
        self.assertEqual(self.state.catalog_total, 1)

    async def test_member_cannot_read_administrative_catalog(self):
        self.state.session_token = "member-token"
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 7, "role": "member"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            async for _ in self.state.load_catalog_books():
                pass

        request.assert_not_awaited()
        self.assertEqual(self.state.catalog_items, [])

    async def test_invalid_catalog_year_preserves_editor_and_does_not_write(self):
        self.state.catalog_edit_id = "42"
        self.state.catalog_edit_title = "Arrival"
        self.state.catalog_edit_year = "2201"
        with patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            async for _ in self.state.save_catalog_edit():
                pass

        request.assert_not_awaited()
        self.assertEqual(self.state.catalog_edit_id, "42")
        self.assertEqual(self.state.catalog_error, "Informe um ano entre 1800 e 2200.")

    async def test_catalog_update_preserves_external_identity_and_refreshes_current_page(self):
        self.state.session_token = "admin-token"
        self.state.catalog_type = "movie"
        self.state.catalog_query = "Arrival"
        self.state.catalog_edit_id = "42"
        self.state.catalog_edit_title = "Arrival updated"
        self.state.catalog_edit_description = "Corrected text"
        self.state.catalog_edit_cover = "https://images.example/new.jpg"
        self.state.catalog_edit_year = "2016"
        empty_page = {"items": [], "total": 0, "page": 1, "next_page": 0}
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock(side_effect=[None, empty_page])) as request:
            async for _ in self.state.save_catalog_edit():
                pass

        self.assertEqual(request.await_args_list[0].args, ("PUT", "/admin/catalog/42"))
        self.assertEqual(request.await_args_list[0].kwargs["data"], {
            "title": "Arrival updated", "description": "Corrected text",
            "cover_url": "https://images.example/new.jpg", "year": 2016,
        })
        self.assertNotIn("identity_key", request.await_args_list[0].kwargs["data"])
        self.assertEqual(len(request.await_args_list), 2)
        self.assertEqual(self.state.catalog_notice, "Obra atualizada.")
        self.assertEqual(self.state.catalog_edit_id, "")

    async def test_catalog_creation_reuses_existing_identity(self):
        self.state.session_token = "admin-token"
        item = {"id": 42, "title": "Arrival", "media_type": "movie", "external_source": "tmdb", "external_id": "329865", "year": 2016}
        with patch("Codeboxd_main.state.session.request", new=AsyncMock(return_value={"id": 1, "role": "admin"})), patch(
            "Codeboxd_main.state.admin.request", new=AsyncMock(return_value={"success": True, "created": False, "item": item})
        ) as request:
            async for _ in self.state.create_catalog_item({"external_source": "tmdb", "external_id": "329865", "title": "Arrival", "year": "2016"}):
                pass
        request.assert_awaited_once()
        self.assertEqual(request.await_args.args[:2], ("POST", "/admin/catalog"))
        self.assertEqual(self.state.catalog_edit_id, "42")
        self.assertIn("já existe", self.state.catalog_notice)

    async def test_catalog_creation_rejects_source_mismatched_to_section(self):
        self.state.catalog_type = "book"
        with patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            async for _ in self.state.create_catalog_item({"external_source": "tmdb", "external_id": "42", "title": "Book"}):
                pass
        request.assert_not_awaited()
        self.assertIn("não corresponde", self.state.catalog_error)

    async def test_reports_use_server_filters_and_sanitize_snapshot_for_display(self):
        self.state.session_token = "admin-token"
        payload = {
            "items": [{
                "id": 5, "created_at": "2026-09-26", "reporter_user_id": 8,
                "target_type": "message", "target_id": "abc", "reason": "spam",
                "description": "Unwanted message", "target_snapshot": {"body": "text", "sender_name": "User"},
                "status": "pending", "reviewer_user_id": None, "decision": None,
                "reviewed_at": None, "auth_token": "must-not-render",
            }],
            "total": 1, "page": 1, "next_page": 0,
        }
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock(return_value=payload)) as request:
            async for _ in self.state.load_reports():
                pass

        request.assert_awaited_once_with(
            "GET", "/admin/reports", group="social", token="admin-token",
            params={"status": "pending", "target_type": "", "reason": "", "page": 1, "per_page": 25},
        )
        self.assertEqual(self.state.reports[0]["target_snapshot"], '{"body": "text", "sender_name": "User"}')
        self.assertNotIn("auth_token", self.state.reports[0])

    async def test_member_cannot_read_reports(self):
        self.state.session_token = "member-token"
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 7, "role": "member"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            async for _ in self.state.load_reports():
                pass

        request.assert_not_awaited()
        self.assertEqual(self.state.reports, [])

    async def test_report_decision_is_explicit_and_does_not_send_actor_identity(self):
        self.state.session_token = "admin-token"
        self.state.report_review_id = "5"
        self.state.report_review_status = "resolved"
        self.state.report_review_decision = "Reviewed and resolved"
        empty_page = {"items": [], "total": 0, "page": 1, "next_page": 0}
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock(side_effect=[None, empty_page])) as request:
            async for _ in self.state.save_report_review():
                pass

        self.assertEqual(request.await_args_list[0].args, ("PUT", "/admin/reports/5"))
        self.assertEqual(request.await_args_list[0].kwargs["data"], {
            "status": "resolved", "decision": "Reviewed and resolved"
        })
        self.assertEqual(len(request.await_args_list), 2)
        self.assertEqual(self.state.reports_notice, "Revisão registrada na auditoria.")
        self.assertEqual(self.state.report_review_id, "")


if __name__ == "__main__":
    unittest.main()
