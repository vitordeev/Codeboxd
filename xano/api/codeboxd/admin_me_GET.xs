query "admin/me" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "username", "name", "account_status", "role"]
    } as $actor

    precondition ($actor != null && $actor.account_status == "active" && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso administrativo não permitido."
    }

    db.get profile {
      field_name = "user_id"
      field_value = $auth.id
      output = ["display_name", "avatar_url"]
    } as $profile
  }

  response = {
    id: $actor.id
    username: $actor.username
    name: $actor.name
    display_name: $profile.display_name
    avatar_url: $profile.avatar_url
    role: $actor.role
  }
}
