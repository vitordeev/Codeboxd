query "lists/{id}/items/{media_id}" verb=DELETE {
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
db.query user_list_item {
 where = $db.user_list_item.list_id == $input.id && $db.user_list_item.media_id == $input.media_id
 return = {type: "single"}
} as $item
conditional {
 if ($item != null) {
db.del user_list_item {
 field_name = "id"
 field_value = $item.id
}
}}
 }
 response = {success: true}
 guid = "YJYsP1TeL8ejd6ppwdLNagBZV2U"
}
