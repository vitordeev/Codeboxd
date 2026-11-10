// Allows user to update the password in the password reset flow
query "reset/update_password" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text password filters=min:8|max:128
    text confirm_password filters=max:128
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: true}
    }

    // A normal login session is not proof of password recovery.
    precondition ($auth.extras.purpose == "password_reset") {
      error_type = "unauthorized"
      error = "Solicite um código de recuperação para redefinir a senha."
    }
    api.lambda {
      code = "const p = $input.password; const n = Array.from(p).length; return n >= 8 && n <= 128 && /[A-Za-z]/.test(p) && /[0-9]/.test(p);"
    } as $valid_password
    precondition ($valid_password) {
      error_type = "inputerror"
      error = "A senha deve ter de 8 a 128 caracteres, incluindo letra e número."
    }

    // Check that the password inputs are matching
    precondition ($input.password == $input.confirm_password) {
      error_type = "inputerror"
      error = "As senhas não coincidem."
    }
  
    // Get user record based on the id of the auth token
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status"]
    } as $user
  
    // Check that the user record id matches the auth id
    precondition ($user != null && $user.id == $auth.id && $user.account_status == "active") {
      error_type = "accessdenied"
    }
  
    // Update user record with the new password
    db.transaction {
      stack {
        // Lock the account, then revalidate against the current version.
        db.edit user {
          field_name = "id"
          field_value = $auth.id
          data = {updated_at: now}
        }
        db.get user {
          field_name = "id"
          field_value = $auth.id
          output = ["id", "session_version", "password", "account_status"]
        } as $locked_user
        function.run "Security/require_current_session" {
          input = {user_id: $auth.id, extras: $auth.extras, allow_reset: true}
        }
        precondition ($locked_user.account_status == "active") {
          error_type = "unauthorized"
          error = "Não foi possível autorizar a redefinição de senha."
        }
        security.check_password {
          text_password = $input.password
          hash_password = $locked_user.password
        } as $matches_current_password
        precondition ($matches_current_password == false) {
          error_type = "inputerror"
          error = "A nova senha deve ser diferente da senha atual."
        }
        api.lambda {
          code = "return ($var.locked_user.session_version ?? 0) + 1;"
        } as $next_session_version
        db.edit user {
          field_name = "id"
          field_value = $auth.id
          data = {password: $input.password, session_version: $next_session_version}
        } as $user
      }
    }
  
    // Create event log
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "reset_password"
        metadata: {}
      }
    } as $event_log
  }

  response = {
    message: {"success":"true","message":"Password updated"}
  }

  tags = ["xano:quick-start"]
  guid = "uu3mbalHPafTRIy10GtGBdmRrrI"
}
