import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--domain", default="")  # Deprecated, kept for backward compatibility
@click.option("--web-base-url", default="")
def main(env, domain, web_base_url):
    if not domain and not web_base_url:
        return click.echo(
            "Argument for parameter `domain` and `web-base-url` is empty. Not changing web.base.url"
        )
    web_base_url = web_base_url or "https://%s" % domain
    click.echo("Setting web.base.url to `%s`" % web_base_url)

    base_url = env["ir.config_parameter"].search([("key", "=", "web.base.url")])
    if base_url:
        base_url.write({"value": web_base_url})
    else:
        base_url.create({"key": "web.base.url", "value": web_base_url})


if __name__ == "__main__":
    main()
