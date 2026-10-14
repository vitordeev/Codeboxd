// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1

    // The role of the user within their company (e.g., 'admin', 'member').
    enum role? {
      values = ["admin", "member", "moderator"]
    }

    object password_reset? {
      schema {
        password token?
        timestamp? expiration?
        bool used?
      }
    }

    text username? filters=trim
    int password_reset_attempts?=0 filters=min:0|max:5
    timestamp password_reset_requested_at?
    text password_reset_format? filters=trim|max:20
    image? avatar?
    text location? filters=trim
    enum account_status? {
      values = ["active", "disabled"]
    }

    timestamp? updated_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
  guid = "M0EM0AsK4P4E02rc0P-b35cNp2E"
}
