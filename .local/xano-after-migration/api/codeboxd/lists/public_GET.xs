query "lists/public" verb=GET {
  api_group = "Codeboxd"

  input {
  }

  stack {
    db.query user_list {
      where = $db.user_list.is_public == true
      return = {type: "list"}
    } as $rows
  }

  response = $rows
  guid = "1VuUeoKvEwsrFexYYD4FjLwNd54"
}