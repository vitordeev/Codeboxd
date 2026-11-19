query "lists/public" verb=GET {
 api_group = "Codeboxd"
 input {
text? q? filters=trim|max:80
int creator_id?=0 filters=min:0
text search_in?="title" filters=trim
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100

 }
 stack {
precondition ($input.search_in == "title" || $input.search_in == "title_description") {
 error_type = "inputerror"
 error = "Critério de busca inválido."
}
var $result { value = null }
conditional {
 if ($input.q == null && $input.creator_id == 0 && $input.search_in == "title") {
db.query user_list {
 where = $db.user_list.is_public == true
 sort = {user_list.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
var.update $result { value = $rows }
 }
 else {
  api.lambda {
   code = "return ($input.q || '').replace(/[\\\\%_]/g, '\\\\$&');"
  } as $literal
  api.lambda {
   code = "return Math.min($input.per_page, 50);"
  } as $limit
  db.query user_list {
   where = $db.user_list.is_public == true && ($input.creator_id == 0 || $db.user_list.user_id == $input.creator_id) && ($input.q == null || $input.q == "" || $db.user_list.title includes $literal || ($input.search_in == "title_description" && $db.user_list.description includes $literal))
   sort = {user_list.title: "asc", user_list.id: "asc"}
   addon = [
    {name: "search_list_creator", input: {user_id: $output.user_id}, as: "items.creator"}
    {name: "search_list_custom_count", input: {list_id: $output.id}, as: "items.custom_count"}
    {name: "search_list_default_count", input: {user_id: $output.user_id, default_key: $output.default_key}, as: "items.default_count"}
   ]
   output = ["itemsTotal", "curPage", "nextPage", "items.id", "items.user_id", "items.title", "items.description", "items.default_key", "items.creator", "items.custom_count", "items.default_count"]
   return = {type: "list", paging: {page: $input.page, per_page: $limit, totals: true, metadata: true}}
  } as $found
  api.lambda {
   code = "return {items: $var.found.items.map(row => ({id: row.id, user_id: row.user_id, title: row.title, description: row.description || '', items_count: row.default_key === row.user_id + ':planned' || row.default_key === row.user_id + ':completed' ? row.default_count : row.custom_count, creator: row.creator || {user_id: row.user_id, username: '', display_name: 'Usuário', avatar_url: ''}})), total: $var.found.itemsTotal, page: $var.found.curPage, next_page: $var.found.nextPage, per_page: $var.limit};"
  } as $searched
  var.update $result { value = $searched }
 }
}
 }
 response = $result
 guid = "1VuUeoKvEwsrFexYYD4FjLwNd54"
}
