query "follows/{user_id}" verb=DELETE {
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
foreach ($connections) {
 each as $connection {
  db.del user_follow {
   field_name = "id"
   field_value = $connection.id
  }
 }
}

 }
}
 }
 response = {follower_id: $auth.id, followed_id: $input.user_id, following: false}
 guid = "h0jPckwo3IeRQvBiqkwznXOHoWA"
}
