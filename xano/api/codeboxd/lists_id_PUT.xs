query "lists/{id}" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
text title filters=trim|min:1|max:120
text description? filters=trim|max:2000
bool is_public?=true
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
db.edit user_list {
 field_name = "id"
 field_value = $input.id
 data = {title: $input.title, description: $input.description, is_public: $input.is_public, updated_at: now}
} as $result
 }
 response = $result
 guid = "YZaczDP8F7yjnoLtnTJ_G1sh1eI"
}
