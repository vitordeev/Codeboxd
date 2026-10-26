"""Reload the verified normal app in its own existing frontend directory."""
import asyncio
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
import psutil
from dotenv import dotenv_values
from tools.real_login_measurement import normal_app_roots, normal_network_available


async def main():
    if not await normal_network_available(): raise RuntimeError('Network unavailable; original app preserved')
    roots = normal_app_roots()
    if len(roots) != 1: raise RuntimeError('Expected one normal app launcher')
    pid, created = roots[0]
    parent = psutil.Process(pid)
    if parent.create_time() != created: raise RuntimeError('Process changed')
    env = parent.environ()
    configured = dotenv_values(ROOT / '.env').get('DEFAULT_LIST_IDENTITY_ENABLED')
    if configured is not None: env['DEFAULT_LIST_IDENTITY_ENABLED'] = configured
    frontend = Path(env.get('REFLEX_WEB_WORKDIR', '')).resolve()
    if not frontend.is_relative_to((ROOT / '.local/frontends').resolve()) or not frontend.is_dir():
        raise RuntimeError('Unexpected frontend path')
    if env.get('REFLEX_APP_MODULE_IMPORT'): raise RuntimeError('Refuse fixture environment')
    children = parent.children(recursive=True)
    for child in reversed(children):
        try: child.terminate()
        except psutil.NoSuchProcess: pass
    parent.terminate()
    _, alive = psutil.wait_procs([parent] + children, timeout=10)
    if alive: raise RuntimeError('Old app still running')
    log_path = ROOT / 'public-list-groups-server.log'
    with log_path.open('w', encoding='utf-8') as log:
        process = subprocess.Popen([sys.executable, '-m', 'reflex', 'run', '--env', 'prod',
            '--single-port', '--frontend-port', '3030', '--backend-port', '3030'],
            cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    for _ in range(240):
        if process.poll() is not None: raise RuntimeError('App exited; inspect log')
        try:
            with urllib.request.urlopen('http://127.0.0.1:3030/listas', timeout=1):
                print('APP_RELOADED_3030', flush=True)
                return
        except OSError: await asyncio.sleep(1)
    raise TimeoutError('App startup')


if __name__ == '__main__': asyncio.run(main())
