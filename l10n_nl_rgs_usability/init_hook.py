# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    companies = env["res.company"].search([("chart_template", "=", "nl_rgs")])
    for company in companies:
        # Generate payment modes
        env["account.chart.template"]._generate_payment_modes(company)

    # Set payment credit account for bank journals
    journals = env["account.journal"].search([])
    journals._set_journal_bank_payment_credit_account()

    # Ensure RGS is installed for the main company
    # This is handled normally by `account` module after installation of a chart in `ir.module.write`
    main_company = env.ref("base.main_company", False)
    if (
        main_company
        and not main_company.chart_template
        and not main_company._existing_accounting()
    ):

        def _load(env):
            env["account.chart.template"]._load(
                "nl_rgs",
                main_company,
                install_demo=False,
            )

        env.registry._auto_install_template = _load

    # Archive the cash basis tax journal
    journals = env["account.journal"].search([])
    for journal in journals.filtered(
        lambda j: j.code == "CABA" and j.company_id.chart_template == "nl_rgs"
    ):
        journal.active = False

    companies = env["res.company"].search([("chart_template", "=", "nl_rgs")])
    for company in companies:
        # Verify VAT Numbers set to True
        company.vat_check_vies = True
        # Create Direct debit in payment mode
        company._create_direct_debit_in_payment_mode()
        # Create spread templates
        company._create_spread_templates()
