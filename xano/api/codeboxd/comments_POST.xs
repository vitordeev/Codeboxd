query "comments" verb=POST {
 api_group = "Codeboxd"
 auth = "user"
 input {
int post_id
text body filters=trim|min:1|max:2000
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
db.get post {
 field_name = "id"
 field_value = $input.post_id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
db.add comment {
 data = {user_id: $auth.id, post_id: $input.post_id, body: $input.body, updated_at: now}
} as $result
 }
 response = $result
 guid = "MFYBXCn7QgDoViz_u7UzCUeqYUA"
}
