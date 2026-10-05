query "admin/dashboard" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

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

    db.query user {
      return = {type: "count"}
    } as $users_total

    db.query post {
      return = {type: "count"}
    } as $posts_total

    db.query media {
      return = {type: "count"}
    } as $media_total

    db.query report {
      where = $db.report.status == "pending"
      return = {type: "count"}
    } as $reports_pending

    db.query report {
      where = $db.report.status == "pending"
      sort = {report.created_at: "desc"}
      output = ["id", "created_at", "target_type", "reason"]
      return = {type: "list", paging: {page: 1, per_page: 5, metadata: false}}
    } as $pending_reports

    db.query post {
      sort = {post.id: "desc"}
      output = ["id", "user_id", "created_at"]
      return = {type: "list", paging: {page: 1, per_page: 6, metadata: false}}
    } as $recent_posts
  }

  response = {
    users_total: $users_total
    posts_total: $posts_total
    media_total: $media_total
    reports_pending: $reports_pending
    pending_reports: $pending_reports
    recent_posts: $recent_posts
  }
}
