function "PostImages/create_post" {
  input {
    int user_id filters=min:1
    json extras
    int reservation_id filters=min:1
    int version filters=min:1
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
        db.get post_image_asset {
          field_name = "id"
          field_value = $input.reservation_id
          lock = true
        } as $reservation
        precondition ($reservation != null && $reservation.user_id == $input.user_id && $reservation.operation == "create") {
          error_type = "notfound"
          error = "Operação não encontrada."
        }
        conditional {
          if ($reservation.state == "attached") {
            db.get post {
              field_name = "id"
              field_value = $reservation.post_id
            } as $existing
            precondition ($existing != null && $existing.user_id == $input.user_id && $existing.image_asset_record_id == $reservation.id && $existing.image_version == $input.version) {
              error_type = "inputerror"
              error = "Esta operação não pode ser reutilizada."
            }
            var.update $result { value = $existing }
          }
          else {
            precondition ($env.CLOUDINARY_UPLOADS_ENABLED == "true" && $env.CLOUDINARY_POST_IMAGES_CONTRACT_READY == "true") {
              error_type = "accessdenied"
              error = "Novos uploads externos estão desativados."
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
            function.run "PostImages/verify_resource" {
              input = {reservation: $reservation, user_id: $input.user_id, version: $input.version}
            } as $image
            db.add post {
              data = {user_id: $input.user_id, media_id: $input.media_id, body: $input.body, spoiler: $input.spoiler, image_provider: "cloudinary", image_public_id: $image.public_id, image_version: $image.version, image_url: $image.url, image_asset_record_id: $reservation.id, image_revision: 1, updated_at: now}
            } as $created
            db.edit post_image_asset {
              field_name = "id"
              field_value = $reservation.id
              data = {post_id: $created.id, state: "attached", asset_id: $image.asset_id, version: $image.version, format: $image.format, bytes: $image.bytes, width: $image.width, height: $image.height, updated_at: now, retain_until: null, last_error_code: null}
            }
            var.update $result { value = $created }
          }
        }
      }
    }
  }
  response = $result
  guid = "CBPostImageCreatePost20261117"
}
