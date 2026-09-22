table post_like {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int user_id { table = "user" }
    int post_id { table = "post" }
    text identity_key
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "identity_key", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "post_id", op: "asc"}]}
  ]
  guid = "-FhSLkT3XHQve3TV6vZl9xt-lso"
}
