// Consume a six-digit code and issue a short-lived reset credential.
query "reset/magic-link-login" verb=POST {
  api_group = "Authentication"
  input {
    text magic_token filters=trim|min:6|max:6
    email email filters=trim|lower
  }

  stack {
    var $reset_session_version { value = 0 }
    api.lambda {
      code = "return /^[0-9]{6}$/.test($input.magic_token);"
    } as $valid_format
    precondition ($valid_format) {
      error_type = "unauthorized"
      error = "Código inválido ou expirado. Solicite um novo código."
    }

    var $accepted { value = false }
    var $reset_user_id { value = 0 }
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "account_status"]
    } as $user

    conditional {
      if ($user != null && $user.account_status == "active") {
        db.transaction {
          stack {
            // Serialize attempts and one-time consumption on the account row.
            db.edit user {
              field_name = "id"
              field_value = $user.id
              data = {updated_at: now}
            }
            db.get user {
              field_name = "id"
              field_value = $user.id
            } as $locked_user

            conditional {
              if ($locked_user.account_status == "active" && $locked_user.password_reset_format == "six_digits" && $locked_user.password_reset.token != null && $locked_user.password_reset.used == false && $locked_user.password_reset.expiration > now && $locked_user.password_reset_attempts < 5) {
                security.check_password {
                  text_password = $input.magic_token
                  hash_password = $locked_user.password_reset.token
                } as $matches

                db.edit user {
                  field_name = "id"
                  field_value = $user.id
                  data = {password_reset_attempts: ($locked_user.password_reset_attempts + 1)}
                }
                conditional {
                  if ($matches) {
                    db.edit user {
                      field_name = "id"
                      field_value = $user.id
                      data = {
                        password_reset: {
                          token: $locked_user.password_reset.token
                          expiration: $locked_user.password_reset.expiration
                          used: true
                        }
                      }
                    }
                    var.update $accepted { value = true }
                    var.update $reset_user_id { value = $user.id }
                    api.lambda {
                      code = "return $var.locked_user.session_version ?? 0;"
                    } as $consumed_session_version
                    var.update $reset_session_version { value = $consumed_session_version }

                  }
                }
              }
            }
          }
        }
      }
    }

    // Outside db.transaction so rejected attempts remain persisted.
    precondition ($accepted) {
      error_type = "unauthorized"
      error = "Código inválido ou expirado. Solicite um novo código."
    }
    security.create_auth_token {
      table = "user"
      extras = {purpose: "password_reset", session_version: $reset_session_version}
      expiration = 300
      id = $reset_user_id
    } as $auth_token
    function.run "Quick Start/log_event" {
      input = {user_id: $reset_user_id, action: "login_for_password_reset", metadata: {}}
    }
  }

  response = {authToken: $auth_token, user_id: $reset_user_id}
  tags = ["xano:quick-start"]
  guid = "dt11WPhZBTfemUoGnpTO8EPVmuY"
}
