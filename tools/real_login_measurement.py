"""Interactive, local-only login/profile measurement against configured Xano.

The user enters credentials in a temporary Edge window. No screenshots, traces,
cookies, credentials, bodies or raw URLs are saved. Only sanitized metrics are
exported. Run from repository root: python -B -m tools.real_login_measurement
"""
import asyncio
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qsl, urlsplit

import httpx
import psutil
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from tools.performance_probe import safe_endpoint
from tools.isolated_frontend import prepare_frontend
from Codeboxd_main.services.api import retry_after_seconds


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/otimizar-performance-app/validation/login-real-apos-cache-2026-10-20.json'


class VisitCycle:
    """Observe booleans/timestamps only; never retain WebSocket payloads.

    A cycle must see busy=True after arming. Cached DOM or initial hydration
    snapshots with busy=False cannot complete a visit.
    """
    def __init__(self):
        self.arm()
        self.submit_at=None

    def arm(self):
        self.armed_at=time.perf_counter()
        self.started_at=None
        self.primary_at=None
        self.finished_at=None

    def submitted(self): self.submit_at=time.perf_counter()

    def received(self, frame):
        if not isinstance(frame,str) or not frame.startswith('42'): return
        try:
            packet=json.loads(frame[frame.index('['):])
            if not isinstance(packet,list) or len(packet)<2 or packet[0]!='event': return
            update=packet[1]
            if isinstance(update,str): update=json.loads(update)
            for state,delta in update.get('delta',{}).items():
                if not state.endswith('social_state') or not isinstance(delta,dict): continue
                busy=delta.get('busy_rx_state_',delta.get('busy'))
                now=time.perf_counter()
                if busy is True and self.started_at is None:
                    self.started_at=now
                if self.started_at is None: continue
                profile=delta.get('profile_rx_state_',delta.get('profile'))
                if isinstance(profile,dict) and profile.get('username') and self.primary_at is None:
                    self.primary_at=now
                if busy is False:
                    self.finished_at=now
        except (ValueError,TypeError,AttributeError):
            return

    def metrics(self):
        return dict(cycle_started=self.started_at is not None,
                    cycle_finished=self.finished_at is not None,
                    primary_update_ms=round((self.primary_at-self.armed_at)*1000)
                    if self.primary_at is not None else None,
                    cycle_total_ms=round((self.finished_at-self.armed_at)*1000)
                    if self.finished_at is not None else None)


def allowed_request(method, path):
    parsed=urlsplit(path)
    if parsed.scheme or parsed.netloc or parsed.fragment: return False
    if method=='POST':
        return parsed.path=='/auth/auth/login' and not parsed.query
    if method!='GET': return False
    if not re.fullmatch(r'/(auth/auth/me|social/media|social/profiles(?:/[0-9]+)?)',parsed.path):
        return False
    return all(key in ('page','per_page') and value.isdigit()
               for key,value in parse_qsl(parsed.query,keep_blank_values=True))


class Measurement:
    def __init__(self, max_requests=80):
        self.lock=threading.Lock()
        self.started=time.perf_counter()
        self.events=[]
        self.total=0
        self.login_attempts=0
        self.max_requests=max_requests
        self.stop_reason=''
        self.retry_until=0.0

    def reserve(self, method):
        with self.lock:
            if self.stop_reason: return False
            if self.total>=self.max_requests or (method=='POST' and self.login_attempts>=3):
                self.stop_reason='request-budget'
                return False
            self.total+=1
            if method=='POST': self.login_attempts+=1
            return True

    def record(self, method, path, status, start, retry_after=''):
        wait=retry_after_seconds(retry_after) if status==429 else 0
        with self.lock:
            self.events.append(dict(method=method,service='xano',endpoint=safe_endpoint(path),
                status=status,offset_ms=round((start-self.started)*1000,3),
                duration_ms=round((time.perf_counter()-start)*1000,3),retry_after_seconds=wait))
            if status==429:
                self.stop_reason='remote-429'
                self.retry_until=time.monotonic()+wait

    def report(self):
        with self.lock:
            return dict(total_outbound_requests=self.total,stop_reason=self.stop_reason,
                statuses=dict(Counter(str(e['status']) for e in self.events)),
                events=[dict(e) for e in self.events])


