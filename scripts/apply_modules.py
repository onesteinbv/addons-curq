import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--dry-run", is_flag=True, default=False)
def main(env, dry_run):
    click.echo("Upgrading bundles...")
    base_module_bundle = env.ref("base.module_base_module_bundle")
    if base_module_bundle.state != "installed":
        return click.echo(
            "`base_module_bundle` is not installed",
            err=True,
        )

    modules = env["ir.module.module"].search([("state", "=", "installed")])
    bundles = modules.filtered(lambda m: m.is_bundle)
    bundles.button_immediate_upgrade()

    current_modules = modules.filtered(lambda m: not m.auto_install)
    target_modules = bundles + bundles.upstream_dependencies(
        exclude_states=("uninstallable",)
    )
    ignore_modules = modules.filtered(
        lambda m: m.name in ["container_s3"] or m.name.startswith("theme_")
    )

    # Exempt payment providers from retirement if the payment module is installed
    payment_module = env.ref("base.module_payment")
    if payment_module.state == "installed":
        click.echo(
            "Payment module is installed, exempting payment providers from retirement."
        )
        ignore_modules += env["payment.provider"].search([]).mapped("module_id")

    target_modules += ignore_modules
    retired_modules = current_modules - target_modules
    if retired_modules:
        if dry_run:
            click.echo(
                "Retired modules: %s" % ", ".join(retired_modules.mapped("name"))
            )
        else:
            click.echo("Uninstalling %s..." % ", ".join(retired_modules.mapped("name")))
            retired_modules.button_immediate_uninstall()
    else:
        click.echo("No retired modules.")


if __name__ == "__main__":
    main()
