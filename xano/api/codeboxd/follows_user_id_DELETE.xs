query "follows/{user_id}" verb=DELETE {
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
db.query user_follow {
 where = $db.user_follow.follower_id == $auth.id && $db.user_follow.followed_id == $input.user_id
 return = {type: "single"}
} as $record
conditional {
 if ($record != null) {
db.del user_follow {
 field_name = "id"
 field_value = $record.id
}
}}
 }
 response = {success: true}
 guid = "h0jPckwo3IeRQvBiqkwznXOHoWA"
}