def handler_class(measurement, bases, transport=None):
    class Proxy(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def do_POST(self): self.forward()
        def do_GET(self): self.forward()
        def do_PUT(self): self.reply(403,b'{}')
        def do_DELETE(self): self.reply(403,b'{}')
        def do_PATCH(self): self.reply(403,b'{}')

        def reply(self,status,body,wait=0):
            self.send_response(status)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(body)))
            if wait: self.send_header('Retry-After',str(wait))
            self.end_headers()
            try: self.wfile.write(body)
            except (BrokenPipeError,ConnectionResetError): pass

        def forward(self):
            if not allowed_request(self.command,self.path):
                self.reply(403,b'{}')
                return
            if not measurement.reserve(self.command):
                self.reply(429,b'{}',max(1,int(measurement.retry_until-time.monotonic())))
                return
            group,relative=self.path.lstrip('/').split('/',1)
            start=time.perf_counter()
            headers={key:self.headers[key] for key in ('Authorization','Content-Type','Accept')
                     if self.headers.get(key)}
            length=int(self.headers.get('Content-Length','0'))
            if not 0<=length<=65536:
                self.reply(413,b'{}')
                return
            body=self.rfile.read(length) if length else None
            try:
                # No connection pool or retries added to the observed application.
                with httpx.Client(timeout=15,follow_redirects=False,transport=transport) as client:
                    response=client.request(self.command,bases[group].rstrip('/')+'/'+relative,
                                            headers=headers,content=body)
                status=response.status_code
                wait=response.headers.get('Retry-After','')
                measurement.record(self.command,self.path,status,start,wait)
                self.reply(status,response.content,retry_after_seconds(wait) if status==429 else 0)
            except httpx.RequestError:
                measurement.record(self.command,self.path,0,start)
                self.reply(502,b'{}')
    return Proxy


def stop_process_tree(process):
    if process.poll() is not None: return
    parent=psutil.Process(process.pid)
    for child in reversed(parent.children(recursive=True)):
        try: child.terminate()
        except psutil.NoSuchProcess: pass
    process.terminate()
    try: process.wait(timeout=10)
    except subprocess.TimeoutExpired: process.kill()


def normal_app_roots():
    """Identify only this workspace's normal Reflex launcher before the test."""
    matches=[]
    for process in psutil.process_iter(['pid','ppid','cmdline','create_time']):
        try:
            args=process.info['cmdline'] or []
            if (args and Path(args[0]).resolve()==Path(sys.executable).resolve()
                    and '-m' in args and 'reflex' in args and 'run' in args
                    and '--frontend-port' in args and args[args.index('--frontend-port')+1]=='3030'
                    and '--backend-port' in args and args[args.index('--backend-port')+1]=='3030'):
                matches.append(process.info)
        except (psutil.Error,OSError,IndexError): pass
    ids={entry['pid'] for entry in matches}
    return [(entry['pid'],entry['create_time']) for entry in matches if entry['ppid'] not in ids]


