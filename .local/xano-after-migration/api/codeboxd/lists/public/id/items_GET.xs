query "lists/public/{id}/items" verb=GET {
  api_group = "Codeboxd"

  input {
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
  
    precondition ($record.is_public) {
      error_type = "accessdenied"
      error = "Operação não permitida."
    }
  
    db.query user_list_item {
      where = $db.user_list_item.list_id == $input.id
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "3u-cGbP12WX2Z2lJMeA47jQMjA0"
}