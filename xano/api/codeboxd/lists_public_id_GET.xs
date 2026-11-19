query "lists/public/{id}" verb=GET {
 api_group = "Codeboxd"
 input {
  int id
 }
 stack {
  db.get user_list {
   field_name = "id"
   field_value = $input.id
   output = ["id", "user_id", "title", "description", "is_public"]
  } as $record
  precondition ($record != null) {
   error_type = "notfound"
   error = "Registro não encontrado."
  }
  precondition ($record.is_public == true) {
   error_type = "notfound"
   error = "Registro não encontrado."
  }
  db.query profile {
   where = $db.profile.user_id == $record.user_id
   return = {type: "single"}
   output = ["user_id", "username", "display_name", "avatar_url"]
  } as $creator
  api.lambda {
   code = "return {id: $var.record.id, user_id: $var.record.user_id, title: $var.record.title, description: $var.record.description || '', is_public: true, creator: {user_id: $var.record.user_id, username: $var.creator ? $var.creator.username : '', display_name: $var.creator ? $var.creator.display_name : 'Usuário', avatar_url: $var.creator ? $var.creator.avatar_url : ''}};"
  } as $result
 }
 response = $result
 guid = "CodeboxdPublicListDetail20261115"
}
