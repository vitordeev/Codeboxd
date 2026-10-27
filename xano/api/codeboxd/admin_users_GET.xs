query "admin/users" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
    text search?="" filters=trim|max:80
    int user_id?=0 filters=min:0
    text account_status?="" filters=trim
    text role?="" filters=trim
    int page?=1 filters=min:1
    int per_page?=25 filters=min:1|max:100
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status", "role"]
    } as $actor

    precondition ($actor != null && $actor.account_status == "active" && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso administrativo não permitido."
    }

    precondition ($input.account_status == "" || $input.account_status == "active" || $input.account_status == "disabled") {
      error_type = "inputerror"
      error = "Estado de conta inválido."
    }

    precondition ($input.role == "" || $input.role == "admin" || $input.role == "moderator" || $input.role == "member") {
      error_type = "inputerror"
      error = "Papel inválido."
    }

    var $users { value = null }

    api.lambda {
      code = "return $input.search.replace(/[\\\\%_]/g, '\\\\$&');"
    } as $search_literal

    conditional {
      if ($input.user_id > 0) {
        db.query user {
          where = $db.user.id == $input.user_id && ($input.account_status == "" || $db.user.account_status == $input.account_status) && ($input.role == "" || $db.user.role == $input.role)
          sort = {user.id: "asc"}
          output = ["itemsReceived", "curPage", "nextPage", "prevPage", "offset", "itemsTotal", "pageTotal", "items.id", "items.username", "items.name", "items.role", "items.account_status", "items.created_at"]
          return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true, metadata: true}}
        } as $users_by_id
        var.update $users { value = $users_by_id }
      }
      elseif ($input.search != "") {
        db.query user {
          where = $db.user.username includes $search_literal && ($input.account_status == "" || $db.user.account_status == $input.account_status) && ($input.role == "" || $db.user.role == $input.role) || $db.user.name includes $search_literal && ($input.account_status == "" || $db.user.account_status == $input.account_status) && ($input.role == "" || $db.user.role == $input.role)
          sort = {user.id: "asc"}
          output = ["itemsReceived", "curPage", "nextPage", "prevPage", "offset", "itemsTotal", "pageTotal", "items.id", "items.username", "items.name", "items.role", "items.account_status", "items.created_at"]
          return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true, metadata: true}}
        } as $users_by_text
        var.update $users { value = $users_by_text }
      }
      else {
        db.query user {
          where = $db.user.id > 0 && ($input.account_status == "" || $db.user.account_status == $input.account_status) && ($input.role == "" || $db.user.role == $input.role)
          sort = {user.id: "asc"}
          output = ["itemsReceived", "curPage", "nextPage", "prevPage", "offset", "itemsTotal", "pageTotal", "items.id", "items.username", "items.name", "items.role", "items.account_status", "items.created_at"]
          return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true, metadata: true}}
        } as $users_unfiltered
        var.update $users { value = $users_unfiltered }
      }
    }
  }

  response = {
    items: $users.items
    total: $users.itemsTotal
    page: $users.curPage
    next_page: $users.nextPage
    per_page: $input.per_page
  }
  guid = "09BI7xyc2hNxuSEMu2PQqgRvtY4"
}
