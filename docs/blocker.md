# Blocker: Access Denied during the search flow

## Summary

Test 4 automates steps 1 to 7 of the challenge. After step 7 (Search), the site blocks the automated browser, so steps 8 to 18 cannot be reached or mapped. The test is marked as an expected failure (xfail) from step 8, so the report shows where it stops.

## What we saw

- **Access Denied (Akamai bot protection).** In one run the browser was sent to the Spanish site (`/es`) and the page returned "Access Denied", with a reference number and a link to `errors.edgesuite.net`. Evidence: [02_access_denied_spanish_site.png](evidence/02_access_denied_spanish_site.png).
- **Cookie banner over the search form.** In another run the English home page loaded, but the OneTrust cookie banner stayed on screen and covered the page. Our click handling for the banner was changed after this run. Evidence: [01_english_home_cookie_banner.png](evidence/01_english_home_cookie_banner.png).

The first screenshot shows the English home page with the origin already set to Miami (MIA), the currency in USD, and the banner with "Set configuration" and "Accept" buttons.

## Steps not automated

These steps depend on pages that we cannot reach while the block is active:

| Step | What it covers | Status |
|---|---|---|
| 8 | Choose the cheapest flight in the list | Not mapped |
| 9 | Pick the cheapest fare price | Not mapped |
| 10 | Upgrade pop-up | Not mapped |
| 11 | Trip summary, continue | Not mapped |
| 12 | Passenger details | Not mapped |
| 13 | Contact details and privacy checkbox | Not mapped |
| 14 | Baggage options (only on some itineraries) | Not mapped |
| 15 | Priority boarding | Not mapped |
| 16 | Go to payment | Not mapped |
| 17 | Check the purchase summary | Not mapped |
| 18 | Stop before payment | Not mapped |

The step names above come from our working notes. Check them against the challenge document before submitting.

## What we did not do

We did not change the IP address, the headers, the browser fingerprint or the user agent to get past the block. Those changes would get around the site's protection, and the challenge does not ask for it. We also did not run the test from other countries.

## Proposed strategy

1. **Ask for an approved environment.** The recruiter or the Avianca team can provide a staging site or add our test runner to an allowlist. Automated traffic is then expected, and the full flow can run. The suite already reads `BASE_URL` from the environment, so pointing it at staging needs no code change.
2. **Split the suite by what it needs.** Steps 1 to 7 stay as the live smoke test. Steps 8 to 18 go in a separate test that runs only when `BASE_URL` points to an approved environment. The `e2e` marker stays for both, and the second test gets its own marker.
3. **Test the locators offline.** When an approved session is available, save the HTML of each page in steps 8 to 18 into a `fixtures/` folder. Offline tests can then check that the locators match the saved pages. These tests do not call the live site, and they are named clearly so nobody reads them as live checks.
4. **Keep the evidence.** On every run that fails, the screenshot and trace go to `test-results/`. Copy the important ones into `docs/evidence/` so the blocker stays documented with the date it was seen.

Until one of these is in place, the test reports the blocker as an expected failure. It does not pass silently, and it does not fake the later steps.
