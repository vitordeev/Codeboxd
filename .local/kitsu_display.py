from pathlib import Path
p=Path('Codeboxd_main/state/social.py'); s=p.read_text(encoding='utf8')
s=s.replace("details=' · '.join(f'{k}: {v}' for k,v in details.items()) if isinstance(details,dict) else '').items()}", "details=' · '.join(f'{k}: {v}' for k,v in details.items()\n            if k not in {'Kitsu ID', 'MyAnimeList ID', 'YouTube ID'}) if isinstance(details,dict) else '').items()}")
p.write_text(s,encoding='utf8')
p=Path('tests/test_kitsu.py'); s=p.read_text(encoding='utf8'); s+='''
    def test_provider_identifiers_are_not_shown_in_media_facts(self):
        from Codeboxd_main.state.social import present_media
        item=catalog.media('kitsu','anime','11','Naruto',details={
            'Kitsu ID':'11','MyAnimeList ID':'20','YouTube ID':'abcDEF_123','Fonte':'Kitsu','Episódios':'220'})
        facts=present_media(item)['details']
        self.assertIn('Fonte: Kitsu',facts)
        self.assertNotIn(' ID:',facts)
        self.assertIn('Episódios: 220',facts)
''';p.write_text(s,encoding='utf8')
p=Path('docs/KITSU.md');p.write_text(p.read_text(encoding='utf-8-sig').replace('83 testes','84 testes'),encoding='utf8')
