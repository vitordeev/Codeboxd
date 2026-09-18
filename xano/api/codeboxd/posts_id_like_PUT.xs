query "posts/{id}/like" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
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
 field_value = $input.id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
var $key { value = $auth.id ~ ":" ~ $input.id }
db.add_or_edit post_like {
 field_name = "identity_key"
 field_value = $key
 data = {user_id: $auth.id, post_id: $input.id, identity_key: $key}
} as $result
 }
 response = $result
 guid = "FPIqrapDgIMLfuMvO4WsLLRlXME"
}
