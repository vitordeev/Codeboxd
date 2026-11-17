query "profiles" verb=GET {
 api_group = "Codeboxd"
 input {
text? q? filters=trim|max:80
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100

 }
 stack {
var $result { value = null }
conditional {
 if ($input.q == null) {
db.query profile {
 sort = {profile.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
var.update $result { value = $rows }
 }
 else {
  api.lambda {
   code = "return $input.q.replace(/[\\\\%_]/g, '\\\\$&');"
  } as $literal
  api.lambda {
   code = "return Math.min($input.per_page, 50);"
  } as $limit
  db.query profile {
   where = $input.q == "" || $db.profile.username includes $literal || $db.profile.display_name includes $literal
   sort = {profile.id: "asc"}
   output = ["itemsTotal", "curPage", "nextPage", "items.user_id", "items.username", "items.display_name", "items.avatar_url"]
   return = {type: "list", paging: {page: $input.page, per_page: $limit, totals: true, metadata: true}}
  } as $found
  var.update $result {
   value = {items: $found.items, total: $found.itemsTotal, page: $found.curPage, next_page: $found.nextPage, per_page: $limit}
  }
 }
}
 }
 response = $result
 guid = "UgGkVqSec1JtB7reKdgaBw6U3Zo"
}
