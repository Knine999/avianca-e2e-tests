"""Code that every page object needs."""
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from utils import config

COOKIE_BANNER_WAIT_MS = 8_000


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(config.BASE_URL, wait_until="domcontentloaded")

    def accept_cookies_if_shown(self) -> None:
        # The cookie banner (OneTrust) covers the search form. On the English
        # site, "Accept" is the button that closes it. "Set configuration"
        # opened a panel and did not close the banner in our runs.
        banner = self.page.locator("#onetrust-consent-sdk")
        try:
            banner.wait_for(state="visible", timeout=COOKIE_BANNER_WAIT_MS)
        except PlaywrightTimeoutError:
            return  # no banner, nothing to close
        self.page.locator("#onetrust-accept-btn-handler").click()
        banner.wait_for(state="hidden", timeout=config.NAVIGATION_TIMEOUT_MS)
