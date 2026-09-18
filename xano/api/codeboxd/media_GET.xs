query "media" verb=GET {
 api_group = "Codeboxd"
 input {
text identity_key?="" filters=trim
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100

 }
 stack {
db.query media {
 where = $input.identity_key == "" || $db.media.identity_key == $input.identity_key
 sort = {media.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
 response = $rows
 guid = "aZXoHM0FsqNrgoEWCGAFZJDnvoE"
}
