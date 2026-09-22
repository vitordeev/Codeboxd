query "comments/{id}" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
text body filters=trim|min:1|max:2000
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
db.get comment {
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
db.edit comment {
 field_name = "id"
 field_value = $input.id
 data = {body: $input.body, updated_at: now}
} as $result
 }
 response = $result
 guid = "XTWhJ5ODYWMQRdbyqm4bdb7Fjmg"
}
