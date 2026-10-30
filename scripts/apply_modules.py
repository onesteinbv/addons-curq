import click
import click_odoo

from odoo.exceptions import MissingError

AUTO_INSTALL_MODULES_TO_UNINSTALL = [
    "crm_iap_enrich",
    "crm_iap_mine",
    "iap_crm",
    "snailmail",
    "snailmail_account",
    "partner_autocomplete",
    "website_share_filter_option_skype",
]


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

    # Install auto_install modules where all dependencies are met
    auto_install_modules = env["ir.module.module"].search(
        [
            ("state", "=", "uninstalled"),
            ("auto_install", "=", True),
            ("name", "not in", AUTO_INSTALL_MODULES_TO_UNINSTALL),
        ]
    )
    installed_module_names = set(
        env["ir.module.module"].search([("state", "=", "installed")]).mapped("name")
    )
    auto_install_modules = auto_install_modules.filtered(
        lambda module: all(
            dependency.name in installed_module_names
            for dependency in module.dependencies_id
        )
    )
    if auto_install_modules:
        module_names = ", ".join(auto_install_modules.mapped("name"))
        click.echo("Installing auto-install modules: %s..." % module_names)
        auto_install_modules.button_immediate_install()

    # Uninstall auto_install modules we don't want
    click.echo("Uninstalling auto-install modules...")
    modules = env["ir.module.module"].search(
        [
            ("name", "in", AUTO_INSTALL_MODULES_TO_UNINSTALL),
            ("state", "=", "installed"),
        ]
    )
    if modules:
        try:
            modules.button_immediate_uninstall()
        except MissingError:
            modules.button_immediate_upgrade()
            modules.button_immediate_uninstall()

    # Uninstall the website_share_filter_option_skype module if it is installed
    website_share_filter_option_skype_module = env.ref(
        "base.module_website_share_filter_option_skype", False
    )

    if website_share_filter_option_skype_module:
        if website_share_filter_option_skype_module.state == "installed":
            website_share_filter_option_skype_module.button_immediate_uninstall()
        elif website_share_filter_option_skype_module.state == "to install":
            website_share_filter_option_skype_module.button_install_cancel()
        elif website_share_filter_option_skype_module.state == "to upgrade":
            website_share_filter_option_skype_module.button_upgrade_cancel()
            website_share_filter_option_skype_module.button_immediate_uninstall()
        elif website_share_filter_option_skype_module.state == "to remove":
            website_share_filter_option_skype_module.button_uninstall_cancel()
            website_share_filter_option_skype_module.button_immediate_uninstall()


if __name__ == "__main__":
    main()
