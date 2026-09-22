table user_list_item {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int list_id { table = "user_list" }
    int media_id { table = "media" }
    text identity_key
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "identity_key", op: "asc"}]}
    {type: "btree", field: [{name: "list_id", op: "asc"}]}
    {type: "btree", field: [{name: "media_id", op: "asc"}]}
  ]
  guid = "kaSEGORsbygfSS1QwxIc0UnyqZI"
}
