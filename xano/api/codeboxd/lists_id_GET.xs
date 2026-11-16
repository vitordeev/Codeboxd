query "lists/{id}" verb=GET {
 api_group = "Codeboxd"
 auth = "user"
 input {
  int id
 }
 stack {
  function.run "Security/require_current_session" {
   input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
  }
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
   output = ["id", "user_id", "title", "description", "is_public"]
  } as $record
  precondition ($record != null && $record.user_id == $auth.id) {
   error_type = "notfound"
   error = "Registro não encontrado."
  }
  db.query profile {
   where = $db.profile.user_id == $record.user_id
   return = {type: "single"}
   output = ["user_id", "username", "display_name", "avatar_url"]
  } as $creator
  api.lambda {
   code = "return {id: $var.record.id, user_id: $var.record.user_id, title: $var.record.title, description: $var.record.description || '', is_public: $var.record.is_public, creator: {user_id: $var.record.user_id, username: $var.creator ? $var.creator.username : '', display_name: $var.creator ? $var.creator.display_name : 'Usuário', avatar_url: $var.creator ? $var.creator.avatar_url : ''}};"
  } as $result
 }
 response = $result
 guid = "CodeboxdOwnerListDetail20261115"
}
