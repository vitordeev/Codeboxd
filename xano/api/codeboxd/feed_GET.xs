query "feed" verb=GET {
 api_group = "Codeboxd"
 auth = "user"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100

 }
 stack {
db.get user {
 field_name = "id"
 field_value = $auth.id
 output = ["id", "account_status"]
} as $actor
precondition ($actor != null && $actor.account_status != "disabled") {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.query post {
 join = {user_follow: {table: "user_follow", where: $db.post.user_id == $db.user_follow.followed_id}}
 where = $db.user_follow.follower_id == $auth.id
 sort = {post.id: "desc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
 response = $rows
 guid = "xrRcMn9iopzec83mV8yJVpSiRLc"
}
