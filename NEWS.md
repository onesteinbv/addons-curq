# CURQ 18.0.10.0 (2026-11-05)

## Features

- New website block that shows store locations on a map.
  ([#422](https://github.com/onesteinbv/addons-curq/pull/422))
- Added support for dynamic membership types, allowing types that were previously
  static, such as follower, applicant, and committee, to be created dynamically. Also
  added a website layout option that displays all group members in a single list, with
  their membership type shown next to their name.

## Improvements

- Improved the bundle grid layout in the onboarding wizard.
  ([#397](https://github.com/onesteinbv/addons-curq/pull/397))
- Add Thunderbird and generic ICS button to the event page
  ([#398](https://github.com/onesteinbv/addons-curq/pull/398))
- Breadcrumbs on the website are now opt-in instead of opt-out. This means that
  breadcrumbs will be hidden by default on all pages, unless the user explicitly enables
  it. ([#406](https://github.com/onesteinbv/addons-curq/pull/406))
- The _/website/info_ page is now disabled by default.
  ([#407](https://github.com/onesteinbv/addons-curq/pull/407))
- Added support to define the action of a website form to create a helpdesk ticket.
- Add category "Bundles" to Apps view
  ([#414](https://github.com/onesteinbv/addons-curq/pull/414))
- Added spam protection to newsletter website block
- Added spam protection on donation payment form.
  ([#421](https://github.com/onesteinbv/addons-curq/pull/421))
- Moved the membership collaboration field ("Wants To Collaborate") to a more
  appropriate position.

## Fixes

- Fixed session revocation: it previously raised an error and did nothing, but now it
  correctly revokes the user's session.
  ([#401](https://github.com/onesteinbv/addons-curq/pull/401))
- Removed ordering based on Sorting code
  ([#405](https://github.com/onesteinbv/addons-curq/pull/405))
- Fixed issue with the CoinGecko exchange rates. The "Last Successful Update" date for
  currency rate providers only updates if rates that are found for that date so that
  rates are fetched again for missed out dates.
- Handle rollback during membership registration to avoid unwanted record creation and
  updates.
- Fixed translation issue on membership registration form
- Use image instead of icon for membership groups on registration page
  ([#423](https://github.com/onesteinbv/addons-curq/pull/423))
- Removed Skype as share option, as it is no longer supported by Microsoft.

# CURQ 18.0.9.2 (2026-06-19)

## Features

- Added branding for discuss public channels
  ([#393](https://github.com/onesteinbv/addons-curq/pull/393))

## Fixes

- Fixed issue where the configured favicon on the website was not displayed correctly
  ([#392](https://github.com/onesteinbv/addons-curq/pull/392))
- Applied ALTCHA protection to the event registration form
  ([#394](https://github.com/onesteinbv/addons-curq/pull/394))

# CURQ 18.0.9.1 (2026-06-16)

## Fixes

- Fix real-time connection issue

# CURQ 18.0.9.0 (2026-06-16)

## TLDR

Complete CURQ branding throughout the interface, support for external events, ALTCHA
protection on forms, and a new release notes feature so you stay up to date with the
latest features.

## Features & major improvements

### CURQ branding

We have replaced Odoo branding with **CURQ branding** in the following parts of the
interface.

- [web interface (#375)](https://github.com/onesteinbv/addons-curq/pull/375)
- [general settings (#377)](https://github.com/onesteinbv/addons-curq/pull/377)
- [frontend / website (#378)](https://github.com/onesteinbv/addons-curq/pull/378)
- [sales interface (#379)](https://github.com/onesteinbv/addons-curq/pull/379)
- [calendar (#380)](https://github.com/onesteinbv/addons-curq/pull/380)
- [membership management (#381)](https://github.com/onesteinbv/addons-curq/pull/381)
- [WPA (#384)](https://github.com/onesteinbv/addons-curq/pull/384)
- [accounting features (#385)](https://github.com/onesteinbv/addons-curq/pull/385)

### Release notes & tools

From now on you can see right away in CURQ what changes have been made, via a new
release notes feature. Additionally, we have added a number of buttons to the user menu:
to our documentation ([docs.curq.nl](https://docs.curq.nl)) and to our support page
([curq.nl/support](https://curq.nl/support)). The release notes can be found in the
general settings.

### ALTCHA protection

[Forms such as login, password reset and contact are now protected with ALTCHA (#391)](https://github.com/onesteinbv/addons-curq/pull/391),
an open-source and privacy-friendly alternative to reCAPTCHA. The _membership
registration form_ is also protected against abuse by this.

## Other improvements

### External events

It is now possible to
[promote events that are not managed by CURQ (#387)](https://github.com/onesteinbv/addons-curq/pull/387).
Handy if you also want to refer to activities of other organizations or partners.

### Open-source 2FA

When setting up two-factor authentication, we now also
[show recommendations for open-source authenticator apps](https://github.com/onesteinbv/addons-curq/pull/388),
so you can choose which tool suits you best.
