query "profiles/{user_id}" verb=GET {
  api_group = "Codeboxd"

  input {
    int user_id
  }

  stack {
    db.query profile {
      where = $db.profile.user_id == $input.user_id
      return = {type: "single"}
    } as $profile
  
    precondition ($profile != null) {
      error_type = "notfound"
      error = "Perfil não encontrado."
    }
  
    db.query user_media_interaction {
      where = $db.user_media_interaction.user_id == $input.user_id
      return = {type: "list"}
    } as $interactions
  
    db.query user_follow {
      where = $db.user_follow.followed_id == $input.user_id
      return = {type: "list"}
    } as $followers
  
    db.query user_follow {
      where = $db.user_follow.follower_id == $input.user_id
      return = {type: "list"}
    } as $following
  }

  response = {
    profile     : $profile
    interactions: $interactions
    followers   : $followers
    following   : $following
  }

  guid = "KN99IAk_SICbNLL9IZnwXi_oBCU"
}