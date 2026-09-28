query posts verb=GET {
  api_group = "Codeboxd"

  input {
    int user_id?
  }

  stack {
    db.query post {
      where = $db.post.user_id == $input.user_id || $input.user_id == 0
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "EKfPmWtb4TCU-2nCYk6mkiHApxQ"
}