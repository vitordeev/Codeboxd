"""Account pages for the first implementation milestone."""
import reflex as rx
from ..state.session import SessionState
from .login import _logo_icon
from ..password_input import password_input


def field(label: str, name: str, kind: str = 'text', input_id: str | None = None, **props) -> rx.Component:
    identifier = input_id or name
    return rx.el.div(
        rx.el.label(label, html_for=identifier, class_name='block text-sm text-gray-300 mb-2'),
        (password_input(id=identifier, name=name, required=True,
                        class_name='form-input-custom w-full h-12 px-4 rounded-xl text-white', **props)
         if kind == 'password' else
         rx.el.input(id=identifier, name=name, type=kind, required=True,
                     class_name='form-input-custom w-full h-12 px-4 rounded-xl text-white', **props)),
    )


def signup_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.section(
                rx.el.a(_logo_icon(), rx.el.span('code',rx.el.span('boxd',class_name='brand-yellow')),href='/',class_name='brand'),
                rx.el.h1('Suas histórias merecem companhia.',class_name='text-4xl font-bold leading-tight'),
                rx.el.p('Salve o que você quer assistir ou ler, avalie suas descobertas e encontre sua comunidade.',class_name='text-gray-400 leading-relaxed'),
                rx.el.img(src='/mascot.png',alt='Mascote Codeboxd'),class_name='signup-intro'),
            rx.el.section(
            rx.el.h2('Faça parte da comunidade', class_name='text-2xl font-bold mb-2'),
            rx.el.p('Crie sua conta e comece sua coleção.', class_name='text-gray-400 mb-8 text-sm'),
            rx.el.form(
                field('Seu nome', 'name', auto_complete='name', max_length=80),
                field('Nome de usuário', 'username', auto_complete='username',
                      pattern='[a-zA-Z0-9_]{3,30}', min_length=3, max_length=30,
                      title='Use de 3 a 30 letras, números ou sublinhados.'),
                field('E-mail', 'email', 'email', auto_complete='email'),
                field('Senha', 'password', 'password', auto_complete='new-password', min_length=8),
                rx.el.p('Use pelo menos 8 caracteres, incluindo letra e número.', class_name='text-xs text-gray-400'),
                field('Confirme a senha', 'confirm_password', 'password', auto_complete='new-password', min_length=8),
                rx.el.label(rx.el.input(type='checkbox', name='remember'), ' Manter-me conectado', class_name='text-sm'),
                rx.cond(SessionState.error_message != '', rx.el.p(SessionState.error_message, role='alert', class_name='text-red-400')),
                rx.el.button(rx.cond(SessionState.is_loading, 'Criando conta…', 'Criar conta'),
                             type='submit', disabled=SessionState.is_loading,
                             class_name='w-full h-12 rounded-xl bg-[#F5B300] text-black font-semibold'),
                on_submit=SessionState.signup, class_name='space-y-4',
            ),
            rx.el.a('Já tenho conta', href='/login', class_name='block mt-6 text-[#F5B300]'),
            class_name='signup-panel'),
            class_name='signup-layout',
        ),
        class_name='min-h-screen bg-black text-white flex justify-center items-center p-8',
    )