async def normal_network_available():
    """Do not replace a working app with a child inheriting blocked networking."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # A public HEAD verifies transport only, without keys or user data.
            await client.head('https://api.themoviedb.org')
        return True
    except httpx.RequestError:
        return False


async def restore_normal_app(roots, log_name='normal-restored-after-cache.log'):
    if not await normal_network_available():
        print('NORMAL_RESTORE_BLOCKED: network unavailable; restart from an approved network-enabled process.',flush=True)
        return False
    # Prepare before stopping a healthy process; each production build owns its files.
    web_dir=prepare_frontend('normal-'+uuid.uuid4().hex)
    for pid,created in roots:
        try:
            parent=psutil.Process(pid)
            if parent.create_time()!=created: continue
            # Children first: a multiprocessing worker can retain the listener.
            for child in reversed(parent.children(recursive=True)):
                try: child.terminate()
                except psutil.NoSuchProcess: pass
            parent.terminate()
            psutil.wait_procs([parent],timeout=5)
        except psutil.NoSuchProcess: pass
    env=dict(os.environ)
    env['REFLEX_WEB_WORKDIR']=str(web_dir)
    # Restore the caller's normal environment; diagnostic overrides were child-only.
    with (ROOT/log_name).open('w',encoding='utf-8') as log:
        restored=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod',
            '--single-port','--frontend-port','3030','--backend-port','3030'],
            cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    import urllib.request
    for _ in range(240):
        if restored.poll() is not None: return False
        try:
            with urllib.request.urlopen('http://127.0.0.1:3030/login',timeout=1):
                return True
        except OSError: await asyncio.sleep(1)
    return False


async def wait_until(predicate, measurement, timeout):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        if measurement.stop_reason: return False
        if await predicate(): return True
        await asyncio.sleep(.2)
    return False


async def main():
    load_dotenv(ROOT/'.env')
    bases={key:os.getenv(env,'').strip() for key,env in
           (('auth','XANO_AUTH_URL'),('social','XANO_SOCIAL_URL'))}
    if any(not value.startswith('https://') for value in bases.values()):
        raise RuntimeError('Configured remote HTTPS services are required')
    measurement=Measurement()
    normal_roots=normal_app_roots()
    server=ThreadingHTTPServer(('127.0.0.1',3041),handler_class(measurement,bases))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3041/auth',
        XANO_SOCIAL_URL='http://127.0.0.1:3041/social',COOKIE_SECURE='false',
        REFLEX_STATE_MANAGER_MODE='memory')
    samples=[]
    failure=''
    with (ROOT/'real-measurement-server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod',
            '--single-port','--frontend-port','3031','--backend-port','3031'],
            cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            import urllib.request
            ready=False
            for _ in range(240):
                if process.poll() is not None: raise RuntimeError('Diagnostic server exited')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:3031/login',timeout=1):
                        ready=True
                        break
                except OSError: await asyncio.sleep(1)
            if not ready: raise TimeoutError('Diagnostic server startup')
            async with async_playwright() as playwright:
                # A visible window is intentional: only the user enters credentials.
                browser=await playwright.chromium.launch(channel='msedge',headless=False)
                context=await browser.new_context(viewport={'width':1440,'height':900})
                page=await context.new_page()
                cycle=VisitCycle()
                page.on('websocket',lambda socket: socket.on('framereceived',cycle.received))
                await page.expose_function('__measurementSubmit',cycle.submitted)
                await page.add_init_script("""document.addEventListener('submit', () => {
                    window.__measurementSubmit();
                }, true);""")
                # Block remote assets/analytics; Xano traffic is server-side via proxy.
                await context.route('**/*',lambda route: route.continue_() if
                    urlsplit(route.request.url).hostname in ('localhost','127.0.0.1')
                    else route.abort())
                await page.goto('http://127.0.0.1:3031/login')
                print('READY_FOR_USER_LOGIN: Entre na janela do Edge de medicao. Nao envie credenciais pelo chat.',flush=True)
                async def profile_visible():
                    return cycle.primary_at is not None and await page.locator('.profile-identity h2').count()>0 and \
                        bool(await page.locator('.profile-identity h2').inner_text())
                authenticated=await wait_until(profile_visible,measurement,600)
                if authenticated:
                    samples.append(dict(width=1440,visit=1,phase='manual-login',
                        login_to_primary_ms=round((time.perf_counter()-cycle.submit_at)*1000)
                        if cycle.submit_at is not None else None))
                    async def complete():
                        return cycle.finished_at is not None and not await page.get_by_text('Carregando…',exact=True).is_visible()
                    initial_finished=await wait_until(complete,measurement,30)
                    samples[0]['finished']=initial_finished
                    samples[0]['cycle_observed']=cycle.metrics()
                    if not initial_finished: measurement.stop_reason=measurement.stop_reason or 'cycle-timeout'
                    for width in (1440,390):
                        await page.set_viewport_size({'width':width,'height':900})
                        for index in range(2 if width==1440 else 1,6):
                            if measurement.stop_reason: break
                            await asyncio.sleep(1)
                            started=time.perf_counter()
                            cycle.arm()
                            before=measurement.total
                            await page.goto('http://127.0.0.1:3031/conta')
                            primary=await wait_until(profile_visible,measurement,30)
                            primary_ms=round((time.perf_counter()-started)*1000)
                            finished=await wait_until(complete,measurement,30) if primary else False
                            samples.append(dict(width=width,visit=index,phase='profile-revisit',
                                primary_ms=primary_ms,primary_present=primary,finished=finished,
                                total_ms=round((time.perf_counter()-started)*1000),
                                outbound_requests=measurement.total-before,cycle_observed=cycle.metrics()))
                            if not primary or not finished: break
                        if measurement.stop_reason: break
                else:
                    failure=measurement.stop_reason or 'manual-login-timeout'
                await context.clear_cookies()
                await browser.close()
        except Exception as exc:
            # Exception messages may contain DOM, URLs or credentials; keep class only.
            failure=type(exc).__name__
        finally:
            stop_process_tree(process)
            server.shutdown()
            print('RESTORING_NORMAL_APP',flush=True)
            restored=await restore_normal_app(normal_roots)
            OUTPUT.write_text(json.dumps(dict(layer='browser-with-real-xano-via-local-proxy',
                user_logged_in=bool(samples),failure=failure,samples=samples,
                normal_restored=restored,cycle_tracking=True,
                proxy_overhead_included=True,**measurement.report()),indent=2),encoding='utf-8')
            print(json.dumps(dict(finished=True,samples=len(samples),failure=failure,
                                  stop_reason=measurement.stop_reason,normal_restored=restored)),flush=True)


if __name__=='__main__': asyncio.run(main())
