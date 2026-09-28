import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
load_dotenv()

from Codeboxd_main.services import catalog


async def main():
    cases=[('movie','Interestelar'),('series','Breaking Bad'),('anime','Cowboy Bebop'),('book','Pride and Prejudice')]
    outcomes=[]
    for kind,query in cases:
        items,errors=await catalog.search(query,kind)
        if errors or not items:
            outcomes.append((kind,False,'search unavailable'))
            continue
        try:
            detail=await catalog.detail(items[0])
            ok=bool(detail.get('title') and detail.get('external_id') and detail.get('media_type')==kind)
            outcomes.append((kind,ok,'search and detail passed' if ok else 'detail response incomplete'))
        except Exception:
            outcomes.append((kind,False,'detail unavailable'))
    for kind,ok,message in outcomes:
        print(('PASS' if ok else 'FAIL'),kind,message,flush=True)
    if not all(ok for _,ok,_ in outcomes):
        raise SystemExit(1)


asyncio.run(main())
