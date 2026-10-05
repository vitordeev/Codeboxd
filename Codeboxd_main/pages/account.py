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


def password_reset_page() -> rx.Component:
    return rx.el.main(
        rx.el.header(
            rx.el.a(_logo_icon(), rx.el.span('code',rx.el.span('boxd',class_name='brand-yellow')),
                    href='/',class_name='brand',aria_label='Codeboxd — descoberta'),
            rx.el.a('← Voltar à descoberta',href='/',class_name='quiet-button reset-discovery-link'),
            class_name='reset-header'),
        rx.el.div(rx.el.section(
            rx.el.div(
                rx.el.span('CONTA CODEBOXD',class_name='reset-eyebrow'),
                rx.el.h1('Redefinir senha',class_name='reset-title'),
                rx.el.p('Recupere o acesso à sua conta em duas etapas.',class_name='reset-description'),
                class_name='reset-intro'),
            rx.el.section(
                rx.el.h2(rx.el.span('1',class_name='reset-step-number'),'Receber código',class_name='reset-step-title'),
                rx.el.p('Enviaremos um código de uso único para o e-mail da sua conta.',class_name='reset-step-copy'),
                rx.el.form(
                    field('E-mail da conta', 'email', 'email', auto_complete='email', placeholder='voce@exemplo.com'),
                    rx.el.button(rx.cond(SessionState.is_loading,'Enviando…','Enviar código por e-mail'),
                        type='submit',disabled=SessionState.is_loading,class_name='action-button reset-primary-button'),
                    on_submit=SessionState.request_password_reset,class_name='reset-form'),
                class_name='reset-step'),
            rx.el.section(
                rx.el.h2(rx.el.span('2',class_name='reset-step-number'),'Criar senha nova',class_name='reset-step-title'),
                rx.el.p('Digite o código recebido e escolha uma senha segura.',class_name='reset-step-copy'),
                rx.el.form(
                    field('E-mail da conta', 'email', 'email', auto_complete='email', placeholder='voce@exemplo.com'),
                    field('Código recebido por e-mail', 'code', 'text', auto_complete='one-time-code',
                          max_length=64, placeholder='Cole o código do e-mail'),
                    field('Nova senha', 'password', 'password', auto_complete='new-password', min_length=8),
                    rx.el.p('Mínimo de 8 caracteres, com pelo menos uma letra e um número.',class_name='reset-hint'),
                    field('Confirme a nova senha', 'confirm_password', 'password',
                          auto_complete='new-password', min_length=8),
                    rx.el.button(rx.cond(SessionState.is_loading,'Salvando…','Salvar nova senha'),
                        type='submit',disabled=SessionState.is_loading,class_name='action-button reset-primary-button'),
                    on_submit=SessionState.reset_password,class_name='reset-form'),
                class_name='reset-step'),
            rx.cond(SessionState.reset_message != '',rx.el.p(SessionState.reset_message,
                role='status',class_name=rx.cond(SessionState.reset_success,
                    'reset-message reset-message-success','reset-message reset-message-error'))),
            rx.el.a('Voltar para entrar',href='/login',class_name='reset-login-link'),
            class_name='reset-card'),class_name='reset-layout'),
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
