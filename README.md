# Avianca E2E tests

This is my automation for Test 4 of the QA technical challenge: a one-way flight search on avianca.com. I wrote it with Python, Playwright and pytest.

## What is covered

- **Test 4 (mandatory):** steps 1 to 7 are automated on the English site, from opening the home page to the flight search.
- **Steps 8 to 18:** not automated. The test is marked as an expected failure from step 8, so the report shows where it stops.

## Status and blocker

Avianca's bot protection (Akamai) blocks the automated browser after the search. Some runs end with an "Access Denied" page, and in others the cookie banner stays on screen. I did not try to get around the block. Steps 8 to 18 depend on the pages behind it, so I could not automate them. The full description, the evidence and my proposed approach are in [docs/blocker.md](docs/blocker.md).

The English version with the Miami origin and the cookie fix still needs a full run. The site notes are in [docs/exploration.md](docs/exploration.md).

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
- `docs/`: requirements, site notes, and the blocker with its evidence

## Known limits

- Prices and availability change, so the test checks the flow, not the price.
- The search runs against the production site. The test never pays or books.
- The tests run at desktop size only (1280 x 900).
- The plus and minus passenger buttons have no accessible names, so I find them by position.
- I accept all cookies because "Accept" is the only button that closes the banner on the English site.

## Blocker and next steps

Steps 8 to 18 are blocked by the site's bot protection after the search. The details, the evidence and the proposed way to handle the flow are in [docs/blocker.md](docs/blocker.md).
