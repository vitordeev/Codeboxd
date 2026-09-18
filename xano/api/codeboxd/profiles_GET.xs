query "profiles" verb=GET {
 api_group = "Codeboxd"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100

 }
 stack {
db.query profile {
 sort = {profile.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
 response = $rows
 guid = "UgGkVqSec1JtB7reKdgaBw6U3Zo"
}
