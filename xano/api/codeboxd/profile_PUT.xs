query "profile" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
text username filters=trim|lower|min:3|max:30
text display_name filters=trim|min:1|max:80
text bio? filters=trim|max:1000
text avatar_url? filters=trim|max:500
 }
 stack {
api.lambda {
 code = "if (!/^[a-z0-9_]{3,30}$/.test($input.username)) return false; if (!$input.avatar_url) return true; try { const u = new URL($input.avatar_url); return u.protocol === 'https:' && !!u.hostname && !u.username && !u.password; } catch { return false; }"
} as $valid_profile
precondition ($valid_profile) {
 error_type = "inputerror"
 error = "Nome de usuario ou URL de foto invalida."
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
db.query profile {
 where = $db.profile.username == $input.username
 return = {type: "single"}
} as $duplicate
precondition ($duplicate == null || $duplicate.user_id == $auth.id) {
  error_type = "inputerror"
  error = "Nome de usuário indisponível."
}
db.query user {
 where = $db.user.username == $input.username && $db.user.id != $auth.id
 return = {type: "single"}
} as $legacy
precondition ($legacy == null) {
  error_type = "inputerror"
  error = "Nome de usuário indisponível."
}
db.transaction {
 stack {
db.add_or_edit profile {
 field_name = "user_id"
 field_value = $auth.id
 data = {user_id: $auth.id, username: $input.username, display_name: $input.display_name, bio: $input.bio, avatar_url: $input.avatar_url}
} as $result
db.edit user {
 field_name = "id"
 field_value = $auth.id
 data = {username: $input.username, name: $input.display_name}
} as $updated_user
 }
}
 }
 response = $result
 guid = "o13suNaroufjBeOUShNCayscUc4"
}
