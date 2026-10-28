"""Test 4 from the challenge: one-way flight selection.

The challenge lists 20 entries under labels 1 to 18. Labels 13 and 16 each
appear twice. The comments below use the challenge labels.

Automated: labels 1 to 7. Label 7 only checks the booking URL, because the
results page stays blank in the automated browser. Labels 8 to 18 are not
automated for the same reason. See docs/blocker.md.
"""
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils import config


@pytest.mark.e2e
def test_one_way_flight_selection(page):
    home = HomePage(page)

    # Label 1: open the site. The trip type defaults to Round trip.
    home.open()
    home.accept_cookies_if_shown()
    expect(page.get_by_text(HomePage.ROUND_TRIP, exact=True)).to_be_visible()

    # Label 2: choose One way. The Return field is not displayed.
    home.select_trip_type(HomePage.ONE_WAY)
    expect(page.get_by_text(HomePage.RETURN, exact=True)).to_be_hidden()

    # Label 3: choose the destination. We also set the origin to Miami, because
    # the default origin depends on the visitor's location.
    home.choose_origin(config.ORIGIN_CITY, config.ORIGIN_CODE)
    home.choose_destination(config.DESTINATION_CITY, config.DESTINATION_CODE)

    # Label 4: choose a departure date.
    home.choose_departure(config.departure_date())

    # Label 5: set the adult count to 2.
    home.set_adults(2)
    home.expect_adults(2)

    # Label 6: confirm the passengers.
    home.confirm_passengers()
    home.expect_summary(config.ORIGIN_CODE, config.DESTINATION_CODE, adults=2)

    # Label 7: search. The booking page opens.
    home.search()
    expect(page).to_have_url(
        re.compile(r"booking\.avianca\.com/av/booking/avail"),
        timeout=config.NAVIGATION_TIMEOUT_MS,
    )

    # Labels 8 to 18 are not automated yet. The challenge lists 20 entries because
    # labels 13 and 16 repeat.
    pytest.xfail("labels 8 to 18 are not automated: the results page stays blank in the automated browser")
