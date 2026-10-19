query "admin/dashboard" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int page?=1 filters=min:1
    int per_page?=6 filters=min:1|max:100
    int reports_page?=1 filters=min:1
    int reports_per_page?=5 filters=min:1|max:100
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status", "role"]
    } as $actor

    precondition ($actor != null && $actor.account_status == "active" && $actor.role == "admin") {
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
      return = {type: "list", paging: {page: $input.reports_page, per_page: $input.reports_per_page, totals: true}}
    } as $pending_reports

    db.query post {
      sort = {post.id: "desc"}
      output = ["id", "user_id", "created_at"]
      return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true}}
    } as $recent_posts
  }

  response = {
    users_total: $users_total
    posts_total: $posts_total
    media_total: $media_total
    reports_pending: $reports_pending
    pending_reports: $pending_reports.items
    recent_posts: $recent_posts.items
    recent_posts_pagination: {
      total: $recent_posts.itemsTotal
      page: $recent_posts.curPage
      next_page: $recent_posts.nextPage
      per_page: $recent_posts.perPage
    }
    pending_reports_pagination: {
      total: $pending_reports.itemsTotal
      page: $pending_reports.curPage
      next_page: $pending_reports.nextPage
      per_page: $pending_reports.perPage
    }
  }
}
