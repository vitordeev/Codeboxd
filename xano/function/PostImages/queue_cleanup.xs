function "PostImages/queue_cleanup" {
  input {
    int asset_record_id filters=min:1
    int user_id filters=min:1
    int post_id filters=min:1
    bool replaced?=false
  }
  stack {
    db.get post_image_asset {
      field_name = "id"
      field_value = $input.asset_record_id
      lock = true
    } as $asset
    precondition ($asset != null && $asset.user_id == $input.user_id && $asset.post_id == $input.post_id && $asset.state == "attached") {
      error_type = "inputerror"
      error = "O vínculo da imagem não pôde ser confirmado."
    }
    db.query post {
      where = $db.post.image_asset_record_id == $asset.id
      return = {type: "count"}
    } as $references
    precondition ($references == 0) {
      error_type = "inputerror"
      error = "A imagem ainda está vinculada a uma publicação."
    }
    var $retain_until { value = now }
    conditional {
      if ($input.replaced) {
        var.update $retain_until { value = now|add_secs_to_timestamp:86400 }
      }
    }
    db.edit post_image_asset {
      field_name = "id"
      field_value = $asset.id
      data = {state: "cleanup_pending", retain_until: $retain_until, updated_at: now}
    }
  }
  response = null
  guid = "CBPostImageQueueCleanup20261117"
}
