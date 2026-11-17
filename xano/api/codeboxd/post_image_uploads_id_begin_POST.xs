query "post-image-uploads/{id}/begin" verb=POST {
  api_group = "Codeboxd"
  auth = "user"
  input {
    int id filters=min:1
  }
  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }
    db.transaction {
      stack {
        db.get user {
          field_name = "id"
          field_value = $auth.id
          lock = true
        } as $actor
        function.run "Security/require_current_session" {
          input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
        }
        precondition ($actor != null && $actor.account_status == "active" && $env.CLOUDINARY_UPLOADS_ENABLED == "true" && $env.CLOUDINARY_POST_IMAGES_CONTRACT_READY == "true") {
          error_type = "accessdenied"
          error = "Novos uploads externos estão desativados."
        }
        db.get post_image_asset {
          field_name = "id"
          field_value = $input.id
          lock = true
        } as $reservation
        precondition ($reservation != null && $reservation.user_id == $auth.id) {
          error_type = "notfound"
          error = "Operação não encontrada."
        }
        precondition ($reservation.state == "reserved" && $reservation.attempt_count == 0) {
          error_type = "inputerror"
          error = "O envio já foi iniciado. Consulte a operação antes de tentar novamente."
        }
        db.edit post_image_asset {
          field_name = "id"
          field_value = $reservation.id
          data = {state: "reconciliation_required", attempt_count: 1, updated_at: now}
        }
      }
    }
  }
  response = {contract_version: 1, id: $input.id, upload_granted: true}
  guid = "CBPostImageBegin20261117"
}
