query "admin/post-image-cleanup/{id}/result" verb=POST {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int id filters=min:1
    text approval_sha256 filters=trim|min:64|max:64
    enum result { values = ["deleted", "uncertain"] }
  }

  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }

    api.lambda {
      code = "return /^[a-f0-9]{64}$/.test($input.approval_sha256);"
    } as $valid_approval

    precondition ($valid_approval) {
      error_type = "inputerror"
      error = "A referência da aprovação é inválida."
    }

    var $result_record { value = null }
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

        precondition ($asset != null && $asset.state == "reconciliation_required" && $asset.last_error_code == ("cleanup_started:" ~ $input.approval_sha256)) {
          error_type = "inputerror"
          error = "O resultado não corresponde a uma limpeza reivindicada."
        }

        var $next_state { value = "reconciliation_required" }
        var $next_code { value = "cleanup_wait:" ~ $input.approval_sha256 }
        conditional {
          if ($input.result == "deleted") {
            var.update $next_state { value = "deleted" }
            var.update $next_code { value = "cleanup_ok:" ~ $input.approval_sha256 }
          }
        }

        db.edit post_image_asset {
          field_name = "id"
          field_value = $asset.id
          data = {state: $next_state, last_error_code: $next_code, updated_at: now}
        } as $result_record
      }
    }
  }

  response = {contract_version: 1, id: $result_record.id, state: $result_record.state, attempt_count: $result_record.attempt_count}
  guid = "CBPostImageCleanupResult20261119"
}
