# CURQ 18.0.10.0 (05-11-2026)

## Nieuwe functionaliteiten

- Nieuw websiteblok dat winkellocaties op een kaart toont.
  ([#422](https://github.com/onesteinbv/addons-curq/pull/422))
- Ondersteuning toegevoegd voor dynamische lidmaatschapstypen. Typen die voorheen
  statisch waren, zoals volger, kandidaat en commissie, kunnen nu dynamisch worden
  aangemaakt. Ook is er een website-indeling toegevoegd waarmee alle groepsleden in één
  lijst worden weergegeven, met hun lidmaatschapstype naast hun naam.

## Verbeteringen

- De rasterindeling van bundels in de onboardingwizard verbeterd.
  ([#397](https://github.com/onesteinbv/addons-curq/pull/397))
- Een Thunderbird- en algemene ICS-knop toegevoegd aan de evenementpagina.
  ([#398](https://github.com/onesteinbv/addons-curq/pull/398))
- Breadcrumbs op de website zijn nu opt-in in plaats van opt-out. Dat betekent dat
  breadcrumbs standaard op alle pagina's verborgen zijn, tenzij de gebruiker ze
  expliciet inschakelt. ([#406](https://github.com/onesteinbv/addons-curq/pull/406))
- De pagina _/website/info_ is nu standaard uitgeschakeld.
  ([#407](https://github.com/onesteinbv/addons-curq/pull/407))
- Ondersteuning toegevoegd om de actie van een websiteformulier in te stellen op het
  aanmaken van een helpdeskticket.
- De categorie 'Bundels' toegevoegd aan de Apps-weergave.
  ([#414](https://github.com/onesteinbv/addons-curq/pull/414))
- Spambeveiliging toegevoegd aan het nieuwsbriefwebsiteblok.
- Spambeveiliging toegevoegd aan het betalingsformulier voor donaties.
  ([#421](https://github.com/onesteinbv/addons-curq/pull/421))
- Het lidmaatschapsveld voor samenwerking ('Wants To Collaborate') verplaatst naar een
  geschiktere plek.

## Opgelost

- Sessie-intrekking opgelost: deze gaf eerder een foutmelding en deed niets, maar trekt
  nu de sessie van de gebruiker correct in.
  ([#401](https://github.com/onesteinbv/addons-curq/pull/401))
- Sortering op basis van de sorteercode verwijderd.
  ([#405](https://github.com/onesteinbv/addons-curq/pull/405))
- Probleem met de CoinGecko-wisselkoersen opgelost. De datum 'Last Successful Update'
  van valutakoersaanbieders wordt alleen bijgewerkt als er voor die datum koersen zijn
  gevonden. Zo worden koersen voor gemiste datums opnieuw opgehaald.
- Rollback tijdens lidmaatschapsregistratie afgehandeld om ongewenste aanmaak en
  wijzigingen van records te voorkomen.
- Vertaalprobleem op het lidmaatschapsregistratieformulier opgelost.
- Op de registratiepagina wordt voor lidmaatschapsgroepen nu een afbeelding gebruikt in
  plaats van een pictogram. ([#423](https://github.com/onesteinbv/addons-curq/pull/423))
- Skype verwijderd als share-optie, omdat Microsoft dit niet langer ondersteunt.

# CURQ 18.0.9.2 (19-06-2026)

## Features

- Branding toegevoegd voor openbare discussie kanalen
  ([#393](https://github.com/onesteinbv/addons-curq/pull/393))

## Fixes

- Opgelost: geconfigureerde favicon op de website werd niet correct weergegeven
  ([#392](https://github.com/onesteinbv/addons-curq/pull/392))
- ALTCHA-beveiliging toegepast op het evenementregistratieformulier
  ([#394](https://github.com/onesteinbv/addons-curq/pull/394))

# CURQ 18.0.9.1 (16-06-2026)

## Fixes

- Realtime verbinding probleem opgelost

# CURQ 18.0.9.0 (16-06-2026)

## TLDR

Een complete CURQ-branding door de hele interface, ondersteuning voor externe
evenementen, ALTCHA-beveiliging op formulieren en een nieuwe release notes-functie zodat
je altijd op de hoogte blijft van de nieuwste features.

## Functionaliteiten & grootschalige verbeteringen

### CURQ-branding

We hebben de Odoo-branding vervangen door **CURQ-branding** in de volgende onderdelen
van de interface.

- [webinterface (#375)](https://github.com/onesteinbv/addons-curq/pull/375)
- [algemene instellingen (#377)](https://github.com/onesteinbv/addons-curq/pull/377)
- [frontend / website (#378)](https://github.com/onesteinbv/addons-curq/pull/378)
- [verkoopinterface (#379)](https://github.com/onesteinbv/addons-curq/pull/379)
- [agenda (#380)](https://github.com/onesteinbv/addons-curq/pull/380)
- [lidmaatschapsbeheer (#381)](https://github.com/onesteinbv/addons-curq/pull/381)
- [WPA (#384)](https://github.com/onesteinbv/addons-curq/pull/384)
- [boekhoudfuncties (#385)](https://github.com/onesteinbv/addons-curq/pull/385)

### Release notes & hulpmiddelen

Je ziet vanaf nu meteen in CURQ welke wijzigingen er zijn doorgevoerd, via een nieuwe
release notes-feature. Daarnaast hebben we in het gebruikersmenu een aantal knoppen
toegevoegd: naar onze documentatie ([docs.curq.nl](https://docs.curq.nl)) en naar onze
supportpagina ([curq.nl/support](https://curq.nl/support)). De release notes zijn terug
te vinden in de algemene instellingen.

### ALTCHA-bescherming

[Formulieren zoals aanmelden, wachtwoord resetten en contact zijn nu beveiligd met ALTCHA (#391)](https://github.com/onesteinbv/addons-curq/pull/391),
een open-source en privacyvriendelijk alternatief voor reCAPTCHA. Ook het _membership
registration form_ is hierdoor beveiligd tegen misbruik.

## Overige verbeteringen

### Externe evenementen

Het is nu mogelijk om
[evenementen te promoten die niet door CURQ worden beheerd (#387)](https://github.com/onesteinbv/addons-curq/pull/387).
Handig als je ook wilt verwijzen naar activiteiten van andere organisaties of partners.

### Open-source 2FA

Bij het instellen van tweestapsauthenticatie laten wij nu ook
[aanbevelingen voor open-source authenticator-apps](https://github.com/onesteinbv/addons-curq/pull/388)
zien, zodat je zelf kunt kiezen welke tool het beste bij je past.
