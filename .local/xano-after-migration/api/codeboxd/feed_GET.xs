query feed verb=GET {
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
  
    db.query user_follow {
      where = $db.user_follow.follower_id == $auth.id
      return = {type: "list"}
    } as $follows
  
    api.lambda {
      code = "return $var.follows.map(f => f.followed_id);"
    } as $following_ids
  
    db.query post {
      where = $db.post.user_id in $following_ids
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "xrRcMn9iopzec83mV8yJVpSiRLc"
}