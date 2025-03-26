import click
import click_odoo

from odoo.exceptions import MissingError


@click.command()
@click_odoo.env_options(default_log_level="error")
def main(
    env,
):  # We have this script because module_change_auto_install doesn't work properly with initdb (click-odoo-contrib)
    module_names = ["iap", "partner_autocomplete"]
    click.echo("Uninstalling auto-install modules...")
    modules = env["ir.module.module"].search(
        [("name", "in", module_names), ("state", "=", "installed")]
    )
    if modules:
        try:
            modules.button_immediate_uninstall()
        except MissingError:
            modules.button_immediate_upgrade()
            modules.button_immediate_uninstall()


if __name__ == "__main__":
    main()
