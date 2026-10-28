# Requirements and build guide

This page lists what you need to run the project and the order to build it from zero.

## What you need

- Windows 10 or 11 with PowerShell
- Python 3.12. Python 3.14 failed to install the pinned packages, because there is no prebuilt `greenlet` wheel for them. Python 3.13 was not tested.
- Git
- Internet access to avianca.com and to PyPI (for `pip`)

## Dependencies

Listed in `requirements.txt`.

| Package | Version | Why it is here |
|---|---|---|
| pytest | 8.3.3 | Runs the tests and handles markers, fixtures and reports |
| pytest-playwright | 0.5.2 | Connects Playwright to pytest. Provides the `page` fixture and the `--headed` flag |
| playwright | 1.47.0 | Drives the browser |

The versions are pinned on purpose. A newer Playwright can change how locators and waits behave, and the tests would break without any change in the project.

## Build from zero

1. Create the project folder and run `git init`.
2. Create a virtual environment with Python 3.12 and install `requirements.txt`.
3. Install the browser with `python -m playwright install chromium`.
4. Write `utils/config.py` first. It holds the site URL, origin, destination, the date rule and the timeouts. Keeping these values in one place means the tests do not change when the trip or the site changes.
5. Write `conftest.py`. It sets the desktop size, the language, the timezone and the `page` fixture.
6. Find the locators you need. The quickest way is the recorder: `python -m playwright codegen https://www.avianca.com/en`. It opens a browser and writes the locator for each click you make. Use the output as a starting point, not as the final code.
7. Write `pages/base_page.py` for shared code, such as the cookie banner, and `pages/home_page.py` for the search form.
8. Write the test as numbered steps that match the challenge document, one comment per step.
9. Run it with `pytest -m e2e -s`, watch the browser and fix any locator that does not match the real page. The browser is always visible because `pytest.ini` includes `--headed`.
10. Mark the steps you did not automate, so the report shows where the test stops.
11. Update the README with the status and the commands.

## Why Python and not JavaScript

Both languages have official Playwright support with the same browser features, so the browser work does not decide the language. The reasons for Python in this project are these:

- **pytest covers more out of the box.** Test discovery, markers (`-m e2e`), fixtures, the `--headed` option and failure screenshots all work without extra setup. With JavaScript, Playwright Test does the same job with its own runner and config file.
- **The tests read top to bottom.** Each numbered step is a few lines in order, which matches the challenge document.
- **Fewer tools to install.** Python needs one interpreter and one virtual environment. JavaScript needs Node.js, a package manager and a lockfile.

JavaScript would be the better choice if the team reviewing this already works in Node.js. The steps, the locators and the test data would carry over almost unchanged.

Trade-off: Python needs a specific version (3.12 here) and a virtual environment. Forgetting to activate the environment is the most common setup problem.
