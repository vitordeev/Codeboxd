// Edit titulos record
query "titulos/{titulos_id}" verb=PATCH {
  api_group = "Titulos"
  auth = "user"

  input {
    int titulos_id? filters=min:1
    dblink {
      table = "titulos"
    }
  }

  stack {
    function.run "Quick Start/enforce_role" {
      input = {user_id: $auth.id, required_role: "admin"}
    } as $role_check
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch titulos {
      field_name = "id"
      field_value = $input.titulos_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "94DY-atWIycUYtO4B8OxPT8h3fU"
}