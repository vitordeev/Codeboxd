query "post-image-uploads" verb=POST {
  api_group = "Codeboxd"
  auth = "user"
  input {
    text operation_key filters=trim|min:32|max:32
    enum operation?="create" { values = ["create", "replace"] }
    int post_id?=0 filters=min:0
    int expected_image_revision?=0 filters=min:0
  }
  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }
    api.lambda {
      code = "return /^[a-f0-9]{32}$/.test($input.operation_key) && (($input.operation === 'create' && $input.post_id === 0 && $input.expected_image_revision === 0) || ($input.operation === 'replace' && $input.post_id > 0));"
    } as $valid_input
    precondition ($valid_input) {
      error_type = "inputerror"
      error = "Operação de imagem inválida."
    }
    var $result { value = null }
    db.transaction {
      stack {
        db.get user {
          field_name = "id"
          field_value = $auth.id
          lock = true
          output = ["id", "account_status", "session_version"]
        } as $actor
        function.run "Security/require_current_session" {
          input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
        }
        precondition ($actor != null && $actor.account_status == "active") {
          error_type = "accessdenied"
          error = "Operação não permitida."
        }
        db.query post_image_asset {
          where = $db.post_image_asset.user_id == $auth.id && $db.post_image_asset.operation_key == $input.operation_key
          return = {type: "single"}
        } as $existing
        conditional {
          if ($existing != null) {
            api.lambda {
              code = "return $var.existing.operation === $input.operation && ($input.operation === 'create' || ($var.existing.post_id || 0) === $input.post_id) && $var.existing.expected_image_revision === $input.expected_image_revision;"
            } as $same_operation
            precondition ($same_operation) {
              error_type = "inputerror"
              error = "A operação pertence a outro contexto."
            }
            var.update $result { value = $existing }
          }
          else {
            precondition ($env.CLOUDINARY_UPLOADS_ENABLED == "true" && $env.CLOUDINARY_POST_IMAGES_CONTRACT_READY == "true" && $env.CLOUDINARY_CLOUD_NAME != null && $env.CLOUDINARY_CLOUD_NAME != "") {
              error_type = "accessdenied"
              error = "Novos uploads externos estão desativados."
            }
            conditional {
              if ($input.operation == "replace") {
                db.get post {
                  field_name = "id"
                  field_value = $input.post_id
                  lock = true
                } as $target
                precondition ($target != null && $target.user_id == $auth.id) {
                  error_type = "notfound"
                  error = "Publicação não encontrada."
                }
                api.lambda {
                  code = "return ($var.target.image_revision || 0) === $input.expected_image_revision;"
                } as $revision_matches
                precondition ($revision_matches) {
                  error_type = "inputerror"
                  error = "A imagem foi alterada. Reabra a publicação."
                }
              }
            }
            security.create_uuid as $resource_uuid
            api.lambda {
              code = "return 'codeboxd/posts/u' + $var.actor.id + '/' + $var.resource_uuid.replace(/-/g, '');"
            } as $public_id
            db.add post_image_asset {
              data = {user_id: $auth.id, post_id: $input.post_id, operation_key: $input.operation_key, operation: $input.operation, state: "reserved", expected_image_revision: $input.expected_image_revision, cloud: $env.CLOUDINARY_CLOUD_NAME, public_id: $public_id, retain_until: null, attempt_count: 0, updated_at: now}
            } as $created
            var.update $result { value = $created }
          }
        }
      }
    }
  }
  response = {contract_version: 1, id: $result.id, user_id: $result.user_id, operation_key: $result.operation_key, operation: $result.operation, post_id: $result.post_id, expected_image_revision: $result.expected_image_revision, state: $result.state, cloud: $result.cloud, public_id: $result.public_id}
  guid = "CBPostImageReserve20261117"
}
