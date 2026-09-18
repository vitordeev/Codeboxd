query "interactions" verb=GET {
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
  error = "Operação não permitida."
}
db.query user_media_interaction {
 where = $db.user_media_interaction.user_id == $auth.id
 sort = {user_media_interaction.id: "asc"}
 return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
} as $rows
 }
 response = $rows
 guid = "lHGLb1vOEmt4aLacrVGAhdFyp_8"
}
