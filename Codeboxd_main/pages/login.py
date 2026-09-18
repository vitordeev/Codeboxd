"""Tela de login do painel admin do CodeBoxd.

Convertida do mockup HTML/Tailwind fornecido, mantendo as mesmas classes
Tailwind e a ilustração SVG original dos mascotes. Os campos de e-mail/senha
e o botão de submit são conectados ao AuthState (services/xano_client via auth_post).
"""

import reflex as rx

from ..state.auth_state import AuthState

# ---------------------------------------------------------------------------
# Head components: Tailwind CDN + config + fonte Inter + CSS customizado.
# Importe HEAD_COMPONENTS no Codeboxd_main.py e passe em rx.App(head_components=...).
# ---------------------------------------------------------------------------

TAILWIND_CONFIG_JS = """
tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        brand: {
          yellow: '#F5B300',
          yellowHover: '#e0a400',
          dark: '#030303',
          cardBorder: '#232323',
          muted: '#7E7E7E',
          subtle: '#666666',
          inputBg: '#080808',
          inputBorder: '#1c1c1c',
        }
      }
    }
  }
}
"""

CUSTOM_CSS = """
body {
  background-color: #000000;
  color: #ffffff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.form-input-custom {
  background-color: #060606;
  border: 1px solid #1e1e1e;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.form-input-custom:focus {
  outline: none;
  border-color: #F5B300;
  box-shadow: 0 0 0 1px #F5B300;
}
.custom-checkbox {
  appearance: none;
  -webkit-appearance: none;
  background-color: transparent;
  border: 1.5px solid #666666;
  border-radius: 4px;
  width: 15px;
  height: 15px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}
.custom-checkbox:checked {
  background-color: transparent;
  border-color: #d1d5db;
}
.custom-checkbox:checked::after {
  content: '';
  display: block;
  width: 4px;
  height: 8px;
  border: solid #ffffff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  margin-bottom: 2px;
}
"""

HEAD_COMPONENTS = [
    rx.el.link(rel="stylesheet", href="/codeboxd.css"),
    rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
    rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
    rx.el.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    ),
    rx.el.style(CUSTOM_CSS),
]


# ---------------------------------------------------------------------------
# Ilustração dos mascotes (SVG original, convertido 1:1)
# ---------------------------------------------------------------------------

