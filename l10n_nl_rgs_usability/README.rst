========================================
Netherlands - RGS Accounting - Usability
========================================

This module contains usability improvements for RGS accounting that are not fitting
in module l10n_nl_rgs. The idea is to leave l10n_nl_rgs as much generic as possible.

- when creating bank/cash journals, the selection of bank account is filtered by journal type
- add multi-company rule for Sequence
- enable analytic accounting by default
- automatically load pre-defined payment terms and payment modes
- automatically add payment account in SEPA payment method line
- automatically install RGS for main company
- automatically install RGS when creating a new company
- remove onboarding setup step regarding COA setup
- remove onboarding "Import your first bill" popup
- archive the cash basis tax journal
- check_chronology active for purchase journals
- create fiscal year for current year
- archive VAT report menuitem
- mandate and payment mode visibility on customer invoice
- impede creating bank journals directly, use menu 'Add a Bank Account' instead
- 'Verify VAT Numbers' set to True
- add 'Direct debit' payment mode
- create spread templates
