query "admin/users" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
    text search filters=trim|min:1|max:80
    int user_id?=0 filters=min:0
    text account_status?="" filters=trim
    text role?="" filters=trim
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

    precondition ($input.account_status == "" || $input.account_status == "active" || $input.account_status == "disabled") {
      error_type = "inputerror"
      error = "Estado de conta inválido."
    }

    precondition ($input.role == "" || $input.role == "admin" || $input.role == "moderator" || $input.role == "member") {
      error_type = "inputerror"
      error = "Papel inválido."
    }

    db.query user {
      where = (($input.user_id > 0 && $db.user.id == $input.user_id) || (($db.user.username|to_lower) ~ ($input.search|to_lower)) || (($db.user.name|to_lower) ~ ($input.search|to_lower))) && ($input.account_status == "" || $db.user.account_status == $input.account_status) && ($input.role == "" || $db.user.role == $input.role)
      sort = {user.id: "asc"}
      output = ["id", "username", "name", "role", "account_status", "created_at"]
      return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true}}
    } as $users
  }

  response = {
    items: $users.items
    total: $users.itemsTotal
    page: $users.curPage
    next_page: $users.nextPage
    per_page: $users.perPage
  }
}
