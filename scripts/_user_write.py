def password_matches(env, user, password):
    """True when `password` already hashes to what is stored for `user`.

    Read through SQL because `res.users.password` always reads back empty.
    """
    if not password:
        return False
    env.cr.execute(
        "SELECT COALESCE(password, '') FROM res_users WHERE id = %s", (user.id,)
    )
    [hashed] = env.cr.fetchone()
    valid, _ = user._crypt_context().verify_and_update(password, hashed)
    return bool(valid)
