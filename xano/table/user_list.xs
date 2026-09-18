table user_list {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    text title filters=trim|min:1|max:120
    text description? filters=trim|max:2000
    bool is_public?=true
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]
  guid = "9VYvnA6iqkXTs0IWM26qVjsJRk0"
}
