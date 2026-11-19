addon search_list_default_count {
 input {
  int user_id
  text? default_key?
 }
 stack {
  db.query user_media_list_status {
   where = $db.user_media_list_status.user_id == $input.user_id && (($input.default_key == ($input.user_id ~ ":planned") && $db.user_media_list_status.status == "want_to_watch") || ($input.default_key == ($input.user_id ~ ":completed") && $db.user_media_list_status.status == "watched"))
   return = {type: "count"}
  }
 }
}
