query "posts/{id}/discussion" verb=GET {
 api_group = "Codeboxd"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100
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
 sort = {comment.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $comments
db.query post_like {
 where = $db.post_like.post_id == $input.id
 sort = {post_like.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $likes
 }
 response = {comments: $comments, likes: $likes}
 guid = "4mlgQNRrEIJI_DSHNj4yLRWS9E0"
}
