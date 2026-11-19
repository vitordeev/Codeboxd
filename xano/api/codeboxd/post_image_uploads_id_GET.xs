query "post-image-uploads/{id}" verb=GET {
  api_group = "Codeboxd"
  auth = "user"
  input {
    int id filters=min:1
  }
  stack {
    function.run "Security/require_current_session" {
      input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
    }
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status"]
    } as $actor
    precondition ($actor != null && $actor.account_status == "active") {
      error_type = "accessdenied"
      error = "Operação não permitida."
    }
    db.get post_image_asset {
      field_name = "id"
      field_value = $input.id
      output = ["id", "user_id", "post_id", "operation_key", "operation", "expected_image_revision", "state", "cloud", "public_id"]
    } as $result
    precondition ($result != null && $result.user_id == $auth.id) {
      error_type = "notfound"
      error = "Operação não encontrada."
    }
  }
  response = {contract_version: 1, id: $result.id, user_id: $result.user_id, operation_key: $result.operation_key, operation: $result.operation, post_id: $result.post_id, expected_image_revision: $result.expected_image_revision, state: $result.state, cloud: $result.cloud, public_id: $result.public_id}
  guid = "CBPostImageReadReserve20261117"
}
