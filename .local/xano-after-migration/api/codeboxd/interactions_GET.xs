query interactions verb=GET {
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
  
    db.query user_media_interaction {
      where = $db.user_media_interaction.user_id == $auth.id
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "lHGLb1vOEmt4aLacrVGAhdFyp_8"
}