query "posts/{id}" verb=DELETE {
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
precondition ($record.user_id == $auth.id) {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.transaction {
 stack {
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
 }
}
 }
 response = {success: true}
 guid = "_iipjta4Ftcsixdn-Y7HXhG3BJI"
}
