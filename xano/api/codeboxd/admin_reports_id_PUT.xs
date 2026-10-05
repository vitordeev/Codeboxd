query "admin/reports/{id}" verb=PUT {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int id
    enum status { values = ["reviewing", "resolved", "rejected"] }
    text decision filters=trim|min:1|max:2000
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

    db.get report {
      field_name = "id"
      field_value = $input.id
      output = ["id", "status", "target_type", "target_id"]
    } as $current

    precondition ($current != null) {
      error_type = "notfound"
      error = "Report não encontrado."
    }

    db.transaction {
      stack {
        db.edit report {
          field_name = "id"
          field_value = $input.id
          data = {
            status: $input.status
            reviewer_user_id: $auth.id
            decision: $input.decision
            reviewed_at: now
          }
        }

        db.add event_log {
          data = {
            user_id: $auth.id
            action: "admin_report_status_changed"
            metadata: {
              report_id: $input.id
              target_type: $current.target_type
              target_id: $current.target_id
              previous_status: $current.status
              new_status: $input.status
              decision: $input.decision
            }
          }
        }
      }
    }
  }

  response = {
    success: true
    report_id: $input.id
    previous_status: $current.status
    status: $input.status
    reviewer_user_id: $auth.id
    decision: $input.decision
  }
}
