query "posts/{id}/like" verb=DELETE {
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
db.query post_like {
 where = $db.post_like.user_id == $auth.id && $db.post_like.post_id == $input.id
 return = {type: "single"}
} as $record
conditional {
 if ($record != null) {
db.del post_like {
 field_name = "id"
 field_value = $record.id
}
}}
 }
 response = {success: true}
 guid = "XGKjubgvxaDXCrYcIK7eBq3XI7g"
}
