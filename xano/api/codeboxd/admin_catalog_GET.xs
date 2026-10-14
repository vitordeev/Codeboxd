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

    precondition ($actor != null && $actor.account_status == "active" && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso administrativo não permitido."
    }

    db.query media {
      where = $db.media.media_type == $input.media_type && ($input.search == "" || $db.media.title ~ $input.search)
      sort = {media.title: "asc"}
      output = ["itemsReceived", "curPage", "nextPage", "prevPage", "offset", "itemsTotal", "pageTotal", "items.id", "items.identity_key", "items.external_source", "items.external_id", "items.media_type", "items.title", "items.description", "items.cover_url", "items.year"]
      return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, totals: true, metadata: true}}
    } as $catalog
  }

  response = {
    items: $catalog.items
    total: $catalog.itemsTotal
    page: $catalog.curPage
    next_page: $catalog.nextPage
    per_page: $input.per_page
  }
  guid = "yI9z9PqXqahTF-oiKEYk0vb1WxQ"
}
