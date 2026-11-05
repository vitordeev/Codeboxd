query "lists/{id}/items" verb=GET {
 api_group = "Codeboxd"
 auth = "user"
 input {
int page?=1 filters=min:1
int per_page?=100 filters=min:1|max:100
int id
 }
 stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

db.get user {
 field_name = "id"
 field_value = $auth.id
 output = ["id", "account_status"]
} as $actor
precondition ($actor != null && $actor.account_status != "disabled") {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.get user_list {
 field_name = "id"
 field_value = $input.id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
precondition ($record.is_public == true || $record.user_id == $auth.id) {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
function.run "Lists/default_list_status" {
 input = {user_id: $record.user_id, default_key: $record.default_key}
} as $default_status
var $rows { value = [] }
conditional {
 if ($default_status != null) {
  db.query user_media_list_status {
   where = $db.user_media_list_status.user_id == $record.user_id && $db.user_media_list_status.status == $default_status
   sort = {user_media_list_status.id: "asc"}
   return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
  } as $status_rows
  api.lambda {
   code = "return $var.status_rows.map(row => ({id: row.id, list_id: $var.record.id, media_id: row.media_id, created_at: row.created_at}));"
  } as $rows
 }
 else {
db.query user_list_item {
 where = $db.user_list_item.list_id == $input.id
 sort = {user_list_item.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
}
 }
 response = $rows
 guid = "_3l4NasD5zKmsOzfSmjhKomojyM"
}
