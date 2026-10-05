query "admin/catalog/{id}" verb=PUT {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int id
    text title filters=trim|min:1|max:500
    text description? filters=max:20000
    text cover_url? filters=trim|max:1000
    int year? filters=min:1800|max:2200
  }

  stack {
    api.lambda {
      code = "if (!($input.cover_url || '')) return true; try { const u = new URL($input.cover_url); return u.protocol === 'https:' && !!u.hostname && !u.username && !u.password; } catch { return false; }"
    } as $valid_cover

    precondition ($valid_cover) {
      error_type = "inputerror"
      error = "A capa deve usar uma URL HTTPS válida."
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status", "role"]
    } as $actor

    precondition ($actor != null && $actor.account_status != "disabled" && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso administrativo não permitido."
    }

    db.get media {
      field_name = "id"
      field_value = $input.id
      output = ["id", "identity_key", "external_source", "external_id", "media_type"]
    } as $existing

    precondition ($existing != null) {
      error_type = "notfound"
      error = "Obra não encontrada."
    }

    db.edit media {
      field_name = "id"
      field_value = $input.id
      data = {
        title: $input.title
        description: $input.description
        cover_url: $input.cover_url
        year: $input.year
      }
    } as $updated
  }

  response = {
    id: $updated.id
    title: $updated.title
    description: $updated.description
    cover_url: $updated.cover_url
    year: $updated.year
    media_type: $existing.media_type
  }
}
