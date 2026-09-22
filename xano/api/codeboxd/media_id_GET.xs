query "media/{id}" verb=GET {
 api_group = "Codeboxd"
 input {
int id
 }
 stack {
db.get media {
 field_name = "id"
 field_value = $input.id
} as $result
precondition ($result != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
 }
 response = $result
 guid = "TrW-KmSyGUUPqF38dfs37tmPlwE"
}
