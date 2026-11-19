addon search_list_creator {
 input { int user_id }
 stack {
  db.query profile {
   where = $db.profile.user_id == $input.user_id
   output = ["user_id", "username", "display_name", "avatar_url"]
   return = {type: "single"}
  }
 }
}
