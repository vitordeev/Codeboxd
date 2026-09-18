table profile {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    text username filters=trim|lower|min:3|max:30
    text display_name filters=trim|min:1|max:80
    text bio? filters=trim|max:1000
    text avatar_url? filters=trim|max:500
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id", op: "asc"}]}
    {type: "btree|unique", field: [{name: "username", op: "asc"}]}
  ]
  guid = "wN6Am20zerXgGOUY-_O3cnrWrC0"
}
