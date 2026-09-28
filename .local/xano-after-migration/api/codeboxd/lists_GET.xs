query lists verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
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
  
    db.query user_list {
      where = $db.user_list.user_id == $auth.id
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "zUEDvn06ODhCr4xWHoRo_y_0S1E"
}