query "follows/{user_id}" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int user_id filters=min:1
 }
 stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

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
db.transaction {
 stack {
db.get user {
 field_name = "id"
 field_value = $auth.id
 lock = true
} as $actor_lock
db.query user_follow {
 where = $db.user_follow.follower_id == $auth.id && $db.user_follow.followed_id == $input.user_id
 return = {type: "list"}
} as $connections
conditional {
 if (($connections|count) == 0) {
  var $key { value = $auth.id ~ ":" ~ $input.user_id }
  db.add user_follow {
   data = {follower_id: $auth.id, followed_id: $input.user_id, identity_key: $key}
  }
 }
}

 }
}
 }
 response = {follower_id: $auth.id, followed_id: $input.user_id, following: true}
 guid = "tbaHveLfCKvAkaW3CmVYe002YHU"
}
