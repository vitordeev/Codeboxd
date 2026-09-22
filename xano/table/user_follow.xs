table user_follow {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int follower_id { table = "user" }
    int followed_id { table = "user" }
    text identity_key
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "identity_key", op: "asc"}]}
    {type: "btree", field: [{name: "follower_id", op: "asc"}]}
    {type: "btree", field: [{name: "followed_id", op: "asc"}]}
  ]
  guid = "wYJHo0D4wsicF6vK9g4OP0azRRU"
}
