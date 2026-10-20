// Local candidate only. Publish and validate separately before enabling the app flag.
query "library" verb=GET {
  api_group = "Codeboxd"
  auth = "user"
  input {
    int after_id?=0 filters=min:0
  }
  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_status"]
    } as $actor
    precondition ($actor != null && $actor.account_status != "disabled") {
      error_type = "accessdenied"
      error = "Operação não permitida."
    }
    db.query user_media_interaction {
      join = {media: {table: "media", where: $db.user_media_interaction.media_id == $db.media.id}}
      where = $db.user_media_interaction.user_id == $auth.id && $db.user_media_interaction.id > $input.after_id
      sort = {user_media_interaction.id: "asc"}
      eval = {media_title: $db.media.title, media_type: $db.media.media_type, media_cover_url: $db.media.cover_url, media_year: $db.media.year}
      return = {type: "list", paging: {page: 1, per_page: 21, metadata: false}}
      output = ["id", "user_id", "media_id", "status", "rating", "review", "spoiler", "media_title", "media_type", "media_cover_url", "media_year"]
    } as $rows
  }
  response = {items: $rows|slice:0:20, has_more: ($rows|count) > 20}
  guid = "SgsdYaGY1jNwlmBSFlfy2go-A7k"
}
