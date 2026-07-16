# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Human Resources",
    "summary": "Centralize employee information",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Human Resources",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr",
        "hr_accessibility",
        "hr_contract",
        "hr_expense",
        "hr_employee_firstname",
        "hr_timesheet_sheet",
        "hr_timesheet_sheet_accessibility",
        "hr_holidays",
        # hr_timesheet depends on project, so we need to include project_accessibility as well
        "project_accessibility",
    ],
    "bundle": True,
}
