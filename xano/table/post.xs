table post {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    int media_id? { table = "media" }
    text body filters=trim|min:1|max:5000
    bool spoiler?
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "media_id", op: "asc"}]}
  ]
  guid = "yj4R8prcVHksFpDqZrhTa7L6j3g"
}
