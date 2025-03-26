import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--login")
@click.option("--password")
def main(env, login, password):
    click.echo("Change password of `%s`..." % login)
    user = env["res.users"].search([("login", "=", login)])
    user.password = password


if __name__ == "__main__":
    main()
