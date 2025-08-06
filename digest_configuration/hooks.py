def post_init_hook(env):
    env["ir.config_parameter"].sudo().search(
        [("key", "=", "digest.default_digest_emails")]
    ).unlink()
