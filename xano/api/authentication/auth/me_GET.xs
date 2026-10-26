// Get the user record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

    // Get the user record based on the auth ID
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email", "role", "username", "account_status"]
    } as $user
  
    precondition ($user.account_status != "disabled") {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
    // Create an event log for get user record
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "get_auth_user"
        metadata: {}
      }
    } as $event_log
  }

  response = $user
  tags = ["xano:quick-start"]
  guid = "K0J82VGROn2aGHYNGmG9X7cmH1M"
}