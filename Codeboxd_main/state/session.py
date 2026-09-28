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
    reset_message: str = ''
    reset_success: bool = False
    admin_password_visible: bool = False

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
        if not await self._validate_session(): return rx.redirect('/admin/login')
        if not self.is_admin: return rx.redirect('/')

    @rx.event
    async def guard_admin_login(self):
        if await self._validate_session():
            if self.is_admin:
                return rx.redirect('/admin')
            self.error_message='Esta conta não tem permissão para acessar a área administrativa.'

    @rx.event
    def toggle_admin_password(self):
        self.admin_password_visible=not self.admin_password_visible

    @rx.event
    async def login(self, form: dict):
        async for event in self._authenticate(form, False): yield event

    @rx.event
    async def admin_login(self, form: dict):
        async for event in self._authenticate(form, False, admin_only=True): yield event

    @rx.event
    async def signup(self, form: dict):
        async for event in self._authenticate(form, True): yield event

    @rx.event
    async def request_password_reset(self, form: dict):
        email=str(form.get('email','')).strip().lower()
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            self.reset_message='Informe um e-mail válido.'
            self.reset_success=False
            return
        self.is_loading=True
        self.reset_message=''
        try:
            # Xano's built-in reset flow sends a one-time code by email.
            await request('GET','/reset/request-reset-link',group='auth',params={'email':email})
            self.reset_message='Se o e-mail estiver cadastrado, você receberá um código de redefinição.'
            self.reset_success=True
        except APIError as exc:
            # Keep the response generic so the page does not reveal registered accounts.
            if exc.status in (400,404):
                self.reset_message='Se o e-mail estiver cadastrado, você receberá um código de redefinição.'
                self.reset_success=True
            else:
                self.reset_message=str(exc)
                self.reset_success=False
        finally:
            self.is_loading=False

    @rx.event
    async def reset_password(self, form: dict):
        email=str(form.get('email','')).strip().lower()
        code=str(form.get('code','')).strip()
        password=str(form.get('password',''))
        confirmation=str(form.get('confirm_password',''))
        self.reset_message=''
        self.reset_success=False
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):
            self.reset_message='Informe o mesmo e-mail usado para solicitar o código.'
            return
        if not code:
            self.reset_message='Informe o código recebido por e-mail.'
            return
        if len(password)<8 or not re.search(r'[A-Za-z]',password) or not re.search(r'\d',password):
            self.reset_message='A senha precisa de 8 caracteres, incluindo letra e número.'
            return
        if password != confirmation:
            self.reset_message='As senhas não coincidem.'
            return
        self.is_loading=True
        try:
            result=await request('POST','/reset/magic-link-login',group='auth',
                                 data={'email':email,'magic_token':code})
            token=result.get('authToken') if isinstance(result,dict) else None
            if not isinstance(token,str) or not token:
                raise APIError('O serviço retornou uma resposta inválida.')
            await request('POST','/reset/update_password',group='auth',token=token,
                          data={'password':password,'confirm_password':confirmation})
            self.reset_message='Senha redefinida. Agora você já pode entrar com a nova senha.'
            self.reset_success=True
        except APIError as exc:
            self.reset_message=('Código inválido ou expirado. Solicite um novo código e tente novamente.'
                                if exc.status in (400,401,403,404,422) else str(exc))
        finally:
            self.is_loading=False

    async def _authenticate(self, form: dict, signup: bool, admin_only: bool = False):
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
                if admin_only and not self.is_admin:
                    self._clear_session()
                    self.error_message='Esta conta não tem permissão para acessar a área administrativa.'
                    return
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
