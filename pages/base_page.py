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
        # The cookie banner (OneTrust) covers the search form. We wait for the
        # Accept button itself, because the banner's outer container does not
        # count as visible even when the banner is on screen.
        accept = self.page.locator("#onetrust-accept-btn-handler").or_(
            self.page.get_by_role("button", name="Accept", exact=True)
        ).first
        try:
            accept.wait_for(state="visible", timeout=COOKIE_BANNER_WAIT_MS)
        except PlaywrightTimeoutError:
            return  # no banner, nothing to close
        accept.click()
        accept.wait_for(state="hidden", timeout=config.NAVIGATION_TIMEOUT_MS)
