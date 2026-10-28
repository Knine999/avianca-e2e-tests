# Avianca E2E tests

This is my automation for Test 4 of the QA technical challenge: a one-way flight selection on avianca.com. I wrote it with Python, Playwright and pytest.

## What is covered

The challenge lists 20 entries under labels 1 to 18. Labels 13 and 16 each appear twice.

- **Labels 1 to 7 (automated):** open the site, choose One way, choose the destination, set the departure date, set two adults, confirm, and search. The test checks the main result of each label, not every expected result. Known gaps:
  - Label 2 checks that the Return field is hidden, but not that the selector shows "One way".
  - Label 4 does not check the date format. On the English site the Departure field shows MM/DD/YYYY (for example 11/10/2026 for November 10), while the challenge expects DD/MM/YYYY. I report this as a difference instead of failing the test on it.
  - Label 7 checks the booking URL, not the list of outbound flights, because the results page stays blank in the automated browser.
- **Labels 8 to 18 (not automated):** the test is marked as an expected failure from label 8, so the report shows where it stops.

## Status and blocker

In my automated runs, labels 1 to 6 pass and the search opens the booking URL with the right values, but the results page stays blank in the automated browser, so no flights are shown. The page loads only a script with an obscured path, which looks like Avianca's bot protection (Akamai). In other runs the site returned an \"Access Denied\" page. I did not try to get around either one. Because of this, label 7 is only partly checked and labels 8 to 18 are not automated. I walked through the whole flow by hand in Chrome, and there the results page works. The details, the evidence and my proposed approach are in [docs/blocker.md](docs/blocker.md). The manual results are in [docs/manual_validation.md](docs/manual_validation.md).

The site notes are in [docs/exploration.md](docs/exploration.md).

## Use of AI as a support tool

I used an AI assistant for code review, to explain errors when a test failed, to review the wording of this documentation, and to help draft the documents in `docs/`. I read every change, ran the code myself and decided what to test, which locators to use and how long to wait.

## Requirements

- Windows with PowerShell
- Python 3.12
- Git

See [docs/requirements.md](docs/requirements.md) for the full list and the steps I followed to build the project from zero.

## Setup

Run these in PowerShell, inside the project folder:

```powershell
py -3.12 -m venv .venv                       # create a virtual environment with Python 3.12
.venv\Scripts\Activate.ps1                   # activate it in this terminal
python -m pip install -r requirements.txt    # install pytest, Playwright and pytest-playwright
python -m playwright install chromium        # download the browser Playwright uses
```

If PowerShell does not let you activate the environment, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

## Running

```powershell
pytest -m e2e                 # run Test 4 without a window
pytest -m e2e --headed -s     # run Test 4 in a visible browser and print the output
```

If a test fails, look in `test-results\` for a screenshot (`.png`) and a trace (`.zip`). Open the trace with:

```powershell
python -m playwright show-trace test-results\<name>.zip
```

## Project structure

- `conftest.py`: browser settings and the `page` fixture
- `pages/base_page.py`: shared code, including the cookie banner
- `pages/home_page.py`: the search form
- `tests/test_04_one_way_flight_selection.py`: Test 4
- `utils/config.py`: origin, destination, dates and timeouts
- `docs/`: requirements, site notes, the manual validation, and the blocker with its evidence

## Known limits

- The challenge asks only for the destination. The test also sets the origin to Miami, so it does not depend on the visitor's location.
- Prices and availability change, so the test checks the flow, not the price.
- The search runs against the production site. The test never pays or books.
- The tests run at desktop size only (1280 x 900).
- I accept all cookies because "Accept" is the only button that closes the banner on the English site.
