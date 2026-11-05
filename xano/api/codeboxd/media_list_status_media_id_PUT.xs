query "media-list-status/{media_id}" verb=PUT {
  api_group = "Codeboxd"
  auth = "user"
  input {
    int media_id filters=min:1
    enum? status { values = ["watched", "want_to_watch"] }
  }
  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }
    function.run "Lists/set_media_list_status" {
      input = {user_id: $auth.id, media_id: $input.media_id, status: $input.status}
    } as $confirmed
    api.lambda {
      code = "return {user_id: $var.confirmed.user_id, media_id: $var.confirmed.media_id, status: $var.confirmed.status};"
    } as $result
  }
  response = $result
  guid = "CBPutMediaListStatus20261103"
}
