query "posts" verb=GET {
 api_group = "Codeboxd"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100
int user_id?=0
 }
 stack {
db.query post {
 where = $db.post.user_id == $input.user_id || $input.user_id == 0
 sort = {post.id: "desc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
api.lambda {
 code = "return Array.isArray($var.rows) ? $var.rows.map(row => { const safe = {...row}; delete safe.image_asset_record_id; return safe; }) : null;"
} as $public_rows
 }
 response = $public_rows
 guid = "EKfPmWtb4TCU-2nCYk6mkiHApxQ"
}
