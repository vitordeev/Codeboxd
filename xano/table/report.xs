table report {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int reporter_user_id { table = "user" }
    enum target_type { values = ["message", "post", "comment", "profile", "media"] }
    text target_id filters=trim|min:1|max:120
    enum reason { values = ["spam", "harassment", "inappropriate", "other"] }
    text description? filters=trim|max:2000
    json target_snapshot?
    enum status?="pending" { values = ["pending", "reviewing", "resolved", "rejected"] }
    int reviewer_user_id? { table = "user" }
    text decision? filters=trim|max:2000
    timestamp reviewed_at?
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "status", op: "asc"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "reporter_user_id", op: "asc"}]}
    {type: "btree", field: [{name: "target_type", op: "asc"}, {name: "target_id", op: "asc"}]}
  ]
}
