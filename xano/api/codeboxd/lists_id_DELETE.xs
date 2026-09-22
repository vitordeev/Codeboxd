query "lists/{id}" verb=DELETE {
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
db.transaction {
 stack {
db.query user_list_item {
 where = $db.user_list_item.list_id == $input.id
 return = {type: "list"}
} as $items
foreach ($items) {
 each as $child {
db.del user_list_item {
 field_name = "id"
 field_value = $child.id
}
}}
db.del user_list {
 field_name = "id"
 field_value = $input.id
}
 }
}
 }
 response = {success: true}
 guid = "13idjuue_hg2Tj95U8H-mA5m3Ro"
}
