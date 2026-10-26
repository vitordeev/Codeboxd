"""GET-only TMDB verification, before/after local token replacement. No values logged."""
import json
import httpx
from dotenv import dotenv_values
from audit_inventory import ROOT, HERE, git


def main():
    current = dotenv_values(ROOT / '.env').get('TMDB_READ_TOKEN', '')
    old_config = git('cat-file', 'blob', 'dd4d283d89a38472f23fab38fd757a6407a09497').decode('utf-8')
    from io import StringIO
    exposed = dotenv_values(stream=StringIO(old_config)).get('TMDB_READ_TOKEN', '')
    if not current or not exposed:
        raise RuntimeError('Missing configuration')
    report = {'current_matches_exposed': current == exposed, 'mode': 'GET-only'}
    with httpx.Client(timeout=15, follow_redirects=False) as client:
        def validate(token):
            response = client.get('https://api.themoviedb.org/3/authentication',
                                  headers={'Authorization': 'Bearer ' + token})
            return {'http_status': response.status_code,
                    'authenticated': response.status_code == 200 and response.json().get('success') is True}
        report['current'] = validate(current)
        report['exposed'] = report['current'] if current == exposed else validate(exposed)
        if current != exposed and report['current']['authenticated']:
            report['catalog_reads'] = {}
            for category, path in (('movies', 'movie/popular'), ('series', 'tv/popular')):
                response = client.get('https://api.themoviedb.org/3/' + path,
                                      headers={'Authorization': 'Bearer ' + current},
                                      params={'language': 'pt-BR', 'page': 1})
                payload = response.json() if response.status_code == 200 else {}
                results = payload.get('results')
                report['catalog_reads'][category] = {'http_status': response.status_code,
                    'has_results': isinstance(results, list) and bool(results)}
    report['rotation_verified'] = (current != exposed and report['current']['authenticated']
                                   and report['exposed']['http_status'] == 401)
    (HERE / 'tmdb-check.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except httpx.RequestError:
        raise SystemExit('Network unavailable for TMDB GET verification; raw output suppressed') from None
    except Exception:
        raise SystemExit('TMDB verification failed; raw output suppressed') from None
