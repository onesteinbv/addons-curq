import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
def main(env):
    click.echo("Check/Install nl_NL language pack...")

    installed_langs = dict(env["res.lang"].get_installed())
    # Dutch
    lang = "nl_NL"
    if lang not in installed_langs:
        env["res.lang"]._activate_lang(lang)
    # English
    lang = "en_US"
    if lang not in installed_langs:
        env["res.lang"]._activate_lang(lang)

    # Force translation of all modules to Dutch
    mods = env["ir.module.module"].search([("state", "=", "installed")])
    mods._update_translations(["nl_NL"], True)

    # Force position of EUR currency to "before"
    currency = env["res.currency"].search([("name", "=", "EUR")])
    currency.write({"position": "before"})


if __name__ == "__main__":
    main()
