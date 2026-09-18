query "lists/public" verb=GET {
 api_group = "Codeboxd"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100

 }
 stack {
db.query user_list {
 where = $db.user_list.is_public == true
 sort = {user_list.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
 response = $rows
 guid = "1VuUeoKvEwsrFexYYD4FjLwNd54"
}
