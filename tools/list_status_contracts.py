"""Build the scoped follow/default-list contract, preserving original guards."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'table/user_follow.xs', 'table/post.xs', 'table/user_media_list_status.xs',
    'function/Lists/set_media_list_status.xs',
    'function/Lists/default_list_status.xs',
    'api/codeboxd/media_list_status_media_id_GET.xs',
    'api/codeboxd/media_list_status_media_id_PUT.xs',
    'api/codeboxd/follows_user_id_PUT.xs',
    'api/codeboxd/follows_user_id_DELETE.xs',
    'api/codeboxd/feed_GET.xs',
    'api/codeboxd/lists_id_items_GET.xs',
    'api/codeboxd/lists_public_id_items_GET.xs',
    'api/codeboxd/lists_id_items_POST.xs',
    'api/codeboxd/lists_id_items_media_id_DELETE.xs',
    'api/codeboxd/lists_id_DELETE.xs',
)
CLASSIFY = '''function.run "Lists/default_list_status" {
 input = {user_id: $record.user_id, default_key: $record.default_key}
} as $default_status
'''
LOCK = '''db.get user {
 field_name = "id"
 field_value = $auth.id
 lock = true
} as $actor_lock
'''


def candidate():
    documents = [(ROOT / 'xano' / name).read_text(encoding='utf-8').strip() for name in FILES]
    if any(re.search(r'^\s*(?:env|records)\s*[{=]', doc, re.M) for doc in documents):
        raise ValueError('Only schemas and logic may be deployed')
    return '\n---\n'.join(documents) + '\n'


def generate_existing():
    """One-time source rewrite; refuses to run over an already upgraded file."""
    for filename in ('lists_id_items_GET.xs', 'lists_public_id_items_GET.xs'):
        path = ROOT / 'xano/api/codeboxd' / filename
        old = path.read_text(encoding='utf-8')
        if 'Lists/default_list_status' in old:
            continue
        start = old.index('db.query user_list_item')
        end = old.index('\n }\n response =', start)
        legacy = old[start:end]
        new = CLASSIFY + '''var $rows { value = [] }
conditional {
 if ($default_status != null) {
  db.query user_media_list_status {
   where = $db.user_media_list_status.user_id == $record.user_id && $db.user_media_list_status.status == $default_status
   sort = {user_media_list_status.id: "asc"}
   return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
  } as $status_rows
  api.lambda {
   code = "return $var.status_rows.map(row => ({id: row.id, list_id: $var.record.id, media_id: row.media_id, created_at: row.created_at}));"
  } as $rows
 }
 else {
''' + legacy + '\n }\n}'
        path.write_text(old[:start] + new + old[end:], encoding='utf-8')

    path = ROOT / 'xano/api/codeboxd/lists_id_items_POST.xs'
    old = path.read_text(encoding='utf-8')
    if 'Lists/default_list_status' not in old:
        start = old.index('var $key')
        end = old.index('\n }\n response =', start)
        legacy = old[start:end]
        new = CLASSIFY + '''var $result { value = null }
conditional {
 if ($default_status != null) {
  function.run "Lists/set_media_list_status" {
   input = {user_id: $auth.id, media_id: $input.media_id, status: $default_status}
  } as $confirmed
  api.lambda {
   code = "return {id: $var.confirmed.item.id, list_id: $var.record.id, media_id: $input.media_id, created_at: $var.confirmed.item.created_at};"
  } as $result
 }
 else {
''' + legacy + '\n }\n}'
        path.write_text(old[:start] + new + old[end:], encoding='utf-8')

    path = ROOT / 'xano/api/codeboxd/lists_id_items_media_id_DELETE.xs'
    old = path.read_text(encoding='utf-8')
    if 'Lists/default_list_status' not in old:
        start = old.index('db.query user_list_item')
        end = old.index('\n }\n response =', start)
        legacy = old[start:end]
        new = CLASSIFY + '''conditional {
 if ($default_status != null) {
  function.run "Lists/set_media_list_status" {
   input = {user_id: $auth.id, media_id: $input.media_id, status: null, conditional_delete: true, expected_status: $default_status}
  } as $confirmed
 }
 else {
''' + legacy + '\n }\n}'
        path.write_text(old[:start] + new + old[end:], encoding='utf-8')

    path = ROOT / 'xano/api/codeboxd/lists_id_DELETE.xs'
    old = path.read_text(encoding='utf-8')
    if 'Lists/default_list_status' not in old:
        old = old.replace('db.transaction {', CLASSIFY + 'db.transaction {', 1)
        old = old.replace(' stack {\ndb.query user_list_item', ' stack {\n' + LOCK + '''conditional {
 if ($default_status != null) {
  db.query user_media_list_status {
   where = $db.user_media_list_status.user_id == $auth.id && $db.user_media_list_status.status == $default_status
   return = {type: "list"}
  } as $statuses
  foreach ($statuses) {
   each as $status_row {
    db.del user_media_list_status {
     field_name = "id"
     field_value = $status_row.id
    }
   }
  }
 }
}
db.query user_list_item''', 1)
        path.write_text(old, encoding='utf-8')

    for verb in ('PUT', 'DELETE'):
        path = ROOT / f'xano/api/codeboxd/follows_user_id_{verb}.xs'
        old = path.read_text(encoding='utf-8')
        if 'lock = true' in old:
            continue
        old = old.replace('int user_id\n', 'int user_id filters=min:1\n')
        start = old.index('var $key' if verb == 'PUT' else 'db.query user_follow')
        end = old.index('\n }\n response =', start)
        operation = '''db.query user_follow {
 where = $db.user_follow.follower_id == $auth.id && $db.user_follow.followed_id == $input.user_id
 return = {type: "list"}
} as $connections
'''
        if verb == 'PUT':
            operation += '''conditional {
 if (($connections|count) == 0) {
  var $key { value = $auth.id ~ ":" ~ $input.user_id }
  db.add user_follow {
   data = {follower_id: $auth.id, followed_id: $input.user_id, identity_key: $key}
  }
 }
}
'''
        else:
            operation += '''foreach ($connections) {
 each as $connection {
  db.del user_follow {
   field_name = "id"
   field_value = $connection.id
  }
 }
}
'''
        self_guard = '''precondition ($input.user_id != $auth.id) {
 error_type = "inputerror"
 error = "Você não pode seguir a si mesmo."
}
''' if verb == 'DELETE' else ''
        new = self_guard + 'db.transaction {\n stack {\n' + LOCK + operation + '\n }\n}'
        old = old[:start] + new + old[end:]
        old = re.sub(r' response = .*\n guid =', ' response = {follower_id: $auth.id, followed_id: $input.user_id, following: ' + ('true' if verb == 'PUT' else 'false') + '}\n guid =', old)
        path.write_text(old, encoding='utf-8')


if __name__ == '__main__':
    generate_existing()
