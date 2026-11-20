query "admin/reports/{id}/remove-target" verb=POST {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int id filters=min:1
    text decision filters=trim|min:1|max:2000
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
      error = "Acesso administrativo nao permitido."
    }

    db.transaction {
      stack {
        function.run "Security/require_current_session" {
          input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
        }

        db.get user {
          field_name = "id"
          field_value = $auth.id
          lock = true
          output = ["id", "account_status", "role"]
        } as $locked_actor

        precondition ($locked_actor != null && $locked_actor.account_status == "active" && $locked_actor.role == "admin") {
          error_type = "accessdenied"
          error = "Acesso administrativo nao permitido."
        }

        db.get report {
          field_name = "id"
          field_value = $input.id
          lock = true
          output = ["id", "status", "target_type", "target_id", "target_snapshot"]
        } as $report

        precondition ($report != null && ($report.status == "pending" || $report.status == "reviewing")) {
          error_type = "inputerror"
          error = "Report ausente ou ja finalizado."
        }

        precondition ($report.target_type == "post" || $report.target_type == "media" || $report.target_type == "comment" || $report.target_type == "review") {
          error_type = "accessdenied"
          error = "Este tipo de report nao autoriza remover este alvo."
        }

        var $target_id { value = $report.target_id|to_int }

        precondition ($target_id > 0) {
          error_type = "inputerror"
          error = "Identificador do alvo invalido."
        }

        conditional {
          if ($report.target_type == "post") {
            db.get post {
              field_name = "id"
              field_value = $target_id
              lock = true
              output = ["id", "user_id", "image_asset_record_id"]
            } as $post

            precondition ($post != null) {
              error_type = "notfound"
              error = "Publicacao ausente ou ja removida."
            }

            db.query comment {
              where = $db.comment.post_id == $target_id
              return = {type: "list"}
            } as $comments

            foreach ($comments) {
              each as $child {
                db.del comment {
                  field_name = "id"
                  field_value = $child.id
                }
              }
            }

            db.query post_like {
              where = $db.post_like.post_id == $target_id
              return = {type: "list"}
            } as $likes

            foreach ($likes) {
              each as $child {
                db.del post_like {
                  field_name = "id"
                  field_value = $child.id
                }
              }
            }

            db.del post {
              field_name = "id"
              field_value = $target_id
            }

            conditional {
              if ($post.image_asset_record_id != null && $post.image_asset_record_id > 0) {
                function.run "PostImages/queue_cleanup" {
                  input = {asset_record_id: $post.image_asset_record_id, user_id: $post.user_id, post_id: $post.id, replaced: false}
                }
              }
            }
          }
          else {
            conditional {
              if ($report.target_type == "media") {
                db.get media {
                  field_name = "id"
                  field_value = $target_id
                  lock = true
                  output = ["id", "moderation_hidden"]
                } as $media

                precondition ($media != null && $media.moderation_hidden != true) {
                  error_type = "notfound"
                  error = "Obra ausente ou ja removida."
                }

                db.edit media {
                  field_name = "id"
                  field_value = $target_id
                  data = {moderation_hidden: true}
                }
              }
              else {
                conditional {
                  if ($report.target_type == "comment") {
                    db.get comment {
                      field_name = "id"
                      field_value = $target_id
                      lock = true
                      output = ["id", "post_id", "user_id", "body"]
                    } as $comment

                    precondition ($comment != null) {
                      error_type = "notfound"
                      error = "Comentario ausente ou ja removido."
                    }

                    db.del comment {
                      field_name = "id"
                      field_value = $target_id
                    }
                  }
                  else {
                    db.get user_media_interaction {
                      field_name = "id"
                      field_value = $target_id
                      lock = true
                      output = ["id", "media_id", "rating", "review", "spoiler", "status"]
                    } as $interaction

                    precondition ($interaction != null && (($interaction.rating != null && $interaction.rating > 0) || ($interaction.review != null && $interaction.review != ""))) {
                      error_type = "notfound"
                      error = "Avaliacao ausente ou ja removida."
                    }

                    db.edit user_media_interaction {
                      field_name = "id"
                      field_value = $target_id
                      data = {rating: null, review: null, spoiler: false}
                    }
                  }
                }
              }
            }
          }
        }

        db.edit report {
          field_name = "id"
          field_value = $input.id
          data = {
            status: "resolved"
            reviewer_user_id: $auth.id
            decision: $input.decision
            reviewed_at: now
          }
        }

        db.add event_log {
          data = {
            user_id: $auth.id
            action: "admin_report_target_removed"
            metadata: {
              report_id: $report.id
              target_type: $report.target_type
              target_id: $target_id
              decision: $input.decision
            }
          }
        }
      }
    }
  }

  response = {
    success: true
    report_id: $input.id
    target_type: $report.target_type
    target_id: $target_id
    status: "resolved"
    reviewer_user_id: $auth.id
    decision: $input.decision
  }
  guid = "CBAdminReportRemoveTarget20261118"
}
