query "likes" verb=GET {
 api_group = "Codeboxd"
 auth = "user"
 input {
  int page?=1 filters=min:1
  int per_page?=100 filters=min:1|max:100
 }
 stack {
  db.get user {
   field_name = "id"
   field_value = $auth.id
   output = ["id", "account_status"]
  } as $actor
  precondition ($actor != null && $actor.account_status != "disabled") {
   error_type = "accessdenied"
   error = "Operacao nao permitida."
  }
  db.query post_like {
   where = $db.post_like.user_id == $auth.id
   sort = {post_like.id: "asc"}
   return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
  } as $rows
 }
 response = $rows
}