def password_reset_page() -> rx.Component:
    request_form = rx.el.form(
        field('E-mail da conta', 'email', 'email', input_id='reset-request-email',
              auto_complete='email', placeholder='voce@exemplo.com', default_value=SessionState.reset_email),
        rx.el.button(rx.cond(SessionState.is_loading | SessionState.reset_sending, 'Enviando…', 'Receber código'),
            type='submit', disabled=SessionState.is_loading | SessionState.reset_sending, class_name='action-button reset-primary-button'),
        on_submit=SessionState.submit_password_reset, class_name='reset-form')
    confirm_form = rx.el.div(
        rx.el.div(
            rx.el.div(rx.el.span('E-mail da conta', class_name='reset-recipient-label'),
                rx.el.p(SessionState.reset_email, class_name='reset-recipient-email')),
            rx.el.button('Alterar', type='button', on_click=SessionState.change_reset_email,
                disabled=SessionState.is_loading | SessionState.reset_sending, class_name='reset-text-button'),
            class_name='reset-recipient'),
        rx.el.form(
            field('Código do e-mail', 'code', 'text', input_id='reset-code', auto_complete='one-time-code',
                  min_length=6, max_length=6, pattern='[0-9]{6}', input_mode='numeric', placeholder='000000'),
            field('Nova senha', 'password', 'password', auto_complete='new-password', min_length=8, max_length=128),
            rx.el.p('De 8 a 128 caracteres, com letra e número. Use uma senha diferente da atual.', class_name='reset-hint'),
            field('Confirmar senha', 'confirm_password', 'password', auto_complete='new-password', min_length=8, max_length=128),
            rx.el.button(rx.cond(SessionState.is_loading, 'Salvando…', 'Redefinir senha'),
                type='submit', disabled=SessionState.is_loading | SessionState.reset_sending | SessionState.reset_completed,
                class_name='action-button reset-primary-button'),
            on_submit=SessionState.reset_password, class_name='reset-form'),
        rx.el.div(rx.el.span('Não recebeu? '),
            rx.el.button(rx.cond(SessionState.reset_sending, 'Enviando…', 'Reenviar código'),
                type='button', on_click=SessionState.submit_password_reset({'email': SessionState.reset_email}),
                disabled=SessionState.is_loading | SessionState.reset_sending, class_name='reset-text-button'),
            class_name='reset-resend'))
    return rx.el.main(
        rx.el.header(
            rx.el.a(_logo_icon(), rx.el.span('code', rx.el.span('boxd', class_name='brand-yellow')),
                href='/', class_name='brand', aria_label='Codeboxd — descoberta'),
            rx.el.a('← Voltar', href='/login', class_name='quiet-button reset-discovery-link'),
            class_name='reset-header'),
        rx.el.div(rx.el.section(
            rx.cond(SessionState.reset_completed,
                rx.el.div(
                    rx.el.div(rx.icon('check', size=26), class_name='reset-symbol'),
                    rx.el.h1('Tudo certo.', class_name='reset-title'),
                    rx.el.p('Sua senha foi atualizada. Entre para continuar suas histórias.', class_name='reset-description'),
                    rx.el.a('Entrar na minha conta', href='/login', class_name='action-button reset-primary-button'),
                    rx.el.button('Precisa redefinir a senha novamente?', type='button',
                        on_click=SessionState.start_new_password_reset, class_name='reset-text-button'),
                    role='status', class_name='reset-complete'),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(rx.cond(SessionState.reset_code_requested, '02', '01'), class_name='reset-progress-current'),
                        rx.el.span(' / 02', class_name='reset-progress-total'),
                        class_name='reset-progress', aria_label=rx.cond(SessionState.reset_code_requested, 'Etapa 2 de 2', 'Etapa 1 de 2')),
                    rx.el.div(
                        rx.el.h1(rx.cond(SessionState.reset_code_requested, 'Confira seu e-mail', 'Esqueceu a senha?'), class_name='reset-title'),
                        rx.el.p(rx.cond(SessionState.reset_code_requested,
                            'Use o código de 6 dígitos e escolha sua nova senha.',
                            'Acontece. Informe seu e-mail para recuperar o acesso.'), class_name='reset-description'),
                        class_name='reset-intro'),
                    rx.cond(SessionState.reset_code_requested, confirm_form, request_form),
                    rx.cond(SessionState.reset_message != '',
                        rx.el.p(SessionState.reset_message, role='status',
                            class_name=rx.cond(SessionState.reset_success,
                                'reset-message reset-message-success', 'reset-message reset-message-error'))),
                    rx.el.a('Voltar para entrar', href='/login', class_name='reset-login-link'))),
            class_name='reset-card'), class_name='reset-layout'),
        class_name='password-reset-page')


def account_page() -> rx.Component:
    return rx.center(
        rx.cond(
            SessionState.is_authenticated,
            rx.vstack(
                rx.heading('Bem-vindo ao CodeBoxd'),
                rx.text(SessionState.user_name),
                rx.text('Sua conta está conectada. As páginas da comunidade estão em desenvolvimento.'),
                rx.cond(SessionState.is_admin, rx.link('Administração', href='/admin')),
                rx.button('Sair', on_click=SessionState.logout),
                spacing='4', max_width='560px', padding='24px',
            ),
            rx.text('Verificando sua sessão…'),
        ), min_height='100vh', background='#0D0D0D', color='#F3F2ED',
    )
