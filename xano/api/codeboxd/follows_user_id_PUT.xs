query "follows/{user_id}" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int user_id
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
db.get user {
 field_name = "id"
 field_value = $input.user_id
} as $target
precondition ($target != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
precondition ($input.user_id != $auth.id) {
  error_type = "inputerror"
  error = "Você não pode seguir a si mesmo."
}
var $key { value = $auth.id ~ ":" ~ $input.user_id }
db.add_or_edit user_follow {
 field_name = "identity_key"
 field_value = $key
 data = {follower_id: $auth.id, followed_id: $input.user_id, identity_key: $key}
} as $result
 }
 response = $result
 guid = "tbaHveLfCKvAkaW3CmVYe002YHU"
}
