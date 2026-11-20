query "admin/post-image-cleanup/{id}/claim" verb=POST {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int id filters=min:1
    int user_id filters=min:1
    int post_id filters=min:1
    text cloud filters=trim|min:1|max:80
    text public_id filters=trim|min:1|max:200
    text asset_id filters=trim|min:1|max:200
    int version filters=min:1
    text approval_sha256 filters=trim|min:64|max:64
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

    api.lambda {
      code = "return /^[a-f0-9]{64}$/.test($input.approval_sha256) && $input.cloud === $env.CLOUDINARY_CLOUD_NAME && new RegExp('^codeboxd/posts/u' + $input.user_id + '/[a-f0-9]{32}$').test($input.public_id);"
    } as $valid_identity

    precondition ($valid_identity) {
      error_type = "inputerror"
      error = "A identidade aprovada para limpeza é inválida."
    }

    var $claimed { value = null }
    db.transaction {
      stack {
        db.get user {
          field_name = "id"
          field_value = $auth.id
          lock = true
          output = ["id", "account_status", "role"]
        } as $actor

        function.run "Security/require_current_session" {
          input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
        }

        precondition ($actor != null && $actor.account_status == "active" && $actor.role == "admin") {
          error_type = "accessdenied"
          error = "Acesso administrativo não permitido."
        }

        db.get post_image_asset {
          field_name = "id"
          field_value = $input.id
          lock = true
        } as $asset

        precondition ($asset != null && $asset.state == "cleanup_pending" && $asset.user_id == $input.user_id && $asset.post_id == $input.post_id && $asset.cloud == $input.cloud && $asset.public_id == $input.public_id && $asset.asset_id == $input.asset_id && $asset.version == $input.version && $asset.retain_until != null && $asset.retain_until <= now) {
          error_type = "inputerror"
          error = "O candidato mudou desde a prévia aprovada."
        }

        db.query post {
          where = $db.post.image_asset_record_id == $asset.id
          return = {type: "count"}
        } as $references

        precondition ($references == 0) {
          error_type = "inputerror"
          error = "O asset ainda está vinculado a uma publicação."
        }

        db.edit post_image_asset {
          field_name = "id"
          field_value = $asset.id
          data = {state: "reconciliation_required", attempt_count: $asset.attempt_count + 1, last_error_code: "cleanup_started:" ~ $input.approval_sha256, updated_at: now}
        } as $claimed
      }
    }
  }

  response = {contract_version: 1, id: $claimed.id, user_id: $claimed.user_id, post_id: $claimed.post_id, state: $claimed.state, cloud: $claimed.cloud, public_id: $claimed.public_id, asset_id: $claimed.asset_id, version: $claimed.version, format: $claimed.format, bytes: $claimed.bytes, width: $claimed.width, height: $claimed.height, attempt_count: $claimed.attempt_count, approval_sha256: $input.approval_sha256}
  guid = "CBPostImageCleanupClaim20261119"
}
