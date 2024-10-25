import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--do-uninstall", is_flag=True, default=False)
def main(env, do_uninstall):
    click.echo("Upgrading bundles...")
    modules = env["ir.module.module"].search([("state", "=", "installed")])
    bundles = modules.filtered(lambda m: m.is_bundle)
    bundles.button_immediate_upgrade()

    if do_uninstall:
        current_modules = modules.filtered(lambda m: not m.auto_install)
        target_modules = bundles.upstream_dependencies()
        retired_modules = current_modules - target_modules
        if retired_modules:
            click.echo("Uninstalling %s..." % ", ".join(retired_modules.mapped("name")))
            retired_modules.button_immediate_uninstall()


if __name__ == "__main__":
    main()
