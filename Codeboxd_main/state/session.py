"""Authentication and server-verified user identity."""
import os
import re
import reflex as rx
from ..services.api import APIError, request


class SessionState(rx.State):
    auth_token: str = rx.Cookie(name='codeboxd_auth', max_age=86400,
        secure=os.getenv('COOKIE_SECURE','false').lower() == 'true', same_site='lax')
    session_token: str = rx.SessionStorage(name='codeboxd_session')
    user_id: int = 0
    user_name: str = ''
    user_role: str = ''
    error_message: str = ''
    is_loading: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id > 0

    @rx.var
    def is_admin(self) -> bool:
        return self.user_id > 0 and self.user_role == 'admin'

    def _token(self) -> str:
        return str(self.session_token or self.auth_token)

    def _clear_identity(self):
        self.user_id=0; self.user_name=''; self.user_role=''

    def _clear_session(self):
        self.auth_token=''; self.session_token=''; self._clear_identity()

    async def _validate_session(self) -> bool:
        if not self._token():
            self._clear_identity()
            return False
        try:
            user=await request('GET','/auth/me',group='auth',token=self._token())
            if not isinstance(user,dict) or not isinstance(user.get('id'),int):
                raise APIError('Resposta de autenticação inválida.')
            if user.get('account_status')=='disabled': raise APIError('Conta desativada.',403)
            self.user_id=user['id']; self.user_name=str(user.get('username') or user.get('name') or '')
            self.user_role=str(user.get('role') or 'member')
            return True
        except APIError as exc:
            self.error_message=str(exc)
            if exc.status in (401,403):
                self._clear_session()
                return False
            # A timeout, rate limit, or provider outage is not proof that the
            # cached identity is invalid. Keep the UI signed in; protected
            # writes still fail closed when their own request is attempted.
            self.user_role=''
            return False

    @rx.event
    async def check_session(self):
        await self._validate_session()

    @rx.event
    async def guard_account(self):
        if not await self._validate_session():
            return rx.redirect('/login')

    @rx.event
    async def guard_admin(self):
        if not await self._validate_session(): return rx.redirect('/login')
        if not self.is_admin: return rx.redirect('/')

    @rx.event
    async def login(self, form: dict):
        async for event in self._authenticate(form, False): yield event

    @rx.event
    async def signup(self, form: dict):
        async for event in self._authenticate(form, True): yield event

    async def _authenticate(self, form: dict, signup: bool):
        if self.is_loading: return
        self.error_message=''
        email=str(form.get('email','')).strip().lower(); password=str(form.get('password',''))
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email) or not password:
            self.error_message='Informe um e-mail válido e a senha.'; return
        payload={'email':email,'password':password}
        if signup:
            # The old published signup endpoint has no profile/username validation.
            # Enable signup only after the social migration has been published.
            if not os.getenv('XANO_SOCIAL_URL', '').strip():
                self.error_message='O cadastro ainda está em preparação. Tente novamente mais tarde.'
                return
            username=str(form.get('username','')).strip().lower(); name=str(form.get('name','')).strip()
            if not re.fullmatch(r'[a-z0-9_]{3,30}',username) or not name:
                self.error_message='Use um nome de usuário de 3 a 30 letras, números ou sublinhados.'; return
            if len(password)<8 or not re.search(r'[A-Za-z]',password) or not re.search(r'\d',password):
                self.error_message='A senha precisa de 8 caracteres, incluindo letra e número.'; return
            if password!=form.get('confirm_password'):
                self.error_message='As senhas não coincidem.'; return
            payload.update(username=username,name=name)
        self.is_loading=True
        yield
        try:
            response=await request('POST','/auth/signup' if signup else '/auth/login',group='auth',data=payload)
            token=response.get('authToken') if isinstance(response,dict) else None
            if not isinstance(token,str) or not token: raise APIError('Resposta de autenticação inválida.')
            self._clear_session()
            if form.get('remember') in ('on','true',True): self.auth_token=token
            else: self.session_token=token
            if await self._validate_session():
                yield rx.redirect('/admin' if self.user_role == 'admin' else '/conta')
        except APIError as exc:
            self.error_message=('E-mail ou senha inválidos.' if not signup and exc.status in (400,401,403)
                else 'E-mail ou nome de usuário indisponível.' if signup and exc.status in (400,403,409) else str(exc))
        finally:
            self.is_loading=False

    @rx.event
    def logout(self):
        self._clear_session()
        return rx.redirect('/login', replace=True)
