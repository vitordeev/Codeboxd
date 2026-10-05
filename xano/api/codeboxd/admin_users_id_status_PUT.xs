query "admin/users/{id}/status" verb=PUT {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int id
    enum account_status { values = ["active", "disabled"] }
    text reason? filters=trim|max:500
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status", "role"]
    } as $actor

    precondition ($actor != null && $actor.account_status != "disabled" && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso administrativo não permitido."
    }

    db.get user {
      field_name = "id"
      field_value = $input.id
      output = ["id", "account_status"]
    } as $target

    precondition ($target != null) {
      error_type = "notfound"
      error = "Conta não encontrada."
    }

    db.transaction {
      stack {
        db.edit user {
          field_name = "id"
          field_value = $input.id
          data = {account_status: $input.account_status, updated_at: now}
        }

        db.add event_log {
          data = {
            user_id: $auth.id
            action: "admin_account_status_changed"
            metadata: {
              target_user_id: $input.id
              previous_status: $target.account_status
              new_status: $input.account_status
              reason: $input.reason
            }
          }
        }
      }
    }
  }

  response = {
    success: true
    user_id: $input.id
    previous_status: $target.account_status
    account_status: $input.account_status
  }
}
