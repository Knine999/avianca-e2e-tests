"""The search form on the home page."""
from datetime import date

from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    # labels as they appear on the English site
    ROUND_TRIP = "Round trip"
    ONE_WAY = "One way"
    RETURN = "Return"

    def select_trip_type(self, label: str) -> None:
        self.page.get_by_text(label, exact=True).first.click()

    def choose_origin(self, city: str, code: str) -> None:
        self.page.get_by_text("Origin", exact=True).first.click()
        self.page.get_by_role("textbox").first.fill(city)
        self.page.get_by_text(f"({code})").first.click()

    def choose_destination(self, city: str, code: str) -> None:
        self.page.get_by_text("Destination", exact=True).first.click()
        self.page.get_by_role("textbox").first.fill(city)
        self.page.get_by_text(f"({code})").first.click()

    def choose_departure(self, day: date) -> None:
        # TODO: the same day number can show up twice when the calendar shows two months
        self.page.get_by_role("button", name=str(day.day), exact=True).first.click()

    def set_adults(self, total: int) -> None:
        # The plus and minus buttons have no accessible names, so we find them
        # by their position in the passenger row. TODO: find a stable locator.
        row = self.page.get_by_text("Adults", exact=True).locator("xpath=../..")
        current = int(row.inner_text().split()[-1]) if row.count() else 1
        plus = row.get_by_role("button").last
        minus = row.get_by_role("button").first
        while current < total:
            plus.click()
            current += 1
        while current > total:
            minus.click()
            current -= 1

    def confirm_passengers(self) -> None:
        self.page.get_by_role("button", name="Confirm", exact=True).click()

    def search(self) -> None:
        self.page.get_by_role("button", name="Search", exact=True).click()

    def expect_summary(self, origin_code: str, destination_code: str, adults: int) -> None:
        expect(self.page.get_by_text(f"({origin_code})")).to_be_visible()
        expect(self.page.get_by_text(f"({destination_code})")).to_be_visible()
        expect(self.page.get_by_text(f"{adults} Adults")).to_be_visible()
