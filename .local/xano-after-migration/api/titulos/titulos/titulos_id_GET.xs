// Get titulos record
query "titulos/{titulos_id}" verb=GET {
  api_group = "Titulos"

  input {
    int titulos_id? filters=min:1
  }

  stack {
    db.get titulos {
      field_name = "id"
      field_value = $input.titulos_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "iJvg2p51T3_boC6tqVVdOTOkM_o"
}