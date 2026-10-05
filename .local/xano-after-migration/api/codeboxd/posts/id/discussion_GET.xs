query "posts/{id}/discussion" verb=GET {
  api_group = "Codeboxd"

  input {
    int id
  }

  stack {
    db.get post {
      field_name = "id"
      field_value = $input.id
    } as $record
  
    precondition ($record != null) {
      error_type = "notfound"
      error = "Registro não encontrado."
    }
  
    db.query comment {
      where = $db.comment.post_id == $input.id
      return = {type: "list"}
    } as $comments
  
    db.query post_like {
      where = $db.post_like.post_id == $input.id
      return = {type: "list"}
    } as $likes
  }

  response = {comments: $comments, likes: $likes}
  guid = "4mlgQNRrEIJI_DSHNj4yLRWS9E0"
}