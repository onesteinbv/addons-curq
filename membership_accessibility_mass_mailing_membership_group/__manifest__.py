# Copyright 2023 Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Membership Accessibility Mass Mailing Membership Group",
    "summary": "Adds options for members to see whether they are on the mailing list of membership groups",
    "version": "16.0.1.0.0",
    "category": "Membership",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["membership_accessibility", "mass_mailing_membership_group"],
    "data": ["views/views.xml"],
}
