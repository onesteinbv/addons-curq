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
