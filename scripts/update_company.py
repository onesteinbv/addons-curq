import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--name")
@click.option("--email")
@click.option("--coc")
@click.option("--city")
@click.option("--zip", "zip_code")  # To not override inbuilt zip
@click.option("--street")
def main(env, name, email, coc, city, zip_code, street):
    click.echo("Update company information...")
    required_modules = env["ir.module.module"]
    required_modules += env.ref("base.module_l10n_nl")
    required_modules += env.ref("base.module_base_customer_company")

    for required_module in required_modules:
        if required_module.state != "installed":
            return click.echo(
                "%s must be installed for this script to run (updating company information)"
                % required_module.name,
                err=True,
            )

    main_company = env.ref("base.main_company", raise_if_not_found=False)

    if not main_company or main_company.updated_by_script:
        click.echo("Company information is already changed")
        return

    values = {
        "name": name,
        "email": email,
        "company_registry": coc,
        "l10n_nl_kvk": coc,
        "city": city,
        "zip": zip_code,
        "street": street,
        "updated_by_script": True,
    }

    netherlands = env.ref(
        "base.nl", raise_if_not_found=False
    )  # Should always exists but I don't ever want this to have errors
    if netherlands:
        values.update({"country_id": netherlands.id})

    main_company.write(values)


if __name__ == "__main__":
    main()
