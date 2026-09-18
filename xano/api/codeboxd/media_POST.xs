query "media" verb=POST {
 api_group = "Codeboxd"
 auth = "user"
 input {
text external_source filters=trim|min:1|max:40
text external_id filters=trim|min:1|max:100
enum media_type { values = ["movie", "series", "anime", "book"] }
text title filters=trim|min:1|max:500
text description? filters=max:20000
text cover_url? filters=trim|max:1000
int year?
json details?
 }
 stack {
api.lambda {
 code = "const i = $input; const valid = (i.external_source === 'tmdb' && ['movie','series'].includes(i.media_type) && /^[0-9]+$/.test(i.external_id)) || (i.external_source === 'jikan' && i.media_type === 'anime' && /^[0-9]+$/.test(i.external_id)) || (i.external_source === 'openlibrary' && i.media_type === 'book' && /^OL[0-9]+W$/.test(i.external_id)); if (!valid) return false; if (!i.cover_url) return true; try { const u = new URL(i.cover_url); return u.protocol === 'https:' && !!u.hostname && !u.username && !u.password; } catch { return false; }"
} as $valid_media
precondition ($valid_media) {
 error_type = "inputerror"
 error = "Identidade externa ou URL invalida."
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
var $key { value = $input.external_source ~ ":" ~ $input.media_type ~ ":" ~ $input.external_id }
db.get media {
 field_name = "identity_key"
 field_value = $key
} as $existing
conditional {
 if ($existing == null) {
db.add media {
 data = {identity_key: $key, external_source: $input.external_source, external_id: $input.external_id, media_type: $input.media_type, title: $input.title, description: $input.description, cover_url: $input.cover_url, year: $input.year, details: $input.details}
} as $result
 }
 else {
 var $result { value = $existing }
 }
}
 }
 response = $result
 guid = "woRdxNUnhDu93EQnbzi1v4ro0pg"
}
