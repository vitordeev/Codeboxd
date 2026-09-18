table user_media_interaction {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    int media_id { table = "media" }
    text identity_key
    enum status { values = ["planned", "in_progress", "completed", "dropped"] }
    decimal rating?
    text review? filters=trim|max:10000
    bool spoiler?
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "identity_key", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "media_id", op: "asc"}]}
  ]
  guid = "sBGOf2EUfTvt1e2dXvYrxm1D-NA"
}
