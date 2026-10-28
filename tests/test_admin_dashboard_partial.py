import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.admin import AdminState


class AdminDashboardPartialTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        path = AdminState.get_full_name().split(".")
        self.state = rx.State(_reflex_internal_init=True).get_substate(path)
        self.state.session_token = "admin-token"
        self.state.dashboard_updated_at = "stale timestamp"
        self.response = {
            "users_total": 5,
            "posts_total": 8,
            "media_total": 13,
            "reports_pending": 2,
            "recent_posts": [{"id": 9, "user_id": 4, "created_at": "today"}],
            "pending_reports": [{"id": 3, "target_type": "post", "reason": "spam", "created_at": "today"}],
        }

    async def load(self):
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch("Codeboxd_main.state.admin.request", new=AsyncMock()) as request:
            request.return_value = self.response
            async for _ in self.state.load_dashboard():
                pass
        return request

    async def test_bad_metric_does_not_hide_valid_metrics_or_other_sections(self):
        self.response["posts_total"] = True
        self.response["reports_pending"] = 0
        request = await self.load()

        request.assert_awaited_once()
        self.assertEqual(dict(self.state.dashboard_stats), {
            "users_total": "5", "posts_total": "—", "media_total": "13", "reports_pending": "0"
        })
        self.assertIn("posts_total", self.state.dashboard_metric_errors)
        self.assertEqual(self.state.recent_posts[0]["id"], "9")
        self.assertEqual(self.state.pending_reports[0]["id"], "3")
        self.assertTrue(self.state.dashboard_updated_at)
        self.assertNotEqual(self.state.dashboard_updated_at, "stale timestamp")
        self.assertEqual(self.state.dashboard_error, "")

    async def test_all_metric_error_keys_exist_and_are_empty_for_initially_available_state(self):
        self.assertEqual(dict(self.state.dashboard_metric_errors), {
            "users_total": "", "posts_total": "", "media_total": "", "reports_pending": ""
        })

        await self.load()

        self.assertEqual(dict(self.state.dashboard_metric_errors), {
            "users_total": "", "posts_total": "", "media_total": "", "reports_pending": ""
        })

    async def test_float_negative_boolean_and_missing_metrics_are_unavailable(self):
        self.response.update(users_total=1.5, posts_total=-1, media_total=float("nan"))
        del self.response["reports_pending"]
        await self.load()

        self.assertEqual(set(self.state.dashboard_stats.values()), {"—"})
        self.assertEqual(set(self.state.dashboard_metric_errors), {
            "users_total", "posts_total", "media_total", "reports_pending"
        })
        self.assertTrue(self.state.recent_posts)
        self.assertTrue(self.state.pending_reports)

    async def test_activity_sections_fail_independently_and_do_not_show_empty_state(self):
        self.response["recent_posts"] = {"unexpected": "object"}
        await self.load()

        self.assertIn("indisponível", self.state.recent_posts_error)
        self.assertEqual(self.state.pending_reports_error, "")
        self.assertEqual(self.state.recent_posts, [])
        self.assertEqual(self.state.pending_reports[0]["id"], "3")
        self.assertEqual(self.state.dashboard_stats["users_total"], "5")

    async def test_http_error_clears_all_previous_data_and_keeps_http_error(self):
        self.state.dashboard_stats = {"users_total": "10", "posts_total": "20", "media_total": "30", "reports_pending": "4"}
        self.state.recent_posts = [{"id": "old"}]
        self.state.pending_reports = [{"id": "old"}]
        self.state.dashboard_updated_at = "old timestamp"
        with patch(
            "Codeboxd_main.state.session.request",
            new=AsyncMock(return_value={"id": 1, "role": "admin"}),
        ), patch(
            "Codeboxd_main.state.admin.request",
            new=AsyncMock(side_effect=APIError("Service unavailable", 503)),
        ):
            async for _ in self.state.load_dashboard():
                pass

        self.assertEqual(set(self.state.dashboard_stats.values()), {"—"})
        self.assertEqual(self.state.recent_posts, [])
        self.assertEqual(self.state.pending_reports, [])
        self.assertEqual(self.state.dashboard_updated_at, "")
        self.assertEqual(self.state.dashboard_error, "Service unavailable")

    async def test_successful_retry_clears_prior_partial_errors_and_refreshes_data(self):
        self.response["media_total"] = -3
        await self.load()
        self.assertIn("media_total", self.state.dashboard_metric_errors)

        self.response["media_total"] = 21
        await self.load()

        self.assertEqual(dict(self.state.dashboard_metric_errors), {
            "users_total": "", "posts_total": "", "media_total": "", "reports_pending": ""
        })
        self.assertEqual(self.state.dashboard_stats["media_total"], "21")
        self.assertEqual(self.state.recent_posts_error, "")
        self.assertEqual(self.state.pending_reports_error, "")
        self.assertEqual(self.state.dashboard_error, "")


if __name__ == "__main__":
    unittest.main()
