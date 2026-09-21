import click
import click_odoo
from _user_write import password_matches


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--login")
@click.option("--password")
def main(env, login, password):
    click.echo("Change password of `%s`..." % login)
    user = env["res.users"].search([("login", "=", login)], limit=1)
    if not user:
        click.echo("No user with login `%s`; nothing to do." % login)
        return
    if password_matches(env, user, password):
        # Writing the same password still sends a security notification.
        click.echo("Password of `%s` is already set; skipping write." % login)
        return
    user.password = password


if __name__ == "__main__":
    main()
