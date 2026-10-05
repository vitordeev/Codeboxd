import asyncio, json, sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from Codeboxd_main.services import catalog
async def main():
    for query in ('homen aranha','homem aranha'):
        items,errors=await catalog.search(query)
        print(json.dumps({'query':query,'items':[(i['media_type'],i['title']) for i in items],'errors':errors},ensure_ascii=True),flush=True)
asyncio.run(main())
