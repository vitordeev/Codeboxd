function "Lists/set_media_list_status" {
  input {
    int user_id filters=min:1
    int media_id filters=min:1
    enum? status { values = ["watched", "want_to_watch"] }
    enum? expected_status? { values = ["watched", "want_to_watch"] }
    bool conditional_delete?=false
  }
  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
    } as $actor
    precondition ($actor != null && $actor.account_status == "active") {
      error_type = "accessdenied"
      error = "Operação não permitida."
    }
    db.get media {
      field_name = "id"
      field_value = $input.media_id
    } as $media
    precondition ($media != null) {
      error_type = "notfound"
      error = "Obra não encontrada."
    }
    var $result { value = null }
    db.transaction {
      stack {
        db.get user {
          field_name = "id"
          field_value = $input.user_id
          lock = true
        } as $actor_lock
        db.query user_media_list_status {
          where = $db.user_media_list_status.user_id == $input.user_id && $db.user_media_list_status.media_id == $input.media_id
          return = {type: "single"}
        } as $current
        var.update $result { value = $current }
        conditional {
          if ($input.conditional_delete == false || ($current != null && $current.status == $input.expected_status)) {
            conditional {
              if ($input.status == null) {
                conditional {
                  if ($current != null) {
                    db.del user_media_list_status {
                      field_name = "id"
                      field_value = $current.id
                    }
                  }
                }
                var.update $result { value = null }
              }
              else {
                conditional {
                  if ($current != null) {
                    db.edit user_media_list_status {
                      field_name = "id"
                      field_value = $current.id
                      data = {status: $input.status, updated_at: now}
                    } as $result
                  }
                  else {
                    db.add user_media_list_status {
                      data = {user_id: $input.user_id, media_id: $input.media_id, status: $input.status, updated_at: now}
                    } as $result
                  }
                }
                api.lambda {
                  code = "return $input.status === 'watched' ? 'completed' : 'planned';"
                } as $consumption_status
                db.query user_media_interaction {
                  where = $db.user_media_interaction.user_id == $input.user_id && $db.user_media_interaction.media_id == $input.media_id
                  return = {type: "single"}
                } as $interaction
                conditional {
                  if ($interaction != null) {
                    db.edit user_media_interaction {
                      field_name = "id"
                      field_value = $interaction.id
                      data = {status: $consumption_status, updated_at: now}
                    }
                  }
                  else {
                    var $key { value = $input.user_id ~ ":" ~ $input.media_id }
                    db.add user_media_interaction {
                      data = {user_id: $input.user_id, media_id: $input.media_id, identity_key: $key, status: $consumption_status, rating: 0, review: "", spoiler: false, updated_at: now}
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    api.lambda {
      code = "return {user_id: $input.user_id, media_id: $input.media_id, status: $var.result ? $var.result.status : null, item: $var.result};"
    } as $confirmed
  }
  response = $confirmed
  guid = "CBSetMediaListStatus20261103"
}
