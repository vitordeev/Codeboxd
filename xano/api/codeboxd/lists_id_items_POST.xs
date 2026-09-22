query "lists/{id}/items" verb=POST {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
int media_id
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
db.get user_list {
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
db.get media {
 field_name = "id"
 field_value = $input.media_id
} as $media
precondition ($media != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
var $key { value = $input.id ~ ":" ~ $input.media_id }
db.add_or_edit user_list_item {
 field_name = "identity_key"
 field_value = $key
 data = {list_id: $input.id, media_id: $input.media_id, identity_key: $key}
} as $result
 }
 response = $result
 guid = "hzINFcLoRjjnJNVIeJojah0z-po"
}
