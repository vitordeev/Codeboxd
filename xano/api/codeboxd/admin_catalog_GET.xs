query "admin/catalog" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
    enum media_type { values = ["movie", "series", "anime", "book"] }
    text search?="" filters=trim|max:120
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

    db.query media {
      where = $db.media.media_type == $input.media_type && ($input.search == "" || (($db.media.title|to_lower) ~ ($input.search|to_lower)))
      sort = {media.title: "asc"}
      output = ["id", "identity_key", "external_source", "external_id", "media_type", "title", "description", "cover_url", "year"]
      return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true}}
    } as $catalog
  }

  response = {
    items: $catalog.items
    total: $catalog.itemsTotal
    page: $catalog.curPage
    next_page: $catalog.nextPage
    per_page: $catalog.perPage
  }
}
