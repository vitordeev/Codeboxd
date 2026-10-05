import time
import urllib.request
for attempt in range(60):
    try:
        with urllib.request.urlopen('http://localhost:3014/',timeout=2) as response:
            if response.status == 200: break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit('Preview did not start')
exec(compile(open('.local/check_home_catalog.py',encoding='utf-8-sig').read(),'.local/check_home_catalog.py','exec'))
