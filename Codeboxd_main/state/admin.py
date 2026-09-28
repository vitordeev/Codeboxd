"""State for the protected administration dashboard."""
from datetime import datetime
import json
import reflex as rx

from .session import SessionState
from ..services.api import APIError, request


class AdminState(SessionState):
    dashboard_loading: bool = False
    dashboard_error: str = ''
    dashboard_updated_at: str = ''
    dashboard_stats: dict[str, str] = {
        'users_total': '—',
        'posts_total': '—',
        'media_total': '—',
        'reports_pending': '—',
    }
    recent_posts: list[dict[str, str]] = []
    pending_reports: list[dict[str, str]] = []
    users_loading: bool = False
    users_error: str = ''
    users_notice: str = ''
    users_query: str = ''
    users_status_filter: str = ''
    users_role_filter: str = ''
    users_page: int = 1
    users_total: int = 0
    users_next_page: int = 0
    users: list[dict[str, str]] = []
    user_details_id: str = ''
    user_action_id: str = ''
    user_action_status: str = ''
    user_action_reason: str = ''
    user_action_loading: bool = False
    catalog_type: str = 'movie'
    catalog_loading: bool = False
    catalog_error: str = ''
    catalog_notice: str = ''
    catalog_query: str = ''
    catalog_page: int = 1
    catalog_total: int = 0
    catalog_next_page: int = 0
    catalog_items: list[dict[str, str]] = []
    catalog_create_loading: bool = False
    catalog_edit_id: str = ''
    catalog_edit_title: str = ''
    catalog_edit_description: str = ''
    catalog_edit_cover: str = ''
    catalog_edit_year: str = ''
    catalog_edit_loading: bool = False
    reports_loading: bool = False
    reports_error: str = ''
    reports_notice: str = ''
    reports_status_filter: str = 'pending'
    reports_type_filter: str = ''
    reports_reason_filter: str = ''
    reports_page: int = 1
    reports_total: int = 0
    reports_next_page: int = 0
    reports: list[dict[str, str]] = []
    report_review_id: str = ''
    report_review_status: str = ''
    report_review_decision: str = ''
    report_review_loading: bool = False

    async def _require_admin(self, section: str = 'users'):
        if not self._token():
            return rx.redirect('/admin/login')
        if not await self._validate_session():
            if not self._token():
                return rx.redirect('/admin/login')
            message = self.error_message or 'Não foi possível verificar sua sessão. Tente novamente.'
            if section == 'catalog':
                self.catalog_error = message
            elif section == 'reports':
                self.reports_error = message
            else:
                self.users_error = message
            return False
        if not self.is_admin:
            return rx.redirect('/')
        return True

    def _user_params(self) -> dict[str, str | int]:
        query = self.users_query.strip()
        params: dict[str, str | int] = {
            'search': query,
            'page': self.users_page,
            'per_page': 25,
            'account_status': self.users_status_filter,
            'role': self.users_role_filter,
        }
        if query.isdecimal():
            params['user_id'] = int(query)
        return params

    async def _fetch_users(self):
        result = await request('GET', '/admin/users', group='social', token=self._token(), params=self._user_params())
        if not isinstance(result, dict) or not isinstance(result.get('items'), list):
            raise APIError('O serviço retornou usuários em formato inesperado.')
        if any(not isinstance(item, dict) for item in result['items']):
            raise APIError('O serviço retornou usuários em formato inesperado.')
        if not isinstance(result.get('total'), int) or not isinstance(result.get('page'), int):
            raise APIError('O serviço não retornou os dados de paginação dos usuários.')
        self.users = [
            {
                'id': str(item.get('id') or ''),
                'username': str(item.get('username') or ''),
                'name': str(item.get('name') or ''),
                'role': str(item.get('role') or 'member'),
                'account_status': str(item.get('account_status') or 'active'),
                'created_at': str(item.get('created_at') or ''),
            }
            for item in result['items']
        ]
        self.users_total = result['total']
        self.users_page = result['page']
        self.users_next_page = result.get('next_page') or 0

    @rx.event
    async def guard_users_page(self):
        allowed = await self._require_admin()
        if allowed is not True:
            return allowed if allowed is not False else None

    @rx.event
    async def search_users(self, form: dict):
        if self.users_loading:
            return
        self.users_query = str(form.get('search', '')).strip()[:80]
        self.users_status_filter = str(form.get('account_status', '')).strip()
        self.users_role_filter = str(form.get('role', '')).strip()
        self.users_page = 1
        self.users_error = ''
        self.users_notice = ''
        if not self.users_query:
            self.users = []
            self.users_total = 0
            self.users_next_page = 0
            self.users_error = 'Informe um nome, usuário ou identificador para pesquisar.'
            return
        self.users_loading = True
        yield
        try:
            allowed = await self._require_admin()
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await self._fetch_users()
        except APIError as exc:
            self.users_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.users_loading = False

    @rx.event
    def toggle_user_details(self, user_id: str):
        self.user_details_id = '' if self.user_details_id == user_id else user_id

    @rx.event
    async def change_users_page(self, page: int):
        if self.users_loading or page < 1 or page == self.users_page or not self.users_query:
            return
        self.users_page = page
        self.users_error = ''
        self.users_loading = True
        yield
        try:
            allowed = await self._require_admin()
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await self._fetch_users()
        except APIError as exc:
            self.users_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.users_loading = False

    @rx.event
    def open_user_status_dialog(self, user_id: str, status: str):
        if status not in ('active', 'disabled'):
            return
        self.user_action_id = user_id
        self.user_action_status = status
        self.user_action_reason = ''

    @rx.event
    def close_user_status_dialog(self):
        self.user_action_id = ''
        self.user_action_status = ''
        self.user_action_reason = ''

    @rx.event
    def set_user_action_reason(self, value: str):
        self.user_action_reason = value[:500]

    @rx.event
    async def confirm_user_status_change(self):
        if self.user_action_loading or not self.user_action_id or self.user_action_status not in ('active', 'disabled'):
            return
        self.user_action_loading = True
        self.users_error = ''
        self.users_notice = ''
        yield
        try:
            allowed = await self._require_admin()
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await request(
                'PUT', f'/admin/users/{self.user_action_id}/status', group='social', token=self._token(),
                data={'account_status': self.user_action_status, 'reason': self.user_action_reason.strip()},
            )
            self.users_notice = 'Estado da conta atualizado e ação registrada.'
            self.close_user_status_dialog()
            await self._fetch_users()
        except APIError as exc:
            self.users_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.user_action_loading = False

    async def _fetch_catalog(self):
        result = await request(
            'GET', '/admin/catalog', group='social', token=self._token(),
            params={'media_type': self.catalog_type, 'search': self.catalog_query,
                    'page': self.catalog_page, 'per_page': 25},
        )
        if not isinstance(result, dict) or not isinstance(result.get('items'), list):
            raise APIError('O serviço retornou o catálogo em formato inesperado.')
        if any(not isinstance(item, dict) for item in result['items']):
            raise APIError('O serviço retornou o catálogo em formato inesperado.')
        if not isinstance(result.get('total'), int) or not isinstance(result.get('page'), int):
            raise APIError('O serviço não retornou os dados de paginação do catálogo.')
        self.catalog_items = [
            {
                'id': str(item.get('id') or ''),
                'identity_key': str(item.get('identity_key') or ''),
                'external_source': str(item.get('external_source') or ''),
                'external_id': str(item.get('external_id') or ''),
                'media_type': str(item.get('media_type') or ''),
                'title': str(item.get('title') or ''),
                'description': str(item.get('description') or ''),
                'cover_url': str(item.get('cover_url') or ''),
                'year': str(item.get('year') or ''),
            }
            for item in result['items']
        ]
        self.catalog_total = result['total']
        self.catalog_page = result['page']
        self.catalog_next_page = result.get('next_page') or 0

    async def _load_catalog(self, media_type: str):
        if media_type not in ('movie', 'series', 'anime', 'book') or self.catalog_loading:
            return
        self.catalog_type = media_type
        self.catalog_error = ''
        self.catalog_notice = ''
        self.catalog_loading = True
        yield
        try:
            allowed = await self._require_admin('catalog')
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await self._fetch_catalog()
        except APIError as exc:
            self.catalog_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.catalog_loading = False

    @rx.event
    async def load_catalog_movies(self):
        async for event in self._load_catalog('movie'):
            yield event

    @rx.event
    async def load_catalog_series(self):
        async for event in self._load_catalog('series'):
            yield event

    @rx.event
    async def load_catalog_anime(self):
        async for event in self._load_catalog('anime'):
            yield event

    @rx.event
    async def load_catalog_books(self):
        async for event in self._load_catalog('book'):
            yield event

    @rx.event
    async def search_catalog(self, form: dict):
        if self.catalog_loading:
            return
        self.catalog_query = str(form.get('search', '')).strip()[:120]
        self.catalog_page = 1
        async for event in self._load_catalog(self.catalog_type):
            yield event

    @rx.event
    async def change_catalog_page(self, page: int):
        if self.catalog_loading or page < 1 or page == self.catalog_page:
            return
        self.catalog_page = page
        async for event in self._load_catalog(self.catalog_type):
            yield event

    @rx.event
    def open_catalog_editor(self, item: dict):
        self.catalog_edit_id = str(item.get('id') or '')
        self.catalog_edit_title = str(item.get('title') or '')
        self.catalog_edit_description = str(item.get('description') or '')
        self.catalog_edit_cover = str(item.get('cover_url') or '')
        self.catalog_edit_year = str(item.get('year') or '')
        self.catalog_error = ''

    @rx.event
    def close_catalog_editor(self):
        self.catalog_edit_id = ''
        self.catalog_edit_title = ''
        self.catalog_edit_description = ''
        self.catalog_edit_cover = ''
        self.catalog_edit_year = ''

    @rx.event
    def set_catalog_edit_title(self, value: str):
        self.catalog_edit_title = value[:500]

    @rx.event
    def set_catalog_edit_description(self, value: str):
        self.catalog_edit_description = value[:20000]

    @rx.event
    def set_catalog_edit_cover(self, value: str):
        self.catalog_edit_cover = value[:1000]

    @rx.event
    def set_catalog_edit_year(self, value: str):
        self.catalog_edit_year = value[:4]

    @rx.event
    async def save_catalog_edit(self):
        if self.catalog_edit_loading or not self.catalog_edit_id:
            return
        title = self.catalog_edit_title.strip()
        year = self.catalog_edit_year.strip()
        if not title:
            self.catalog_error = 'O título é obrigatório.'
            return
        if year and (not year.isdecimal() or int(year) < 1800 or int(year) > 2200):
            self.catalog_error = 'Informe um ano entre 1800 e 2200.'
            return
        self.catalog_edit_loading = True
        self.catalog_error = ''
        self.catalog_notice = ''
        yield
        try:
            allowed = await self._require_admin('catalog')
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await request(
                'PUT', f'/admin/catalog/{self.catalog_edit_id}', group='social', token=self._token(),
                data={'title': title, 'description': self.catalog_edit_description.strip() or None,
                      'cover_url': self.catalog_edit_cover.strip() or None,
                      'year': int(year) if year else None},
            )
            self.close_catalog_editor()
            self.catalog_notice = 'Obra atualizada.'
            await self._fetch_catalog()
        except APIError as exc:
            self.catalog_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.catalog_edit_loading = False

    @rx.event
    async def create_catalog_item(self, form: dict):
        if self.catalog_create_loading:
            return
        source = str(form.get('external_source', '')).strip().lower()
        external_id = str(form.get('external_id', '')).strip()
        title = str(form.get('title', '')).strip()
        year_value = str(form.get('year', '')).strip()
        if not title or not external_id:
            self.catalog_error = 'Informe o identificador externo e o título.'
            return
        if year_value and (not year_value.isdecimal() or int(year_value) < 1800 or int(year_value) > 2200):
            self.catalog_error = 'Informe um ano entre 1800 e 2200.'
            return
        source_ok = ((self.catalog_type in ('movie', 'series') and source == 'tmdb')
                     or (self.catalog_type == 'book' and source == 'openlibrary')
                     or (self.catalog_type == 'anime' and source in ('jikan', 'kitsu')))
        if not source_ok:
            self.catalog_error = 'A fonte externa não corresponde ao tipo desta seção.'
            return
        self.catalog_create_loading = True
        self.catalog_error = ''
        self.catalog_notice = ''
        yield
        try:
            allowed = await self._require_admin('catalog')
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            result = await request(
                'POST', '/admin/catalog', group='social', token=self._token(),
                data={'external_source': source, 'external_id': external_id,
                      'media_type': self.catalog_type, 'title': title,
                      'description': str(form.get('description', '')).strip() or None,
                      'cover_url': str(form.get('cover_url', '')).strip() or None,
                      'year': int(year_value) if year_value else None},
            )
            if not isinstance(result, dict) or not isinstance(result.get('item'), dict):
                raise APIError('O serviço não retornou a obra cadastrada.')
            item = result['item']
            if result.get('created') is True:
                self.catalog_query = title[:120]
                self.catalog_page = 1
                self.catalog_notice = 'Obra cadastrada no catálogo.'
                await self._fetch_catalog()
            else:
                self.open_catalog_editor(item)
                self.catalog_notice = 'Essa identidade já existe. Abrimos o registro atual para edição.'
        except APIError as exc:
            self.catalog_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.catalog_create_loading = False

    async def _fetch_reports(self):
        result = await request(
            'GET', '/admin/reports', group='social', token=self._token(),
            params={'status': self.reports_status_filter, 'target_type': self.reports_type_filter,
                    'reason': self.reports_reason_filter, 'page': self.reports_page, 'per_page': 25},
        )
        if not isinstance(result, dict) or not isinstance(result.get('items'), list):
            raise APIError('O serviço retornou reports em formato inesperado.')
        if any(not isinstance(item, dict) for item in result['items']):
            raise APIError('O serviço retornou reports em formato inesperado.')
        if not isinstance(result.get('total'), int) or not isinstance(result.get('page'), int):
            raise APIError('O serviço não retornou os dados de paginação dos reports.')
        self.reports = [
            {
                'id': str(item.get('id') or ''),
                'created_at': str(item.get('created_at') or ''),
                'reporter_user_id': str(item.get('reporter_user_id') or ''),
                'target_type': str(item.get('target_type') or ''),
                'target_id': str(item.get('target_id') or ''),
                'reason': str(item.get('reason') or ''),
                'description': str(item.get('description') or ''),
                'target_snapshot': json.dumps(item.get('target_snapshot'), ensure_ascii=False) if item.get('target_snapshot') else '',
                'status': str(item.get('status') or 'pending'),
                'reviewer_user_id': str(item.get('reviewer_user_id') or ''),
                'decision': str(item.get('decision') or ''),
                'reviewed_at': str(item.get('reviewed_at') or ''),
            }
            for item in result['items']
        ]
        self.reports_total = result['total']
        self.reports_page = result['page']
        self.reports_next_page = result.get('next_page') or 0

    async def _load_reports(self):
        if self.reports_loading:
            return
        self.reports_error = ''
        self.reports_notice = ''
        self.reports_loading = True
        yield
        try:
            allowed = await self._require_admin('reports')
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await self._fetch_reports()
        except APIError as exc:
            self.reports_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.reports_loading = False

    @rx.event
    async def load_reports(self):
        async for event in self._load_reports():
            yield event

    @rx.event
    async def search_reports(self, form: dict):
        if self.reports_loading:
            return
        self.reports_status_filter = str(form.get('status', '')).strip()
        self.reports_type_filter = str(form.get('target_type', '')).strip()
        self.reports_reason_filter = str(form.get('reason', '')).strip()
        self.reports_page = 1
        async for event in self._load_reports():
            yield event

    @rx.event
    async def change_reports_page(self, page: int):
        if self.reports_loading or page < 1 or page == self.reports_page:
            return
        self.reports_page = page
        async for event in self._load_reports():
            yield event

    @rx.event
    def open_report_review(self, report_id: str, status: str):
        if status not in ('reviewing', 'resolved', 'rejected'):
            return
        self.report_review_id = report_id
        self.report_review_status = status
        self.report_review_decision = ''
        self.reports_error = ''

    @rx.event
    def close_report_review(self):
        self.report_review_id = ''
        self.report_review_status = ''
        self.report_review_decision = ''

    @rx.event
    def set_report_review_decision(self, value: str):
        self.report_review_decision = value[:2000]

    @rx.event
    async def save_report_review(self):
        if self.report_review_loading or not self.report_review_id:
            return
        decision = self.report_review_decision.strip()
        if not decision:
            self.reports_error = 'Registre uma decisão antes de atualizar o report.'
            return
        self.report_review_loading = True
        self.reports_error = ''
        self.reports_notice = ''
        yield
        try:
            allowed = await self._require_admin('reports')
            if allowed is not True:
                if allowed is not False:
                    yield allowed
                return
            await request(
                'PUT', f'/admin/reports/{self.report_review_id}', group='social', token=self._token(),
                data={'status': self.report_review_status, 'decision': decision},
            )
            self.close_report_review()
            self.reports_notice = 'Revisão registrada na auditoria.'
            await self._fetch_reports()
        except APIError as exc:
            self.reports_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.report_review_loading = False

    @rx.event
    async def load_dashboard(self):
        if self.dashboard_loading:
            return
        self.dashboard_loading = True
        self.dashboard_error = ''
        yield
        try:
            if not self._token():
                yield rx.redirect('/admin/login')
                return
            if not await self._validate_session():
                if not self._token():
                    yield rx.redirect('/admin/login')
                else:
                    self.dashboard_error = self.error_message or 'Não foi possível verificar sua sessão. Tente novamente.'
                return
            if not self.is_admin:
                yield rx.redirect('/')
                return
            result = await request('GET', '/admin/dashboard', group='social', token=self._token())
            if not isinstance(result, dict):
                raise APIError('O serviço retornou dados inesperados para o dashboard.')
            keys = ('users_total', 'posts_total', 'media_total', 'reports_pending')
            if any(not isinstance(result.get(key), (int, float)) for key in keys):
                raise APIError('O serviço não retornou todos os indicadores do dashboard.')
            self.dashboard_stats = {key: str(result[key]) for key in keys}
            recent = result.get('recent_posts', [])
            if not isinstance(recent, list) or any(not isinstance(item, dict) for item in recent):
                raise APIError('O serviço retornou atividade recente em formato inesperado.')
            self.recent_posts = [
                {
                    'id': str(item.get('id') or ''),
                    'user_id': str(item.get('user_id') or ''),
                    'created_at': str(item.get('created_at') or ''),
                }
                for item in recent
            ]
            pending = result.get('pending_reports', [])
            if not isinstance(pending, list) or any(not isinstance(item, dict) for item in pending):
                raise APIError('O serviço retornou reports pendentes em formato inesperado.')
            self.pending_reports = [
                {
                    'id': str(item.get('id') or ''),
                    'target_type': str(item.get('target_type') or ''),
                    'reason': str(item.get('reason') or ''),
                    'created_at': str(item.get('created_at') or ''),
                }
                for item in pending
            ]
            self.dashboard_updated_at = datetime.now().astimezone().strftime('%d/%m/%Y %H:%M')
        except APIError as exc:
            self.dashboard_error = str(exc)
            if exc.status == 401:
                self._clear_session()
                yield rx.redirect('/admin/login')
            elif exc.status == 403:
                yield rx.redirect('/')
        finally:
            self.dashboard_loading = False
