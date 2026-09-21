import click
import click_odoo
from _user_write import password_matches


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--xml-id", default="base.user_admin")
@click.option("--login")
@click.option("--password")
def main(env, xml_id, login, password):
    click.echo("Update user `%s`..." % xml_id)
    user = env.ref(xml_id)
    if login and user.login != login:
        user.login = login
    elif login:
        # Writing the same login still sends a security notification.
        click.echo("Login of `%s` is already set; skipping write." % xml_id)
    if password and not password_matches(env, user, password):
        user.password = password
    elif password:
        click.echo("Password of `%s` is already set; skipping write." % xml_id)


if __name__ == "__main__":
    main()
