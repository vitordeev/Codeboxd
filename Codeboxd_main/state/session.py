"""Authentication and server-verified user identity."""
import os
import re
import hashlib
import math
import time
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
    reset_completed: bool = False
    reset_email: str = ''
    reset_code_requested: bool = False
    reset_sending: bool = False
    admin_password_visible: bool = False
    _navigation_verified_until: float = 0.0
    _navigation_verified_token: str = ''
    _navigation_verified_user: int = 0
    _session_identity_token: str = ''
    _auth_retry_at: float = 0.0
    _auth_retry_token: str = ''
    _reset_retry_at: float = 0.0
    _reset_retry_key: str = ''

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id > 0

    @rx.var
    def is_admin(self) -> bool:
        return self.user_id > 0 and self.user_role == 'admin'

    def _token(self) -> str:
        return str(self.session_token or self.auth_token)

    def _clear_identity(self):
        self._forget_navigation_validation()
        self._session_identity_token=''
        self.user_id=0; self.user_name=''; self.user_role=''

    def _forget_navigation_validation(self):
        self._navigation_verified_until=0.0
        self._navigation_verified_token=''; self._navigation_verified_user=0

    def _clear_session(self):
        self._auth_retry_at=0.0; self._auth_retry_token=''
        self.auth_token=''; self.session_token=''; self._clear_identity()

    async def _validate_navigation_session(self) -> bool:
        token=self._token()
        fingerprint=hashlib.sha256(token.encode()).hexdigest() if token else ''
        # This is UI identity reuse only. Writes and admin guards use fresh validation.
        if (token and fingerprint==self._navigation_verified_token
                and self.user_id==self._navigation_verified_user and self.user_id>0
                and self.user_role=='member' and time.monotonic()<self._navigation_verified_until):
            return True
        return await self._validate_session()

    async def _validate_session(self) -> bool:
        token=self._token()
        if not token:
            self._clear_identity()
            return False
        fingerprint=hashlib.sha256(token.encode()).hexdigest()
        if self._session_identity_token and fingerprint!=self._session_identity_token:
            self._clear_identity()
        remaining=math.ceil(self._auth_retry_at-time.monotonic()) if fingerprint==self._auth_retry_token else 0
        if remaining>0:
            self._forget_navigation_validation()
            self.user_role=''
            self.error_message=f'Muitas solicitações. Tente novamente em {remaining} segundos.'
            return False
        self._forget_navigation_validation()
        try:
            user=await request('GET','/auth/me',group='auth',token=token)
            if self._token()!=token: return False
            if not isinstance(user,dict) or not isinstance(user.get('id'),int):
                raise APIError('Resposta de autenticação inválida.')
            if user.get('account_status')=='disabled': raise APIError('Conta desativada.',403)
            self.user_id=user['id']; self.user_name=str(user.get('username') or user.get('name') or '')
            self.user_role=str(user.get('role') or 'member')
            self._session_identity_token=fingerprint
            self._navigation_verified_token=fingerprint
            self._navigation_verified_user=self.user_id
            self._navigation_verified_until=time.monotonic()+15
            self._auth_retry_at=0.0; self._auth_retry_token=''
            self.error_message=''
            return True
        except APIError as exc:
            if self._token()!=token: return False
            self.error_message=str(exc)
            if exc.status==429:
                self._auth_retry_token=fingerprint
                self._auth_retry_at=time.monotonic()+max(1,exc.retry_after or 30)
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
    async def submit_password_reset(self, form: dict):
        if self.is_loading or self.reset_sending: return
        self.reset_sending=True
        try:
            # Flush the loading state before waiting for the mail provider.
            yield
            await self.request_password_reset(form)
        finally:
            self.reset_sending=False

    @rx.event
    async def request_password_reset(self, form: dict):
        if self.is_loading: return
        email=str(form.get('email','')).strip().lower()
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            self.reset_message='Informe um e-mail válido.'
            self.reset_success=False
            return
        key=hashlib.sha256(email.encode()).hexdigest()
        remaining=math.ceil(self._reset_retry_at-time.monotonic()) if key==self._reset_retry_key else 0
        if remaining>0:
            self.reset_message=f'Muitas solicitações. Tente novamente em {remaining} segundos.'
            self.reset_success=False
            return
        self.is_loading=True
        self.reset_message=''
        self.reset_completed=False
        try:
            # The backend checks account eligibility before issuing the code.
            await request('GET','/reset/request-reset-link',group='auth',params={'email':email})
            self.reset_message='Se o e-mail estiver cadastrado, você receberá um código de 6 dígitos. Ele expira em 15 minutos.'
            self.reset_success=True
            self.reset_email=email
            self.reset_code_requested=True
        except APIError as exc:
            self.reset_success=False
            if exc.status==404:
                self.reset_message='Não encontramos uma conta ativa com esse e-mail. Confira o endereço ou crie uma conta.'
                self.reset_email=email
                self.reset_code_requested=False
            elif exc.status==400:
                self.reset_message='Não foi possível enviar o código. Confira o e-mail e tente novamente em instantes.'
            else:
                self.reset_message=str(exc)
                self.reset_success=False
                if exc.status==429:
                    self._reset_retry_key=key
                    self._reset_retry_at=time.monotonic()+max(1,exc.retry_after or 30)
        finally:
            if self.reset_success:
                self._reset_retry_key=key
                self._reset_retry_at=time.monotonic()+60
            self.is_loading=False

    @rx.event
    def enter_password_reset_page(self):
        if self.reset_completed:
            self._start_new_password_reset()

    @rx.event
    def start_new_password_reset(self):
        if self.is_loading or self.reset_sending: return
        self._start_new_password_reset()

    def _start_new_password_reset(self):
        self.reset_code_requested=False
        self.reset_completed=False
        self.reset_success=False
        self.reset_message=''

    @rx.event
    def change_reset_email(self):
        if self.is_loading or self.reset_sending: return
        self.reset_code_requested=False
        self.reset_completed=False
        self.reset_success=False
        self.reset_message=''

    @rx.event
    async def resend_reset_code(self):
        if not self.reset_email or self.reset_completed: return
        await self.request_password_reset({'email': self.reset_email})

    @rx.event
    async def reset_password(self, form: dict):
        if self.is_loading or self.reset_sending or self.reset_completed: return
        email=str(self.reset_email or form.get('email','')).strip().lower()
        code=str(form.get('code','')).strip()
        password=str(form.get('password',''))
        confirmation=str(form.get('confirm_password',''))
        self.reset_message=''
        self.reset_success=False
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):
            self.reset_message='Informe o mesmo e-mail usado para solicitar o código.'
            return
        if not re.fullmatch(r'[0-9]{6}',code):
            self.reset_message='Informe o código de 6 dígitos recebido por e-mail.'
            return
        if not 8 <= len(password) <= 128 or not re.search(r'[A-Za-z]',password) or not re.search(r'[0-9]',password):
            self.reset_message='A senha deve ter de 8 a 128 caracteres, incluindo letra e número.'
            return
        if password != confirmation:
            self.reset_message='As senhas não coincidem.'
            return
        self.is_loading=True
        code_accepted=False
        try:
            result=await request('POST','/reset/magic-link-login',group='auth',
                                 data={'email':email,'magic_token':code})
            code_accepted=True
            token=result.get('authToken') if isinstance(result,dict) else None
            if not isinstance(token,str) or not token:
                raise APIError('O serviço retornou uma resposta inválida.')
            await request('POST','/reset/update_password',group='auth',token=token,
                          data={'password':password,'confirm_password':confirmation})
            if self.user_id > 0 and result.get('user_id') == self.user_id:
                self._clear_session()
            self.reset_message='Senha redefinida. Agora você já pode entrar com a nova senha.'
            self.reset_success=True
            self.reset_completed=True
        except APIError as exc:
            if code_accepted:
                if exc.status in (400,422):
                    self.reset_message='A nova senha não foi aceita. Use de 8 a 128 caracteres, com letra e número, e uma senha diferente da atual. Solicite um novo código para tentar novamente.'
                elif exc.status in (401,403,404):
                    self.reset_message='A autorização de recuperação expirou ou já foi usada. Solicite um novo código.'
                else:
                    self.reset_message='Não foi possível confirmar a troca. Tente entrar com a nova senha ou solicite um novo código.'
            else:
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
