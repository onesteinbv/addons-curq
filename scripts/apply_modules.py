import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--do-uninstall", is_flag=True, default=False)
def main(env, do_uninstall):
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

    # NB: Disable for now. Better to go from A to B to C than from A to C
    # if do_uninstall:
    #     current_modules = modules.filtered(lambda m: not m.auto_install)
    #     target_modules = bundles + bundles.upstream_dependencies(
    #         exclude_states=("uninstallable",)
    #     )
    #     retired_modules = current_modules - target_modules
    #     if retired_modules:
    #         click.echo("Uninstalling %s..." % ", ".join(retired_modules.mapped("name")))
    #         retired_modules.button_immediate_uninstall()


if __name__ == "__main__":
    main()
