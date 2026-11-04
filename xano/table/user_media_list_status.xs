table user_media_list_status {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    timestamp updated_at?=now
    int user_id { table = "user" }
    int media_id { table = "media" }
    enum status { values = ["watched", "want_to_watch"] }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id", op: "asc"}, {name: "media_id", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}, {name: "status", op: "asc"}, {name: "id", op: "asc"}]}
  ]
  guid = "CBMediaListStatus20261103Tb"
}
