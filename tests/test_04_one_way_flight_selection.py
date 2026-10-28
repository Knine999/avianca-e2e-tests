"""Test 4 from the challenge: search a one-way flight.

Steps 1 to 7 are automated on the English site. Steps 8 to 18 are not
automated yet, so the test is marked as an expected failure from step 8.
"""
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils import config


@pytest.mark.e2e
def test_one_way_flight_search(page):
    home = HomePage(page)

    # Step 1: open the site. Round trip is selected by default.
    home.open()
    home.accept_cookies_if_shown()
    expect(page.get_by_text(HomePage.ROUND_TRIP, exact=True)).to_be_visible()

    # Step 2: One way hides the Return field.
    home.select_trip_type(HomePage.ONE_WAY)
    expect(page.get_by_text(HomePage.RETURN, exact=True)).to_be_hidden()

    # Steps 3 and 4: origin and destination. The origin is set on purpose,
    # because the site picks it from the visitor's location.
    home.choose_origin(config.ORIGIN_CITY, config.ORIGIN_CODE)
    home.choose_destination(config.DESTINATION_CITY, config.DESTINATION_CODE)

    # Step 5: departure date.
    home.choose_departure(config.departure_date())

    # Steps 6 and 7: two adults, confirm, then search.
    home.set_adults(2)
    expect(page.get_by_text("2 Adults")).to_be_visible()
    home.confirm_passengers()
    home.expect_summary(config.ORIGIN_CODE, config.DESTINATION_CODE, adults=2)
    home.search()
    expect(page).to_have_url(
        re.compile(r"booking\.avianca\.com/av/booking/avail"),
        timeout=config.NAVIGATION_TIMEOUT_MS,
    )

    # Steps 8 to 18 are not mapped yet.
    pytest.xfail("steps 8 to 18 are not automated yet")
