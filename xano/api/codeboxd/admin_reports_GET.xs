query "admin/reports" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
    text status?="" filters=trim
    text target_type?="" filters=trim
    text reason?="" filters=trim
    int page?=1 filters=min:1
    int per_page?=25 filters=min:1|max:100
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

    precondition ($input.status == "" || $input.status == "pending" || $input.status == "reviewing" || $input.status == "resolved" || $input.status == "rejected") {
      error_type = "inputerror"
      error = "Estado de report inválido."
    }

    precondition ($input.target_type == "" || $input.target_type == "message" || $input.target_type == "post" || $input.target_type == "comment" || $input.target_type == "profile" || $input.target_type == "media") {
      error_type = "inputerror"
      error = "Tipo de alvo inválido."
    }

    precondition ($input.reason == "" || $input.reason == "spam" || $input.reason == "harassment" || $input.reason == "inappropriate" || $input.reason == "other") {
      error_type = "inputerror"
      error = "Motivo inválido."
    }

    db.query report {
      where = ($input.status == "" || $db.report.status == $input.status) && ($input.target_type == "" || $db.report.target_type == $input.target_type) && ($input.reason == "" || $db.report.reason == $input.reason)
      sort = {report.created_at: "desc"}
      output = ["id", "created_at", "reporter_user_id", "target_type", "target_id", "reason", "description", "target_snapshot", "status", "reviewer_user_id", "decision", "reviewed_at"]
      return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true}}
    } as $reports
  }

  response = {
    items: $reports.items
    total: $reports.itemsTotal
    page: $reports.curPage
    next_page: $reports.nextPage
    per_page: $reports.perPage
  }
}
