from pathlib import Path
p=Path('Codeboxd_main/services/catalog.py'); s=p.read_text(encoding='utf8')
s=s.replace("    if not query.strip(): return items\n    scored = [(title_score(query, item), item) for item in items]\n    return [item for score, item in sorted(scored, key=lambda pair: pair[0], reverse=True) if score > 0]",'''    scored = [(title_score(query, item), item) for item in items]
    result, seen_anime = [], set()
    for score, item in sorted(scored, key=lambda pair: pair[0], reverse=True):
        if score <= 0: continue
        mal_id = ''
        if item.get('media_type') == 'anime':
            if item.get('external_source') == 'jikan': mal_id = str(item.get('external_id') or '')
            elif item.get('external_source') == 'kitsu': mal_id = str((item.get('details') or {}).get('MyAnimeList ID') or '')
        if mal_id and mal_id in seen_anime: continue
        if mal_id: seen_anime.add(mal_id)
        result.append(item)
    return result''')
s=s.replace("try: delay=min(5,max(0.5,float(retry_after)))", "try: delay=max(0.5,float(retry_after))")
s=s.replace("except ValueError: delay=0.5*(2**attempt)\n                    await asyncio.sleep(delay)","except ValueError: delay=0.5*(2**attempt)\n                    if delay > 5: raise  # Do not retry before the provider permits it.\n                    await asyncio.sleep(delay)")
p.write_text(s,encoding='utf8')
p=Path('tests/test_kitsu.py'); s=p.read_text(encoding='utf-8-sig')
s+='''
    def test_search_deduplicates_verified_legacy_identity(self):
        new=catalog.media('kitsu','anime','11','Naruto',details={'MyAnimeList ID':'20'})
        old=catalog.media('jikan','anime','20','Naruto')
        distinct=catalog.media('jikan','anime','11','Naruto Special')
        self.assertEqual(catalog.relevant_results('Naruto',[new,old,distinct]),[new,distinct])

    async def test_long_rate_limit_does_not_retry_too_early(self):
        client=AsyncMock()
        client.get.return_value=httpx.Response(429,headers={'Retry-After':'60'},
            request=httpx.Request('GET',catalog.KITSU_URL+'/anime'))
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch.object(catalog.httpx,'AsyncClient',return_value=context), patch.object(catalog.asyncio,'sleep',new=AsyncMock()) as sleep:
            with self.assertRaises(APIError) as error: await catalog.fetch(catalog.KITSU_URL+'/anime')
        self.assertEqual(error.exception.status,429)
        self.assertEqual(client.get.await_count,1)
        sleep.assert_not_awaited()
'''
p.write_text(s,encoding='utf8')
