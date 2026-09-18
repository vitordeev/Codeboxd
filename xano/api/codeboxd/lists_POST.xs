query "lists" verb=POST {
 api_group = "Codeboxd"
 auth = "user"
 input {
text title filters=trim|min:1|max:120
text description? filters=trim|max:2000
bool is_public?=true
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
db.add user_list {
 data = {user_id: $auth.id, title: $input.title, description: $input.description, is_public: $input.is_public, updated_at: now}
} as $result
 }
 response = $result
 guid = "e0SNrmbgrquRIypbGRSj39HFkeI"
}
