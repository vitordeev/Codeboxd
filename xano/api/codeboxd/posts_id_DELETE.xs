query "posts/{id}" verb=DELETE {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
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
db.get post {
 field_name = "id"
 field_value = $input.id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
precondition ($record.user_id == $auth.id) {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.transaction {
 stack {
db.get user {
 field_name = "id"
 field_value = $auth.id
 lock = true
} as $actor_lock
function.run "Security/require_current_session" {
 input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
}
precondition ($actor_lock != null && $actor_lock.account_status == "active") {
 error_type = "accessdenied"
 error = "Operação não permitida."
}
db.get post {
 field_name = "id"
 field_value = $input.id
 lock = true
} as $locked_post
precondition ($locked_post != null && $locked_post.user_id == $auth.id) {
 error_type = "notfound"
 error = "Publicação não encontrada."
}
db.query comment {
 where = $db.comment.post_id == $input.id
 return = {type: "list"}
} as $comments
foreach ($comments) {
 each as $child {
db.del comment {
 field_name = "id"
 field_value = $child.id
}
}}
db.query post_like {
 where = $db.post_like.post_id == $input.id
 return = {type: "list"}
} as $likes
foreach ($likes) {
 each as $child {
db.del post_like {
 field_name = "id"
 field_value = $child.id
}
}}
db.del post {
 field_name = "id"
 field_value = $input.id
}
conditional {
 if ($locked_post.image_asset_record_id != null && $locked_post.image_asset_record_id > 0) {
  function.run "PostImages/queue_cleanup" {
   input = {asset_record_id: $locked_post.image_asset_record_id, user_id: $auth.id, post_id: $locked_post.id, replaced: false}
  }
 }
}
 }
}
 }
 response = {success: true}
 guid = "_iipjta4Ftcsixdn-Y7HXhG3BJI"
}
