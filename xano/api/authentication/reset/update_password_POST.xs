// Allows user to update the password in the password reset flow
query "reset/update_password" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text password filters=min:8
    text confirm_password
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: true}
    }

    // Check that the password inputs are matching
    precondition ($input.password == $input.confirm_password) {
      error = "Passwords do not match!"
    }
  
    // Get user record based on the id of the auth token
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $user
  
    // Check that the user record id matches the auth id
    precondition ($user != null && $user.id == $auth.id && $user.account_status != "disabled") {
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
          output = ["id", "session_version"]
        } as $locked_user
        function.run "Security/require_current_session" {
          input = {user_id: $auth.id, extras: $auth.extras, allow_reset: true}
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
