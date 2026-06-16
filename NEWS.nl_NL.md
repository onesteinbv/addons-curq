# CURQ 18.0.9.0 (16-06-2026)

## TLDR

Een complete CURQ-branding door de hele interface, ondersteuning voor externe evenementen, ALTCHA-beveiliging op formulieren en een nieuwe release notes-functie zodat je altijd op de hoogte blijft van de nieuwste features.

## Functionaliteiten & grootschalige verbeteringen

### CURQ-branding

We hebben de Odoo-branding vervangen door **CURQ-branding** in de volgende onderdelen van de interface.

* [webinterface (#375)](https://github.com/onesteinbv/addons-curq/pull/375)
* [algemene instellingen (#377)](https://github.com/onesteinbv/addons-curq/pull/377)
* [frontend / website (#378)](https://github.com/onesteinbv/addons-curq/pull/378)
* [verkoopinterface (#379)](https://github.com/onesteinbv/addons-curq/pull/379)
* [agenda (#380)](https://github.com/onesteinbv/addons-curq/pull/380)
* [lidmaatschapsbeheer (#381)](https://github.com/onesteinbv/addons-curq/pull/381)
* [WPA (#384)](https://github.com/onesteinbv/addons-curq/pull/384)
* [boekhoudfuncties (#385)](https://github.com/onesteinbv/addons-curq/pull/385)

### Release notes & hulpmiddelen

Je ziet vanaf nu meteen in CURQ welke wijzigingen er zijn doorgevoerd, via een nieuwe release notes-feature. Daarnaast hebben we in het gebruikersmenu een aantal knoppen toegevoegd: naar onze documentatie ([docs.curq.nl](https://docs.curq.nl)) en naar onze supportpagina ([curq.nl/support](https://curq.nl/support)). De release notes zijn terug te vinden in de algemene instellingen.

### ALTCHA-bescherming

[Formulieren zoals aanmelden, wachtwoord resetten en contact zijn nu beveiligd met ALTCHA (#391)](https://github.com/onesteinbv/addons-curq/pull/391), een open-source en privacyvriendelijk alternatief voor reCAPTCHA. Ook het *membership registration form* is hierdoor beveiligd tegen misbruik.

## Overige verbeteringen

### Externe evenementen

Het is nu mogelijk om [evenementen te promoten die niet door CURQ worden beheerd (#387)](https://github.com/onesteinbv/addons-curq/pull/387). Handig als je ook wilt verwijzen naar activiteiten van andere organisaties of partners.

### Open-source 2FA

Bij het instellen van tweestapsauthenticatie laten wij nu ook [aanbevelingen voor open-source authenticator-apps](https://github.com/onesteinbv/addons-curq/pull/388) zien, zodat je zelf kunt kiezen welke tool het beste bij je past.
