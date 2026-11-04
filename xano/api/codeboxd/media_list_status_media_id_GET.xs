query "media-list-status/{media_id}" verb=GET {
  api_group = "Codeboxd"
  auth = "user"
  input {
    int media_id filters=min:1
  }
  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }
    db.get media {
      field_name = "id"
      field_value = $input.media_id
    } as $media
    precondition ($media != null) {
      error_type = "notfound"
      error = "Obra não encontrada."
    }
    db.query user_media_list_status {
      where = $db.user_media_list_status.user_id == $auth.id && $db.user_media_list_status.media_id == $input.media_id
      return = {type: "single"}
    } as $row
    api.lambda {
      code = "return {user_id: $auth.id, media_id: $input.media_id, status: $var.row ? $var.row.status : null};"
    } as $result
  }
  response = $result
  guid = "CBGetMediaListStatus20261103"
}
