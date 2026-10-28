# Site exploration notes

Notes from opening avianca.com by hand and from the automated runs. Anything not listed here was not checked.

## English site (`/en`)

- The default origin depends on the visitor's location. When testing from the US the origin is Miami (MIA). The test sets the origin explicitly.
- Prices and the currency are in USD on this version.
- Trip type defaults to "Round trip". "One way" is the tab next to it.
- Passengers default to 1.
- The cookie banner is OneTrust. Its buttons are "Set configuration" and "Accept". The test clicks "Accept".

## Spanish site (`/es`)

Observed in an earlier run, before the project moved to the English site.

- `/en` redirected to `/es` in one run.
- Prices and the currency were in Colombian pesos (COP). The origin was Bogota (BOG).
- "One way" hides the Return field.
- Searching opens `booking.avianca.com/av/booking/avail` with the search values in the URL.
- One run was blocked with "Access Denied" on `/es`. The page shows a reference number and an `errors.edgesuite.net` link. That is Akamai's bot protection.

## Not explored

Steps 8 to 18 of Test 4: fares, the upgrade pop-up, the passenger form, contact details, services and the payment summary.

## Open questions

- Does the full English flow pass in an automated run once the cookie change is in place? This still needs a run.
- Does the search results page show the outbound flight list as the challenge expects (label 7)? The automated test only checks the booking URL.
