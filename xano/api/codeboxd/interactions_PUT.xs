query "interactions" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int media_id
enum status { values = ["planned", "in_progress", "completed", "dropped"] }
decimal rating?=0
text review? filters=trim|max:10000
bool spoiler?=false
 }
 stack {
db.get user {
 field_name = "id"
 field_value = $auth.id
 output = ["id", "account_status"]
} as $actor
precondition ($actor != null && $actor.account_status != "disabled") {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.get media {
 field_name = "id"
 field_value = $input.media_id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
precondition ($input.rating >= 0 && $input.rating <= 5 && ($input.rating * 2) % 1 == 0) {
  error_type = "inputerror"
  error = "Nota deve estar entre 0,5 e 5, em passos de 0,5."
}
var $key { value = $auth.id ~ ":" ~ $input.media_id }
db.add_or_edit user_media_interaction {
 field_name = "identity_key"
 field_value = $key
 data = {user_id: $auth.id, media_id: $input.media_id, status: $input.status, rating: $input.rating, review: $input.review, spoiler: $input.spoiler, updated_at: now, identity_key: $key}
} as $result
 }
 response = $result
 guid = "fjLiz9t_uHh3TOWyCthIv6LLYDE"
}
