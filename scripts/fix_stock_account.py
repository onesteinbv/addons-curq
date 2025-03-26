import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
def main(env):
    # Installing stock_account will create ir.property property_stock_account_output_categ_id and property_stock_account_input_categ_id for the
    # main_company. Somehow if this module is installed it removes the ir.model.data or ir.property. (in rgs._load(main_company) -> self.generate_properties())
    # See: accounts/chart_template.py in def _load(self, company) it deletes ir.property
    # This is a core issue it can also be triggered by creating a database installing stock_account installing belgium coa switch to it, and update stock_account
    # TODO: Fix in core, can be remove when done on existing databases
    xml_ids = [
        ("stock_account", "property_stock_account_output_categ_id"),
        ("stock_account", "property_stock_account_input_categ_id"),
    ]
    main_company = env.ref("base.main_company", False)
    if not main_company:  # Not sure if main company can be deleted
        return
    for xml_id in xml_ids:
        ir_property = env.ref("%s.%s" % (xml_id[0], xml_id[1]), False)
        if ir_property:
            continue
        env["ir.model.data"].create(
            {
                "res_id": env["ir.property"].search(
                    [
                        ("name", "=", xml_id[1]),
                        ("company_id", "=", main_company.id),
                        ("res_id", "=", False),
                    ]
                ),
                "model": "ir.property",
                "name": xml_id[1],
                "module": xml_id[0],
                "noupdate": True,
            }
        )


if __name__ == "__main__":
    main()
