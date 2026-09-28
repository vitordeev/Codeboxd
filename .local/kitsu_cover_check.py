from pathlib import Path
p=Path('.local/kitsu_browser.py');s=p.read_text(encoding='utf-8-sig').replace("page.locator('#home-animes').scroll_into_view_if_needed()", "page.locator('#home-animes').scroll_into_view_if_needed()\n    page.wait_for_function(\"Array.from(document.querySelectorAll('#anime_rated img')).some(img => img.complete && img.naturalWidth > 0)\",timeout=30000)\n    print('anime_covers_loaded',page.locator('#anime_rated img').evaluate_all('(items)=>items.filter(i=>i.complete && i.naturalWidth>0).length'),flush=True)")
p.write_text(s,encoding='utf8')
