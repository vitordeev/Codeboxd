"""Explicit test entry point, using the existing fail-closed fictional backend."""
from tools.ui_controls_state import ControlsFixture
from tools.ui_foundations_fixture import app
import reflex as rx
from Codeboxd_main.pages.social import button, confirm, feedback, field, textarea, empty_state, shell, editor


def controls_page():
    return shell('Controles de teste', 'Dados fictícios; nenhuma gravação remota.',
        rx.el.form(field('Nome de exibição', 'display_name', 'Pessoa de teste'),
            textarea('Sua crítica', 'review', 'Um rascunho de teste.'),
            rx.el.button('Salvar teste', type='submit', class_name='action-button'),
            rx.cond(ControlsFixture.message != '', feedback(ControlsFixture.message, 'error')),
            class_name='editor-form', on_submit=ControlsFixture.fail),
        button('Abrir edição', ControlsFixture.open_editor, variant='secondary'),
        button(rx.cond(ControlsFixture.working, 'Salvando…', 'Simular carregamento'),
            ControlsFixture.simulate_loading, disabled=ControlsFixture.working),
        empty_state('Nenhuma obra adicionada. Suas obras aparecerão aqui.'),
        feedback('Alteração confirmada nesta demonstração.', 'success'),
        feedback('Parte das informações está indisponível; o conteúdo carregado permanece disponível.'),
        confirm('Excluir rascunho de teste', ControlsFixture.no_operation),
        editor('Editar rascunho', 'As alterações ficam somente nesta fixture.',
            rx.el.div(field('Título', 'title', 'Título de teste'),
                textarea('Descrição', 'description', 'Texto preservado.'), class_name='editor-form'),
            open=ControlsFixture.opened, on_open_change=ControlsFixture.set_opened))


app.add_page(controls_page, route='/ui-controls-fixture')
