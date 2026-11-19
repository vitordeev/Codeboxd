addon search_list_custom_count {
 input { int list_id }
 stack {
  db.query user_list_item {
   where = $db.user_list_item.list_id == $input.list_id
   return = {type: "count"}
  }
 }
}
