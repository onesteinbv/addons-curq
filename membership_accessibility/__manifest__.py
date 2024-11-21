# Copyright 2023 Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Membership Accessibility",
    "summary": "It automatically adds required groups for member users (Sales- Own Documents Only, Project - User and Timesheet- User: own timesheets only groups for now)"
    "Adds a new group which would manage whether users are able to see membership tab or not"
    "Adds membership and subscription tab in user profile so that members can view their own memberships."
    "Add a new group which would manage whether users are able to see sales,crm and contacts menu",
    "version": "16.0.1.0.0",
    "category": "Membership",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "membership_extension",
        "sale",
        "crm",
        "subscription_oca",
        "project",
        "hr_timesheet",
        "membership_hr_recruitment",
        "membership_committee",
    ],
    "data": ["security/membership_accessibility_security.xml", "views/views.xml"],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
