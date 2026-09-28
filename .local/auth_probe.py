import json,os
from pathlib import Path
import httpx
from dotenv import load_dotenv
load_dotenv()
account=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
base=os.environ['XANO_AUTH_URL'].rstrip('/')
social=os.environ['XANO_SOCIAL_URL'].rstrip('/')
with httpx.Client(timeout=httpx.Timeout(10,connect=3)) as client:
 login=client.post(base+'/auth/login',json={'email':account['email'],'password':account['password']})
 print('login',login.status_code,flush=True)
 token=login.json().get('authToken','')
 headers={'Authorization':'Bearer '+token}
 for route,url in [('auth initial',base+'/auth/me'),('media',social+'/media?per_page=20'),('profiles',social+'/profiles'),('feed',social+'/feed?per_page=20'),('posts',social+'/posts?per_page=20'),('auth after',base+'/auth/me')]:
  try:
   response=client.get(url,headers=headers); print(route,response.status_code,flush=True)
  except httpx.HTTPError as exc: print(route,type(exc).__name__,flush=True)