query "admin/post-image-cleanup-candidates" verb=GET {
  api_group = "Codeboxd"
  auth = "user"

  input {
    int per_page?=10 filters=min:1|max:10
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
      error = "Acesso administrativo não permitido."
    }

    db.query post_image_asset {
      where = $db.post_image_asset.state == "cleanup_pending" && $db.post_image_asset.retain_until != null && $db.post_image_asset.retain_until <= now
      sort = {post_image_asset.retain_until: "asc", post_image_asset.id: "asc"}
      return = {type: "list", paging: {page: 1, per_page: $input.per_page, metadata: false}}
    } as $candidates

    var $records { value = [] }
    var $record { value = null }
    foreach ($candidates) {
      each as $asset {
        db.query post {
          where = $db.post.image_asset_record_id == $asset.id
          return = {type: "count"}
        } as $references

        var.update $record {
          value = {
            id: $asset.id
            user_id: $asset.user_id
            post_id: $asset.post_id
            state: $asset.state
            cloud: $asset.cloud
            public_id: $asset.public_id
            asset_id: $asset.asset_id
            version: $asset.version
            format: $asset.format
            bytes: $asset.bytes
            width: $asset.width
            height: $asset.height
            retain_until: $asset.retain_until
            reference_count: $references
          }
        }

        var.update $records { value = $records|push:$record }
      }
    }
  }

  response = {contract_version: 1, fetched_at: now, records: $records}
  guid = "CBPostImageCleanupCandidates20261119"
}
