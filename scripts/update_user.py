import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--xml-id", default="base.user_admin")
@click.option("--login")
@click.option("--password")
def main(env, xml_id, login, password):
    click.echo("Update user `%s`..." % xml_id)
    user = env.ref(xml_id)
    user.login = login
    user.password = password


if __name__ == "__main__":
    main()
