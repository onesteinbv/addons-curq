def post_init_hook(env):
    env["res.company"].sudo().search([]).write({"currency_rates_autoupdate": False})
    env["account.journal"].sudo().search([("type", "=", "sale")]).write(
        {"check_chronology": True}
    )
    env["account.journal"].sudo().search([("type", "=", "purchase")]).write(
        {"check_chronology": False}
    )
