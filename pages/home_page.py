"""The search form on the home page."""
import re
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
        # The site may already show the right origin. Then there is nothing to change.
        if f"({code})" in self._airport_box("Origin").input_value():
            return
        self._pick_airport("Origin", city, code)

    def choose_destination(self, city: str, code: str) -> None:
        self._pick_airport("Destination", city, code)

    def _airport_box(self, field: str):
        # The input has the combobox role. Its label is also used by the open
        # list, so we filter by role to get only the input.
        return self.page.get_by_role("combobox", name=field, exact=True)

    def _pick_airport(self, field: str, city: str, code: str) -> None:
        box = self._airport_box(field)
        box.click()
        box.fill("")
        # type one key at a time, so the list filters the same way it does for a person
        box.press_sequentially(city, delay=50)
        # pick the option inside this field's list by the airport code
        listbox = self.page.get_by_role("listbox", name=field, exact=True)
        code_pattern = re.compile(rf"\b{re.escape(code)}\b")
        option = listbox.get_by_role("option").filter(has_text=code_pattern).or_(
            listbox.get_by_text(code_pattern)
        )
        option.first.click()

    def choose_departure(self, day: date) -> None:
        # The calendar shows two months, so the same day number appears twice.
        # Each day button has a data-date that starts with the full date.
        day_button = self.page.locator(
            f'button[data-name="dayCell"][data-date^="{day.isoformat()}"]'
        )
        expect(day_button).to_be_enabled()
        day_button.click()

    def _adults_row(self):
        return self.page.get_by_text("Adults", exact=True).locator("xpath=../..")

    def set_adults(self, total: int) -> None:
        row = self._adults_row()
        plus = row.get_by_role("button", name="Increase", exact=True)
        minus = row.get_by_role("button", name="Decrease", exact=True)
        # the row text ends with the current count, for example "Adults From 15 years old 1"
        current = int(row.inner_text().split()[-1])
        while current < total:
            plus.click()
            current += 1
        while current > total:
            minus.click()
            current -= 1

    def expect_adults(self, total: int) -> None:
        row = self._adults_row()
        expect(row.get_by_text(str(total), exact=True)).to_be_visible()
        expect(row.get_by_role("button", name="Increase", exact=True)).to_be_enabled()
        expect(row.get_by_role("button", name="Decrease", exact=True)).to_be_enabled()

    def confirm_passengers(self) -> None:
        self.page.get_by_role("button", name="Confirm", exact=True).click()

    def search(self) -> None:
        self.page.get_by_role("button", name="Search", exact=True).click()

    def _passenger_count(self):
        # the Passengers field shows the label and, next to it, the total
        return self.page.get_by_text("Passengers", exact=True).locator("xpath=following-sibling::div[1]")

    def expect_summary(self, origin_code: str, destination_code: str, adults: int) -> None:
        # origin and destination live in input fields, so we read their values
        expect(self._airport_box("Origin")).to_have_value(re.compile(rf"\({re.escape(origin_code)}\)"))
        expect(self._airport_box("Destination")).to_have_value(re.compile(rf"\({re.escape(destination_code)}\)"))
        expect(self._passenger_count()).to_have_text(str(adults))
        # the passenger dropdown is closed
        expect(self.page.get_by_text("Who's flying")).to_be_hidden()
