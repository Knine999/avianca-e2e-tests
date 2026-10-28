# Blocker: bot protection in automated runs

## Summary

In my automated runs with Playwright, the search reaches the booking URL with the right values, but a few seconds later the results page is replaced by an "Access denied" page from the site's bot protection. My manual walk-through in Chrome completed the whole flow (see [manual_validation.md](manual_validation.md)). So the block affects the automated browser, not the flow itself.

## What I saw in automated runs

- **Access Denied (Akamai).** In one run the browser was sent to the Spanish site (`/es`) and the page returned "Access Denied", with a reference number and a link to `errors.edgesuite.net`. Evidence: [02_access_denied_spanish_site.png](evidence/02_access_denied_spanish_site.png).
- **Cookie banner over the page.** In another run the English home page loaded, but the OneTrust banner stayed on screen and covered the page. I changed how the test handles the banner after this run. Evidence: [01_english_home_cookie_banner.png](evidence/01_english_home_cookie_banner.png).
- **Blank page, then Access denied on the results page.** Right after the search the page is white for a few seconds ([03_booking_page_blank_automated.jpeg](evidence/03_booking_page_blank_automated.jpeg)). Then it shows "Access denied. The request was blocked by the security rules (error code 15)", sent via Imperva, with an incident ID ([04_results_page_access_denied_imperva.png](evidence/04_results_page_access_denied_imperva.png), with my IP address covered).

## What happens on the results page

I recorded the network responses and cookies of one run ([05_results_page_diagnosis.json](evidence/05_results_page_diagnosis.json)). The cookie list has names only, no values. This is the order of events:

1. The browser opens `booking.avianca.com/av/booking/avail` with the search values, and the server answers 200.
2. The page loads a script from a path with random words, then sends data back to it with a POST.
3. The browser asks for the same results URL again, and this time the server answers 403.
4. The page loads several `_Incapsula_Resource` files, one of them with an `incident_id`.
5. The "Access denied" page appears, inside a frame.

The cookies match two bot protection products. `_abck`, `bm_sz`, `ak_bmsc` and `bm_sv` are the names used by Akamai Bot Manager. `visid_incap_*`, `incap_ses_*`, `nlbi_*` and `reese84` are the names used by Imperva (Incapsula). So the booking site checks the browser first, then refuses the results page and shows Imperva's block page.

## Why the Access denied page did not show up before

- The block page appears a few seconds after the results URL loads, and it is drawn inside a frame. The page body itself has no text.
- Earlier versions of the test only checked the URL and stopped right away, so the screenshot showed the white page in between.
- The first "Access Denied" I saw, on `/es`, was a different page. It came from Akamai on `www.avianca.com` (with an `errors.edgesuite.net` link). The one on the results page comes from Imperva on `booking.avianca.com`.

The test now waits for the block page and, if it appears, stops with the reason "the results page was blocked by the site's bot protection".

## Headless mode

When the tests run without a visible browser (headless), the site blocks the home page itself. `www.avianca.com/en` answers with Akamai's "Access Denied" page and a reference number, so neither test can start. Evidence: [06_home_access_denied_headless.jpeg](evidence/06_home_access_denied_headless.jpeg).

With a visible browser (`--headed`) the home page loads and both tests run. That is why `pytest.ini` includes `--headed`. If the home page is blocked anyway, the tests stop with the reason "the home page was blocked by the site's bot protection".

## Labels not automated

The challenge lists 20 entries under labels 1 to 18. Labels 13 and 16 each appear twice.

| Label | What it covers |
|---|---|
| 8 | Choose the cheapest flight. The fare options are displayed. |
| 9 | Select the cheapest fare and click the price button. The upgrade pop-up opens. |
| 10 | Select "Continue with restrictions". The trip summary is displayed. |
| 11 | Click Continue. The passenger information screen opens. |
| 12 | Enter gender, first name, last name, date of birth and nationality for both passengers. |
| 13 | Enter the booking holder's contact details and accept the privacy policy. Then click Continue. |
| 14 | If the baggage section is shown, select "No, I have what I need". |
| 15 | Select Priority Boarding. The pop-up opens. |
| 16 | Select both passengers, then click Save and Exit. Then click Go to Payment. |
| 17 | Review the purchase summary. Airports, date, fare and flight number must match the selection. Amounts in USD. |
| 18 | Close the browser. |

Labels 8 to 18 are not automated, because the automated browser is blocked on the results page. The manual run shows that these labels work for a person.

## What I did not do

I did not change the IP address, the headers, the browser fingerprint or the user agent to get past the block. Those changes would get around the site's protection, and the challenge does not ask for it. I also did not run the test from other countries.

## Proposed strategy

1. **Ask for an approved environment.** The recruiter or the Avianca team can provide a staging site or add my test runner to an allowlist. Automated traffic is then expected, and labels 8 to 18 can run. The suite already reads `BASE_URL` from the environment, so pointing it at staging needs no code change.
2. **Split the suite by what it needs.** Labels 1 to 7 stay as the live smoke test. Labels 8 to 18 go in a separate test that runs only when `BASE_URL` points to an approved environment, with its own marker.
3. **Use the manual run as the reference.** `manual_validation.md` records what each entry should do. Use it to write the expected results and to check the automated test against the real flow.
4. **Test the locators offline.** When an approved session is available, save the HTML of the pages in labels 8 to 18 into a `fixtures/` folder. Offline tests can then check that the locators match the saved pages. These tests do not call the live site, and they are named clearly so nobody reads them as live checks.
5. **Keep the evidence.** On every run that fails, the screenshot and trace go to `test-results/`. Copy the important ones into `docs/evidence/`.

Until labels 8 to 18 are automated, the test marks them as an expected failure. It does not pass silently, and it does not fake the later steps.
