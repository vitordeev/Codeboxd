// Delete titulos record
query "titulos/{titulos_id}" verb=DELETE {
  api_group = "Titulos"
  auth = "user"

  input {
    int titulos_id? filters=min:1
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

    function.run "Quick Start/enforce_role" {
      input = {user_id: $auth.id, required_role: "admin"}
    } as $role_check
    db.del titulos {
      field_name = "id"
      field_value = $input.titulos_id
    }
  }

  response = null
  guid = "oZz6F-zWZG0pIUJ9bAoK8egIGh4"
}