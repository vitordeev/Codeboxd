// Delete titulos record
query "titulos/{titulos_id}" verb=DELETE {
  api_group = "Titulos"

  input {
    int titulos_id? filters=min:1
  }

  stack {
    db.del titulos {
      field_name = "id"
      field_value = $input.titulos_id
    }
  }

  response = null
  guid = "oZz6F-zWZG0pIUJ9bAoK8egIGh4"
}