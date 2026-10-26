function "Security/require_current_session" {
  input {
    int user_id
    json extras
    bool allow_reset?=false
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "account_status", "session_version"]
    } as $session_user

    precondition ($session_user != null && $session_user.account_status != "disabled") {
      error_type = "unauthorized"
      error = "Sessão inválida. Entre novamente."
    }

    api.lambda {
      code = "const e = $input.extras || {}; return Number.isInteger(e.session_version) && e.session_version >= 0 && e.session_version === ($var.session_user.session_version ?? 0) && (e.purpose === 'session' || ($input.allow_reset === true && e.purpose === 'password_reset'));"
    } as $session_valid

    precondition ($session_valid) {
      error_type = "unauthorized"
      error = "Sessão expirada. Entre novamente."
    }
  }

  response = null
  guid = "LK1-t6jMxADc_vsnGxhFLousKzA"
}
