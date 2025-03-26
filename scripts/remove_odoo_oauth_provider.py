import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
def main(env):
    click.echo("Remove Odoo.com login...")
    provider_openerp = env.ref("auth_oauth.provider_openerp", raise_if_not_found=False)
    if provider_openerp:
        provider_openerp.unlink()


if __name__ == "__main__":
    main()
