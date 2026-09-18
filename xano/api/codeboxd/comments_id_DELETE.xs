query "comments/{id}" verb=DELETE {
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
db.del comment {
 field_name = "id"
 field_value = $input.id
}
 }
 response = {success: true}
 guid = "PAzBpSut0XwM2jBj8QA63g0D2DU"
}
