"""Account pages for the first implementation milestone."""
import reflex as rx
from ..state.session import SessionState
from .login import _logo_icon


def field(label: str, name: str, kind: str = 'text', **props) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, html_for=name, class_name='block text-sm text-gray-300 mb-2'),
        rx.el.input(id=name, name=name, type=kind, required=True,
                    class_name='form-input-custom w-full h-12 px-4 rounded-xl text-white', **props),
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
