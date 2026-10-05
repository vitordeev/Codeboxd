from pathlib import Path
import re

root=Path('xano/api/codeboxd')
feed=root/'feed_GET.xs'
source=feed.read_text(encoding='utf8')
start=source.index('db.query user_follow {')
end=source.index('} as $rows',start)+len('} as $rows')
source=source[:start]+'''db.query post {
 join = {user_follow: {table: "user_follow", where: $db.post.user_id == $db.user_follow.followed_id}}
 where = $db.user_follow.follower_id == $auth.id
 return = {type: "list"}
} as $rows'''+source[end:]
feed.write_text(source,encoding='utf8')
for file in root.glob('*GET.xs'):
    source=file.read_text(encoding='utf8')
    if 'return = {type: "list"}' not in source: continue
    source=source.replace(' input {',' input {\nint page?=1 filters=min:1\nint per_page?=100 filters=min:1|max:100',1)
    source=re.sub(r'db.query (\w+) \{(.*?)return = \{type: "list"\}',
        lambda m:'db.query '+m[1]+' {'+m[2]+'sort = {'+m[1]+'.id: "'+('desc' if m[1]=='post' else 'asc')+'"}\n return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}',source,flags=re.S)
    file.write_text(source,encoding='utf8')
