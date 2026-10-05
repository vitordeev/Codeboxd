query "reports" verb=POST {
  api_group = "Codeboxd"
  auth = "user"

  input {
    enum target_type { values = ["message", "post", "comment", "profile", "media"] }
    text target_id filters=trim|min:1|max:120
    enum reason { values = ["spam", "harassment", "inappropriate", "other"] }
    text description? filters=trim|max:2000
    json target_snapshot?
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status"]
    } as $actor

    precondition ($actor != null && $actor.account_status != "disabled") {
      error_type = "accessdenied"
      error = "Operação não permitida."
    }

    var $numeric_target_id {
      value = $input.target_id|to_int
    }

    conditional {
      if ($input.target_type == "message") {
        api.lambda {
          code = "const s = $input.target_snapshot; if (!s || typeof s !== 'object' || Array.isArray(s) || !String(s.body || '').trim()) return false; return {body: String(s.body || '').slice(0, 2000), sender_name: String(s.sender_name || '').slice(0, 80), sent_at: String(s.sent_at || '').slice(0, 40)};"
        } as $safe_snapshot

        precondition ($safe_snapshot != false) {
          error_type = "inputerror"
          error = "O contexto mínimo da mensagem é obrigatório."
        }
      }
      else {
        conditional {
          if ($input.target_type == "post") {
            precondition ($numeric_target_id > 0) {
              error_type = "inputerror"
              error = "Identificador de publicação inválido."
            }
            db.get post {
              field_name = "id"
              field_value = $numeric_target_id
              output = ["id", "user_id", "body", "spoiler", "created_at"]
            } as $target
            precondition ($target != null) {
              error_type = "notfound"
              error = "Publicação não encontrada."
            }
            var $safe_snapshot {
              value = {body: $target.body, spoiler: $target.spoiler, created_at: $target.created_at}
            }
          }
          else {
            conditional {
              if ($input.target_type == "comment") {
                precondition ($numeric_target_id > 0) {
                  error_type = "inputerror"
                  error = "Identificador de comentário inválido."
                }
                db.get comment {
                  field_name = "id"
                  field_value = $numeric_target_id
                  output = ["id", "user_id", "post_id", "body", "created_at"]
                } as $target
                precondition ($target != null) {
                  error_type = "notfound"
                  error = "Comentário não encontrado."
                }
                var $safe_snapshot {
                  value = {body: $target.body, post_id: $target.post_id, created_at: $target.created_at}
                }
              }
              else {
                conditional {
                  if ($input.target_type == "profile") {
                    precondition ($numeric_target_id > 0) {
                      error_type = "inputerror"
                      error = "Identificador de perfil inválido."
                    }
                    db.get profile {
                      field_name = "user_id"
                      field_value = $numeric_target_id
                      output = ["user_id", "username", "display_name", "bio"]
                    } as $target
                    precondition ($target != null) {
                      error_type = "notfound"
                      error = "Perfil não encontrado."
                    }
                    var $safe_snapshot {
                      value = {username: $target.username, display_name: $target.display_name, bio: $target.bio}
                    }
                  }
                  else {
                    precondition ($numeric_target_id > 0) {
                      error_type = "inputerror"
                      error = "Identificador de obra inválido."
                    }
                    db.get media {
                      field_name = "id"
                      field_value = $numeric_target_id
                      output = ["id", "media_type", "title", "year"]
                    } as $target
                    precondition ($target != null) {
                      error_type = "notfound"
                      error = "Obra não encontrada."
                    }
                    var $safe_snapshot {
                      value = {media_type: $target.media_type, title: $target.title, year: $target.year}
                    }
                  }
                }
              }
            }
          }
        }
      }
    }

    db.add report {
      data = {
        reporter_user_id: $auth.id
        target_type: $input.target_type
        target_id: $input.target_id
        reason: $input.reason
        description: $input.description
        target_snapshot: $safe_snapshot
        status: "pending"
      }
    } as $created
  }

  response = {id: $created.id, status: $created.status}
}
