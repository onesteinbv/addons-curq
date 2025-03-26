import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--domain")
def main(env, domain):
    if not domain:
        return click.echo(
            "Argument for parameter domain is empty. Not changing web.base.url"
        )
    click.echo("Setting web.base.url to `https://%s`" % domain)

    base_url = env["ir.config_parameter"].search([("key", "=", "web.base.url")])
    if base_url:
        base_url.write({"value": "https://%s" % domain})
    else:
        base_url.create({"key": "web.base.url", "value": "https://%s" % domain})


if __name__ == "__main__":
    main()
