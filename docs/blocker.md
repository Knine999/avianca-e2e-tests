# Blocker: bot protection in automated runs

## Summary

My automated runs with Playwright are blocked by Avianca's bot protection (Akamai) after the search. My manual walk-through in a normal browser completed the whole flow without that block (see [manual_validation.md](manual_validation.md)). So the block affects automated sessions, not the flow itself.

## What I saw in automated runs

- **Access Denied (Akamai).** In one run the browser was sent to the Spanish site (`/es`) and the page returned "Access Denied", with a reference number and a link to `errors.edgesuite.net`. Evidence: [02_access_denied_spanish_site.png](evidence/02_access_denied_spanish_site.png).
- **Cookie banner over the page.** In another run the English home page loaded, but the OneTrust banner stayed on screen and covered the page. I changed how the test handles the banner after this run. Evidence: [01_english_home_cookie_banner.png](evidence/01_english_home_cookie_banner.png).

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

Labels 8 to 18 are the part of the flow that automation cannot reach. The manual run shows that they work, so the test cases are valid. What fails is the automated session.

## What I did not do

I did not change the IP address, the headers, the browser fingerprint or the user agent to get past the block. Those changes would get around the site's protection, and the challenge does not ask for it. I also did not run the test from other countries.

## Proposed strategy

1. **Ask for an approved environment.** The recruiter or the Avianca team can provide a staging site or add my test runner to an allowlist. Automated traffic is then expected, and labels 8 to 18 can run. The suite already reads `BASE_URL` from the environment, so pointing it at staging needs no code change.
2. **Split the suite by what it needs.** Labels 1 to 7 stay as the live smoke test. Labels 8 to 18 go in a separate test that runs only when `BASE_URL` points to an approved environment, with its own marker.
3. **Use the manual run as the reference.** `manual_validation.md` records what each entry should do. Use it to write the expected results and to check the automated test against the real flow.
4. **Test the locators offline.** When an approved session is available, save the HTML of the pages in labels 8 to 18 into a `fixtures/` folder. Offline tests can then check that the locators match the saved pages. These tests do not call the live site, and they are named clearly so nobody reads them as live checks.
5. **Keep the evidence.** On every run that fails, the screenshot and trace go to `test-results/`. Copy the important ones into `docs/evidence/`.

Until one of these is in place, the test reports the blocker as an expected failure. It does not pass silently, and it does not fake the later steps.
