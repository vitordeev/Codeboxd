query "lists/public/{id}/items" verb=GET {
 api_group = "Codeboxd"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100
int id
 }
 stack {
db.get user_list {
 field_name = "id"
 field_value = $input.id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
precondition ($record.is_public == true) {
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
 guid = "3u-cGbP12WX2Z2lJMeA47jQMjA0"
}
