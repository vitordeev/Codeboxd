query "posts/{id}" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
text body filters=trim|min:1|max:5000
int media_id?=0
bool spoiler?=false
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
conditional {
 if ($input.media_id > 0) {
db.get media {
 field_name = "id"
 field_value = $input.media_id
} as $media
precondition ($media != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
}}
db.edit post {
 field_name = "id"
 field_value = $input.id
 data = {body: $input.body, media_id: $input.media_id, spoiler: $input.spoiler, updated_at: now}
} as $result
 }
 response = $result
 guid = "qe--qlzGinsokmakSyTWuKE18eo"
}
