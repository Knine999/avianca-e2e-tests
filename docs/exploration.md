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

## First automated run on Windows (2026-10-27)

Run with `pytest -m e2e --headed -s` on Windows, Python 3.12, Chromium from Playwright.

- Label 1 passed. The cookie banner was accepted and the Round trip tab was visible.
- Label 2 passed. Choosing One way hid the Return field.
- Label 3 failed on the Origin field. Playwright found the "Origin" label, but the field container covered it, so the click timed out after 15 seconds. A site announcement bar (a "marquesina" element at the top of the page) also intercepted clicks.
- This was not an Access Denied page. The test reached the home page and the form.
- The fix was to click the input that the label points to, using its label, instead of the label text.
- Second run: the click worked, but the label matched two elements (the input and the open list). The input has the combobox role, so the test now finds it by role and name.
- Third run: typing worked, but no element with the text "(MIA)" showed up in the list. The test now types the city one key at a time, picks the option inside the field's list by the airport code, and skips the origin when it already shows Miami (MIA).
- Fourth run: origin and destination passed. The date step failed because the calendar shows two months and the first "10" was a past, disabled day. The test now picks the day by its `data-date` attribute.
- In every run so far the tester had to click Accept on the cookie banner by hand. The test was waiting for the banner's outer container, which does not count as visible. It now waits for the Accept button.
- Fifth run: the test accepted the cookie banner by itself. Origin, destination and date passed. The adult count was 2, but the check looked for the text "2 Adults", which the site does not show. The count is a number next to the plus and minus buttons, and those buttons are named Increase and Decrease. The test now checks the number and that both buttons are enabled.
- The Departure field shows the date as MM/DD/YYYY on the English site (11/10/2026 for November 10). The challenge expects DD/MM/YYYY.
- Sixth run: labels 1 to 6 passed and the search opened `booking.avianca.com/av/booking/avail`. The result was xfailed. Label 7 passed only because it checks the URL. The saved trace shows the results page was blank.
- Seventh run: the search reached the same URL with the right values and the server answered 200, but the page stayed blank for more than 15 seconds and the click timed out. The only other request to that domain was a script with an obscured path, which looks like bot protection. The Search click now has the navigation timeout.
- Eighth run, with a 20 second wait on the results page: the page showed "Access denied. The request was blocked by the security rules (error code 15)", sent via Imperva. The server answered 403 to the second request for the results URL. Details in [blocker.md](blocker.md).

## Not explored

Steps 8 to 18 of Test 4: fares, the upgrade pop-up, the passenger form, contact details, services and the payment summary.

## Open questions

- Does the full English flow pass in an automated run once the cookie change is in place? This still needs a run.
- Does the search results page show the outbound flight list as the challenge expects (label 7)? The automated test only checks the booking URL.
