function "PostImages/update_post" {
  input {
    int user_id filters=min:1
    json extras
    int post_id filters=min:1
    enum image_action { values = ["replace", "remove"] }
    int expected_image_revision filters=min:0
    int reservation_id?=0 filters=min:0
    int version?=0 filters=min:0
    text body filters=trim|min:1|max:5000
    int media_id?=0
    bool spoiler?=false
  }
  stack {
    var $result { value = null }
    db.transaction {
      stack {
        db.get user {
          field_name = "id"
          field_value = $input.user_id
          lock = true
        } as $actor
        function.run "Security/require_current_session" {
          input = {user_id: $input.user_id, extras: $input.extras, allow_reset: false}
        }
        precondition ($actor != null && $actor.account_status == "active") {
          error_type = "accessdenied"
          error = "Operação não permitida."
        }
        db.get post {
          field_name = "id"
          field_value = $input.post_id
          lock = true
        } as $record
        precondition ($record != null && $record.user_id == $input.user_id) {
          error_type = "notfound"
          error = "Publicação não encontrada."
        }
        var $reservation { value = null }
        conditional {
          if ($input.image_action == "replace") {
            db.get post_image_asset {
              field_name = "id"
              field_value = $input.reservation_id
              lock = true
            } as $replacement
            precondition ($replacement != null && $replacement.user_id == $input.user_id && $replacement.operation == "replace" && $replacement.post_id == $record.id && $replacement.expected_image_revision == $input.expected_image_revision) {
              error_type = "notfound"
              error = "Operação não encontrada."
            }
            var.update $reservation { value = $replacement }
          }
          else {
            precondition ($input.reservation_id == 0 && $input.version == 0) {
              error_type = "inputerror"
              error = "Envio de imagem contraditório."
            }
          }
        }
        conditional {
          if ($reservation != null && $reservation.state == "attached") {
            precondition ($record.image_asset_record_id == $reservation.id && $record.image_version == $input.version) {
              error_type = "inputerror"
              error = "Esta operação não pode ser reutilizada."
            }
            var.update $result { value = $record }
          }
          else {
            api.lambda {
              code = "return ($var.record.image_revision || 0) === $input.expected_image_revision;"
            } as $revision_matches
            precondition ($revision_matches) {
              error_type = "inputerror"
              error = "A imagem foi alterada. Reabra a publicação."
            }
            conditional {
              if ($input.media_id > 0) {
                db.get media {
                  field_name = "id"
                  field_value = $input.media_id
                } as $media
                precondition ($media != null) {
                  error_type = "notfound"
                  error = "Obra não encontrada."
                }
              }
            }
            api.lambda {
              code = "return ($var.record.image_revision || 0) + 1;"
            } as $next_revision
            var $image { value = null }
            conditional {
              if ($input.image_action == "replace") {
                precondition ($env.CLOUDINARY_UPLOADS_ENABLED == "true" && $env.CLOUDINARY_POST_IMAGES_CONTRACT_READY == "true") {
                  error_type = "accessdenied"
                  error = "Novos uploads externos estão desativados."
                }
                function.run "PostImages/verify_resource" {
                  input = {reservation: $reservation, user_id: $input.user_id, version: $input.version}
                } as $image
                db.edit post {
                  field_name = "id"
                  field_value = $record.id
                  data = {body: $input.body, media_id: $input.media_id, spoiler: $input.spoiler, image: null, image_provider: "cloudinary", image_public_id: $image.public_id, image_version: $image.version, image_url: $image.url, image_asset_record_id: $reservation.id, image_revision: $next_revision, updated_at: now}
                } as $result
                db.edit post_image_asset {
                  field_name = "id"
                  field_value = $reservation.id
                  data = {state: "attached", asset_id: $image.asset_id, version: $image.version, format: $image.format, bytes: $image.bytes, width: $image.width, height: $image.height, updated_at: now, retain_until: null, last_error_code: null}
                }
              }
              else {
                db.edit post {
                  field_name = "id"
                  field_value = $record.id
                  data = {body: $input.body, media_id: $input.media_id, spoiler: $input.spoiler, image: null, image_provider: null, image_public_id: null, image_version: null, image_url: null, image_asset_record_id: null, image_revision: $next_revision, updated_at: now}
                } as $result
              }
            }
            conditional {
              if ($record.image_asset_record_id != null && $record.image_asset_record_id > 0) {
                function.run "PostImages/queue_cleanup" {
                  input = {asset_record_id: $record.image_asset_record_id, user_id: $input.user_id, post_id: $record.id, replaced: $input.image_action == "replace"}
                }
              }
            }
          }
        }
      }
    }
  }
  response = $result
  guid = "CBPostImageUpdatePost20261117"
}
