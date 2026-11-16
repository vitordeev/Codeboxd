import unittest

import reflex as rx

from Codeboxd_main.pages.social import (
    button,
    editor,
    empty_state,
    feedback,
    field,
    list_detail_page,
    shell,
    textarea,
    unified_search_page,
)


def literal(value):
    return getattr(value, '_var_value', value)


def components(root):
    yield root
    for child in getattr(root, 'children', []):
        if hasattr(child, 'children'):
            yield from components(child)


def text_content(root):
    if isinstance(root, str):
        return root
    value = literal(root)
    if isinstance(value, str):
        return value
    return ' '.join(text_content(child) for child in getattr(root, 'children', []))


class SocialUIComponentTests(unittest.TestCase):
    def test_field_and_textarea_connect_visible_labels_to_controls(self):
        field_component = field('Nome público', 'display_name', 'Ana',
                                input_id='profile-name', required=True)
        field_label, field_input = field_component.children
        self.assertEqual(literal(field_label.html_for), 'profile-name')
        self.assertEqual(literal(field_input.id), 'profile-name')
        self.assertEqual(literal(field_input.default_value), 'Ana')
        self.assertTrue(literal(field_input.required))

        text_component = textarea('Bio', 'bio', 'Texto', id='profile-bio')
        text_label, text_input = text_component.children
        self.assertEqual(literal(text_label.html_for), 'profile-bio')
        self.assertEqual(literal(text_input.id), 'profile-bio')
        self.assertEqual(literal(text_input.default_value), 'Texto')

    def test_buttons_preserve_button_default_and_support_form_submit(self):
        normal = button('Abrir')
        submit = button('Salvar', type='submit', disabled=True)
        self.assertEqual(literal(normal.type), 'button')
        self.assertEqual(literal(submit.type), 'submit')
        self.assertTrue(literal(submit.disabled))

    def test_feedback_and_empty_states_have_distinct_live_semantics(self):
        notice = feedback('Salvo')
        error = feedback('Falha', error=True)
        empty = empty_state('Nenhum perfil encontrado.')
        self.assertEqual(literal(notice.role), 'status')
        self.assertEqual(notice.custom_attrs['aria-live'], 'polite')
        self.assertEqual(literal(error.role), 'alert')
        self.assertEqual(error.custom_attrs['aria-live'], 'assertive')
        self.assertEqual(literal(empty.role), 'status')
        self.assertEqual(empty.custom_attrs['aria-live'], 'polite')

    def test_editor_dialog_keeps_title_description_and_named_close(self):
        dialog = editor('Editar perfil', 'Altere os dados do perfil.',
                        rx.el.p('Campos do perfil'))
        content = dialog.children[0]
        self.assertEqual(type(content).__name__, 'DialogContent')
        self.assertEqual(type(content.children[0]).__name__, 'DialogTitle')
        self.assertEqual(type(content.children[1]).__name__, 'DialogDescription')
        close = content.children[-1]
        self.assertEqual(type(close).__name__, 'DialogClose')
        self.assertEqual(close.children[0].custom_attrs['aria-label'], 'Fechar diálogo')

    def test_shell_exposes_primary_routes_and_expandable_account_destinations(self):
        tree = list(components(shell('Página', 'Subtítulo')))
        hrefs = {
            literal(getattr(component, attribute))
            for component in tree
            for attribute in ('href', 'to')
            if hasattr(component, attribute)
        }
        self.assertIn('/', hrefs)
        self.assertIn('/buscar', hrefs)
        self.assertIn('/feed', hrefs)
        self.assertIn('/biblioteca', hrefs)
        self.assertIn('/conta', hrefs)
        self.assertIn('/listas', hrefs)
        self.assertIn('/comunidade', hrefs)
        details = next(component for component in tree if type(component).__name__ == 'Details')
        summary = next(component for component in tree if type(component).__name__ == 'Summary')
        self.assertIn('account-menu-items', details.children[1].class_name)
        self.assertEqual(summary.custom_attrs['aria-label'], 'Abrir menu da conta')
        self.assertFalse(summary.event_triggers)

    def test_unified_search_has_three_scopes_and_pagination_controls(self):
        tree = list(components(unified_search_page()))
        scope_controls = [component for component in tree
                          if 'aria-pressed' in getattr(component, 'custom_attrs', {})]
        self.assertEqual(len(scope_controls), 3)
        identifiers = {literal(component.id) for component in tree
                       if hasattr(component, 'id')}
        self.assertTrue({'unified-search-query', 'search-creator-id', 'search-list-field'} <= identifiers)
        labels = {literal(component.custom_attrs['aria-label']) for component in tree
                  if 'aria-label' in getattr(component, 'custom_attrs', {})}
        self.assertIn('Escopo da busca', labels)
        self.assertIn('Paginação dos resultados', labels)

    def test_list_detail_has_labeled_share_fallback_and_pagination(self):
        tree = list(components(list_detail_page()))
        share_input = next(component for component in tree
                           if literal(getattr(component, 'id', None)) == 'list-share-url')
        share_label = next(component for component in tree
                           if literal(getattr(component, 'html_for', None)) == 'list-share-url')
        self.assertTrue(literal(share_input.read_only))
        self.assertTrue(share_label.children)
        labels = {literal(component.custom_attrs['aria-label']) for component in tree
                  if 'aria-label' in getattr(component, 'custom_attrs', {})}
        self.assertIn('Paginação dos itens da lista', labels)


if __name__ == '__main__':
    unittest.main()
