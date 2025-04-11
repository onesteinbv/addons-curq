[![Pre-commit Status](https://github.com/onesteinbv/addons-container/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/onesteinbv/addons-container/actions/workflows/pre-commit.yml)
[![Demo](https://img.shields.io/badge/Demo-Try_it_out-blue)](https://demo.curq.nl/web/login)

# CURQ

CURQ is an all-in-one platform for businesses, built on Odoo and other FOSS.

CURQ is purpose-built / highly opinionated where the goal is to make a complete package without 
business consultant having to think about every single module to install. The goal is to streamline the 
installation process and support process. Basically Curq is Odoo + OCA modules + other open source modules 
pre-packaged with bundles. A bundle is a normal Odoo module with only dependencies to other modules.

## Bundles

In CURQ, bundles are a set of predefined modules that makes installation of Odoo much easier, you don't need
much knowledge about what modules exists. E.g. the essential bundle (`container_install`) contains 
alot of modules that we need / want for every installation. We now can just install those with a simple click.

**Available out of the box**: 

- **Essentials Installation** (`container_install`): Installs essential modules
- **Accounting** (`account_install`): Invoices, Contracts & Payments
- **CRM** (`crm_install`): Track leads and close opportunities
- **Event organizer** (`event_install`): Efficiently organize events and all related tasks: planning, 
  registration tracking, attendances, etc
- **Helpdesk** (`helpdesk_install`): Streamline customer support and ensure quick and efficient issue resolution
- **Human Resources** (`hr_install`): Centralize employee information
- **Email Marketing** (`mass_mailing_install`): Design, send, and track emails
- **Membership Management** (`membership_install`): Efficiently manage memberships and administrative tasks
- **Project Management** (`project_install`): Organize and plan your projects 
- **Sales Management** (`sale_install`): Sales process from quotations to invoices
- **Inventory** (`stock_install`): Manage your stock and logistics activities
- **Surveys** (`survey_install`): Create, distribute, and analyze questionnaires to gather feedback, opinions, or data 
  efficiently
- **Publish Events** (`website_event_install`): Publish events, and sell tickets on your website
- **Website & Blog** (`website_install`): Build a website
- **Community Builder** (`website_membership_install`): Empower your community with tools to improve member engagement,
  content sharing, and more
- **eCommerce** (`website_sale_install`): Sell your products online

TODO: Screenshot of wizard

## Creating new bundles

Creating a bundle is very easy. By adding the flag: `bundle: True` to the `__manifest__.py` you make sure
that the dependencies (`depends`) are automatically uninstalled when the bundle is uninstalled. Note that a dependency
is only uninstalled when it's not required in any other installed bundle. For example `website_install` and 
`website_sale` both depend on `website` but if both are installed and `website_install` is uninstalled
it will not uninstall `website`.

## GIT Aggregator

CURQ uses [git-aggregator](https://github.com/acsone/git-aggregator) to fetch modules from different sources.
CURQ uses a copy of OCA modules for convenience here: [onesteinbv/addons-oca](https://github.com/onesteinbv/addons-oca) 
primarily to prevent having to add every single OCA repository and necessary pull requests to the `repo.yaml` which
will make it utterly tedious to maintain. Other modules used in CURQ are in 
[onesteinbv/addons-generic](https://github.com/onesteinbv/addons-generic) which are (most if not all) generic
modules that are not yet proposed to the OCA or just not interesting for the OCA.

## package.txt

Aggregated modules aren't automatically included in the 
[curq image](https://github.com/onesteinbv/addons-curq/pkgs/container/curq) that is the `package.txt` for.

## Maintenance scripts

After installation or update of Odoo (`$MODE` Install, Init or Update) it will `scripts/run.sh` which does some
basic setup of the database. 

## Resources

- [Documentation](https://docs.curq.nl)
- Contributing
- [Bug tracker](https://github.com/onesteinbv/addons-curq/issues)
- [Updates](https://curq.nl/blog)

## Docker

The image is based on https://github.com/onesteinbv/odoo-docker 
most info on all options / environment variables can be found there. 
But notably the `MODE` env variable is most important

docker compose

## Helm

## License

AGPL