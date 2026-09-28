import asyncio
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from Codeboxd_main.services import catalog
async def main():
    for kind,query in [('anime','Cowboy Bebop'),('book','Pride and Prejudice')]:
        items,errors=await catalog.search(query,kind)
        if errors: raise AssertionError(errors)
        assert items
        item=await catalog.detail(items[0])
        assert item['title'] and item['external_id'] and item['media_type']==kind
        print('PASS live provider search and detail:',kind,flush=True)
asyncio.run(main())