def _mascots_svg() -> rx.Component:
    return rx.el.svg(
        # Robô da esquerda (segurando tablet)
        rx.el.svg.g(
            rx.el.svg.rect(x="52", y="160", width="10", height="28", rx="5", fill="#4B4836", stroke="#1F1E19", stroke_width="1.5"),
            rx.el.svg.rect(x="68", y="160", width="10", height="28", rx="5", fill="#4B4836", stroke="#1F1E19", stroke_width="1.5"),
            rx.el.svg.ellipse(cx="57", cy="190", rx="14", ry="6", fill="#141414", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.ellipse(cx="73", cy="190", rx="14", ry="6", fill="#141414", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.rect(x="44", y="132", width="42", height="34", rx="10", fill="#141414", stroke="#2a2a2a", stroke_width="1.5"),
            rx.el.svg.path(d="M56 142 L65 156 L74 142", fill="none", stroke="#F5B300", stroke_width="2"),
            rx.el.svg.circle(cx="65", cy="160", r="3.5", fill="#F5B300"),
            rx.el.svg.circle(cx="34", cy="98", r="9", fill="#141414", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.circle(cx="34", cy="98", r="4.5", fill="#F5B300"),
            rx.el.svg.circle(cx="34", cy="92", r="1.5", fill="#141414"),
            rx.el.svg.circle(cx="34", cy="104", r="1.5", fill="#141414"),
            rx.el.svg.rect(x="38", y="70", width="54", height="48", rx="22", fill="#141414", stroke="#F5B300", stroke_width="3"),
            rx.el.svg.rect(x="44", y="77", width="42", height="34", rx="14", fill="#050505"),
            rx.el.svg.ellipse(cx="55", cy="93", rx="4.5", ry="6.5", fill="#F5B300"),
            rx.el.svg.ellipse(cx="75", cy="93", rx="4.5", ry="6.5", fill="#F5B300"),
            rx.el.svg.path(d="M44 140 C34 146 38 160 48 156", fill="none", stroke="#524E3A", stroke_width="7", stroke_linecap="round"),
            rx.el.svg.circle(cx="48", cy="156", r="4", fill="#F5B300"),
            rx.el.svg.path(d="M84 140 C94 146 95 162 82 165", fill="none", stroke="#524E3A", stroke_width="7", stroke_linecap="round"),
            rx.el.svg.g(
                rx.el.svg.rect(x="0", y="0", width="28", height="38", rx="4", fill="#1a1a1a", stroke="#F5B300", stroke_width="1.8"),
                rx.el.svg.rect(x="3", y="3", width="22", height="32", rx="2", fill="#000"),
                rx.el.svg.path(d="M6 14 Q10 10 14 13 T22 9", fill="none", stroke="#F5B300", stroke_width="1.4"),
                rx.el.svg.rect(x="6", y="20", width="3", height="10", fill="#F5B300"),
                rx.el.svg.rect(x="11", y="23", width="3", height="7", fill="#F5B300"),
                rx.el.svg.rect(x="16", y="18", width="3", height="12", fill="#F5B300"),
                rx.el.svg.circle(cx="21", cy="27", r="1.5", fill="#F5B300"),
                transform="translate(70, 134) rotate(12)",
            ),
        ),
        # Robô da direita (acenando)
        rx.el.svg.g(
            rx.el.svg.rect(x="130", y="160", width="9", height="28", rx="4.5", fill="#4B4836", stroke="#1F1E19", stroke_width="1.5"),
            rx.el.svg.rect(x="144", y="160", width="9", height="28", rx="4.5", fill="#4B4836", stroke="#1F1E19", stroke_width="1.5"),
            rx.el.svg.ellipse(cx="134", cy="190", rx="13", ry="5.5", fill="#141414", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.ellipse(cx="149", cy="190", rx="13", ry="5.5", fill="#141414", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.rect(x="124", y="132", width="36", height="32", rx="9", fill="#141414", stroke="#2a2a2a", stroke_width="1.5"),
            rx.el.svg.path(d="M124 142 L160 142", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.path(d="M124 158 L160 158", stroke="#F5B300", stroke_width="2"),
            rx.el.svg.path(d="M125 142 C114 146 106 142 98 140", fill="none", stroke="#524E3A", stroke_width="6", stroke_linecap="round"),
            rx.el.svg.path(d="M98 140 C93 138 90 142 95 145 C90 146 92 150 97 148", fill="none", stroke="#787355", stroke_width="2"),
            rx.el.svg.path(d="M158 142 C165 148 168 158 162 165", fill="none", stroke="#524E3A", stroke_width="6", stroke_linecap="round"),
            rx.el.svg.circle(cx="160", cy="166", r="4.5", fill="#686348"),
            rx.el.svg.circle(cx="170", cy="98", r="8.5", fill="#141414", stroke="#F5B300", stroke_width="2.5"),
            rx.el.svg.circle(cx="170", cy="98", r="4", fill="#F5B300"),
            rx.el.svg.circle(cx="170", cy="93", r="1.3", fill="#141414"),
            rx.el.svg.circle(cx="170", cy="103", r="1.3", fill="#141414"),
            rx.el.svg.rect(x="115", y="74", width="48", height="44", rx="20", fill="#141414", stroke="#F5B300", stroke_width="2.8"),
            rx.el.svg.rect(x="120", y="80", width="38", height="31", rx="12", fill="#050505"),
            rx.el.svg.ellipse(cx="129", cy="95", rx="4", ry="5.5", fill="#F5B300"),
            rx.el.svg.ellipse(cx="147", cy="95", rx="4", ry="5.5", fill="#F5B300"),
        ),
        view_box="0 0 340 220",
        fill="none",
        xmlns="http://www.w3.org/2000/svg",
        class_name="w-full max-w-[340px] h-auto",
    )


def _logo_icon() -> rx.Component:
    return rx.el.svg(
        rx.el.svg.path(d="M22 3L40 13.5V34.5L22 45L4 34.5V13.5L22 3Z", stroke="#F5B300", stroke_width="2.6"),
        rx.el.svg.path(d="M22 3V24M4 13.5L22 24M40 13.5L22 24", stroke="#F5B300", stroke_width="2.6"),
        rx.el.svg.path(d="M9 22.5L12 25L9 27.5", stroke="#F5B300", stroke_width="1.8"),
        rx.el.svg.path(d="M31 22.5L35 25L31 27.5V22.5Z", fill="#F5B300", stroke="#F5B300", stroke_width="1.2"),
        class_name="w-10 h-10 text-[#F5B300] flex-shrink-0",
        fill="none",
        stroke="currentColor",
        stroke_linecap="round",
        stroke_linejoin="round",
        stroke_width="2.5",
        view_box="0 0 44 44",
    )


# ---------------------------------------------------------------------------
# Página de login
# ---------------------------------------------------------------------------

def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.main(
            # ---- Coluna esquerda: marca + ilustração ----
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        _logo_icon(),
                        rx.el.span("codeboxd", class_name="text-2xl font-bold tracking-tight text-[#F5B300] font-sans"),
                        class_name="flex items-center gap-3 mb-12 sm:mb-16",
                    ),
                    rx.el.h1(
                        "Suas histórias.", rx.el.br(),
                        "Sua comunidade.", rx.el.br(),
                        "CodeBoxd.",
                        class_name="text-3xl sm:text-4xl lg:text-[42px] font-bold leading-[1.18] tracking-tight text-white mb-6",
                    ),
                    rx.el.p(
                        "Um lugar para quem ama filmes, séries, animes e livros. "
                        "Descubra, registre e compartilhe suas próximas histórias.",
                        class_name="text-[13px] sm:text-[14px] leading-relaxed text-[#7e7e7e] max-w-[420px] font-normal",
                    ),
                ),
                rx.el.div(_mascots_svg(), class_name="mt-8 pt-4 flex items-end"),
                class_name="flex-1 flex flex-col justify-between max-w-[500px]",
            ),
            # ---- Coluna direita: formulário de login ----
            rx.el.section(
                rx.el.header(
                    rx.el.h2("Entre na sua conta", class_name="text-xl sm:text-2xl font-bold tracking-tight text-white mb-2"),
                    rx.el.p("Bem-vindo de volta ao CodeBoxd", class_name="text-[13px] text-[#787878] font-normal"),
                    class_name="mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("E-mail", class_name="block text-[13px] text-[#7e7e7e] mb-2 font-normal", html_for="email"),
                        rx.el.input(
                            id="email",
                            name="email",
                            type="email",
                            required=True,
                            auto_complete="email",
                            class_name="form-input-custom w-full h-12 px-4 rounded-xl text-white text-sm focus:ring-0",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Senha", class_name="block text-[13px] text-[#7e7e7e] mb-2 font-normal", html_for="password"),
                        rx.el.input(
                            id="password",
                            name="password",
                            type="password",
                            required=True,
                            auto_complete="current-password",
                            class_name="form-input-custom w-full h-12 px-4 rounded-xl text-white text-sm focus:ring-0",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.span("Manter-me conectado"),
                            rx.el.input(type="checkbox", name="remember", default_checked=True, class_name="custom-checkbox"),
                            class_name="flex items-center gap-2.5 cursor-pointer select-none text-[#808080] font-normal hover:text-gray-300",
                        ),
                        rx.el.a("Criar conta", href="/cadastro", class_name="text-[#F5B300] hover:underline font-medium"),
                        class_name="flex items-center justify-between text-xs sm:text-[13px] pt-1",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.p(AuthState.error_message, class_name="text-[13px] text-red-500 pt-1"),
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.el.svg(
                                rx.el.svg.path(d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"),
                                rx.el.svg.polyline(points="10 17 15 12 10 7"),
                                rx.el.svg.line(x1="15", x2="3", y1="12", y2="12"),
                                class_name="w-4 h-4 stroke-[2.5]",
                                fill="none", stroke="currentColor",
                                stroke_linecap="round", stroke_linejoin="round",
                                view_box="0 0 24 24",
                            ),
                            rx.el.span(rx.cond(AuthState.is_loading, "Entrando...", "Entrar")),
                            type="submit",
                            disabled=AuthState.is_loading,
                            class_name="w-full h-12 bg-[#F5B300] hover:bg-[#e0a400] text-black font-semibold text-[14px] rounded-xl flex items-center justify-center gap-2 transition-colors duration-150 active:scale-[0.99] shadow-sm",
                        ),
                        class_name="pt-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Seu próximo filme favorito pode começar com uma boa conversa.",
                                class_name="text-[11px] leading-relaxed text-[#595959]",
                            ),
                            class_name="border border-[#222222] rounded-2xl px-5 py-3.5 bg-[#030303]/60 text-center",
                        ),
                        class_name="pt-6",
                    ),
                    on_submit=AuthState.login,
                    class_name="space-y-5",
                ),
                class_name="flex-1 flex flex-col justify-center max-w-[450px] w-full mt-4 md:mt-0",
            ),
            class_name="w-full max-w-[1100px] min-h-[640px] flex flex-col md:flex-row items-stretch justify-between gap-12 lg:gap-20 py-8 px-4 sm:px-8",
        ),
        class_name="bg-black text-white min-h-screen flex items-center justify-center p-4 sm:p-8 selection:bg-yellow-500 selection:text-black",
    )
