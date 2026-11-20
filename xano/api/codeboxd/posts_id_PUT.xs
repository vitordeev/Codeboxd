query "posts/{id}" verb=PUT {
 api_group = "Codeboxd"
 auth = "user"
 input {
int id
text body filters=trim|min:1|max:5000
int media_id?=0
bool spoiler?=false
image image?
file image_upload?
enum image_action?="keep" { values = ["keep", "replace", "remove"] }
int image_reservation_id?=0 filters=min:0
int image_version?=0 filters=min:0
int expected_image_revision?=0 filters=min:0
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
precondition ($actor != null && $actor.account_status != "disabled") {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
db.get post {
 field_name = "id"
 field_value = $input.id
} as $record
precondition ($record != null) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
precondition ($record.user_id == $auth.id) {
  error_type = "accessdenied"
  error = "Operação não permitida."
}
conditional {
 if ($input.media_id > 0) {
db.get media {
 field_name = "id"
 field_value = $input.media_id
} as $media
precondition ($media != null && $media.moderation_hidden != true) {
  error_type = "notfound"
  error = "Registro não encontrado."
}
}}
precondition (($input.image_action == "keep" && $input.image_reservation_id == 0 && $input.image_version == 0 && ($record.image_provider != "cloudinary" || ($input.image_upload == null && $input.image == null))) || ($input.image_action != "keep" && $input.image_upload == null && $input.image == null)) {
 error_type = "inputerror"
 error = "Envio de imagem contraditório."
}
conditional {
 if ($input.image_action != "keep") {
  function.run "PostImages/update_post" {
   input = {user_id: $auth.id, extras: $auth.extras, post_id: $input.id, image_action: $input.image_action, expected_image_revision: $input.expected_image_revision, reservation_id: $input.image_reservation_id, version: $input.image_version, body: $input.body, media_id: $input.media_id, spoiler: $input.spoiler}
  } as $result
 }
 else {
db.transaction {
 stack {
db.get user {
 field_name = "id"
 field_value = $auth.id
 lock = true
} as $legacy_actor
function.run "Security/require_current_session" {
 input = {user_id: $auth.id, extras: $auth.extras, allow_reset: false}
}
precondition ($legacy_actor != null && $legacy_actor.account_status == "active") {
 error_type = "accessdenied"
 error = "Operação não permitida."
}
db.get post {
 field_name = "id"
 field_value = $input.id
 lock = true
} as $record
precondition ($record != null && $record.user_id == $auth.id && ($record.image_provider != "cloudinary" || ($input.image_upload == null && $input.image == null))) {
 error_type = "accessdenied"
 error = "A publicação mudou. Reabra o editor."
}
api.lambda {
 code = "return ($var.record.image_revision || 0) + 1;"
} as $legacy_next_revision
conditional {
 if ($input.image_upload != null) {
storage.create_image {
 access = "public"
 value = $input.image_upload
 filename = ""
} as $post_image
 }
 else {
var $post_image { value = $input.image }
 }
}
conditional {
 if ($post_image != null) {
db.edit post {
 field_name = "id"
 field_value = $input.id
 data = {body: $input.body, media_id: $input.media_id, image: $post_image, image_revision: $legacy_next_revision, spoiler: $input.spoiler, updated_at: now}
} as $result
 }
}
conditional {
 if ($post_image == null) {
db.edit post {
 field_name = "id"
 field_value = $input.id
 data = {body: $input.body, media_id: $input.media_id, spoiler: $input.spoiler, updated_at: now}
} as $result
 }
}
 }
}
 }
}
 }
 response = $result
 guid = "qe--qlzGinsokmakSyTWuKE18eo"
}
