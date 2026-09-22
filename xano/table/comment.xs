table comment {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    int post_id { table = "post" }
    text body filters=trim|min:1|max:2000
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "post_id", op: "asc"}]}
  ]
  guid = "Qd2BP54RE76r3k6uXo4gNZgzbXM"
}
