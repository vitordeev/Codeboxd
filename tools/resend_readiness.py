"""Read provider status/counts without exposing keys, addresses or messages."""
import argparse
import json
from pathlib import Path
import time

from dotenv import dotenv_values
from tools.list_status_live import PacedClient
from tools.session_revocation import metadata_config

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = '''function "cb_resend_readiness" {
 input {}
 stack {
  api.request {
   url = "https://api.resend.com/domains"
   method = "GET"
   headers = ["Authorization: Bearer " ~ $env.RESEND_API_KEY]
   timeout = 15
  } as $domains
  api.request {
   url = "https://api.resend.com/inboxes"
   method = "GET"
   headers = ["Authorization: Bearer " ~ $env.RESEND_API_KEY]
   timeout = 15
  } as $inboxes
  var $domain_count { value = null }
  var $inbox_count { value = null }
  conditional {
   if ($domains.response.status == 200) {
    var.update $domain_count { value = $domains.response.result.data|count }
   }
  }
  conditional {
   if ($inboxes.response.status == 200) {
    var.update $inbox_count { value = $inboxes.response.result.data|count }
   }
  }
 }
 response = {
  domains_http_status: $domains.response.status
  inboxes_http_status: $inboxes.response.status
  domain_count: $domain_count
  inbox_count: $inbox_count
  key_present: $env.RESEND_API_KEY != null && $env.RESEND_API_KEY != ""
  sender_present: $env.RESEND_FROM != null && $env.RESEND_FROM != ""
 }
}'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve previous evidence')
    report = {'layer': 'local_resend_key_and_isolated_interpreter_probe', 'sent_emails': 0,
              'provider_resources_created': 0, 'published': False,
              'published_environment_validated': False}
    config = dotenv_values(ROOT / '.env')
    base, headers = metadata_config()
    with PacedClient(timeout=45) as client:
        for route in ('domains', 'inboxes'):
            response = client.get('https://api.resend.com/' + route,
                                  headers={'Authorization': 'Bearer ' + config.get('RESEND_API_KEY', '')})
            report['local_key_' + route + '_http_status'] = response.status_code
        response = client.post(base + '/multidoc/debug',
            headers={**headers, 'Content-Type': 'text/x-xanoscript'},
            params={'entry_obj_type': 'function', 'entry_obj_name': 'cb_resend_readiness', 'input': '{}'}, content=SCRIPT)
        response.raise_for_status()
        data = response.json()
        debug_id = data.get('id') or data.get('debug_id')
        for _ in range(20):
            if data.get('status') not in ('pending', 'queued', 'running'):
                break
            time.sleep(1)
            response = client.get(base + '/multidoc/debug/' + str(debug_id), headers=headers)
            response.raise_for_status()
            data = response.json()
        report['remote_debug_status'] = data.get('status')
        if data.get('status') == 'ok':
            summary = data.get('result')
            if isinstance(summary, str):
                try:
                    summary = json.loads(summary)
                except json.JSONDecodeError:
                    report['summary_parse_failure'] = True
                    summary = None
            safe = {'domains_http_status', 'inboxes_http_status', 'domain_count',
                    'verified_domain_count', 'inbox_count', 'key_present', 'sender_present'}
            if isinstance(summary, dict):
                report['interpreter_environment'] = {k: v for k, v in summary.items()
                    if k in safe and (v is None or type(v) in (int, bool))}
    args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
