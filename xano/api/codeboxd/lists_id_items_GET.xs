query "lists/{id}/items" verb=GET {
 api_group = "Codeboxd"
 auth = "user"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100
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
precondition ($record.is_public == true || $record.user_id == $auth.id) {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.query user_list_item {
 where = $db.user_list_item.list_id == $input.id
 sort = {user_list_item.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
 response = $rows
 guid = "_3l4NasD5zKmsOzfSmjhKomojyM"
}
