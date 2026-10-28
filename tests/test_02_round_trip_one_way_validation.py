"""Test 2 from the challenge: round trip and one way form validation.

All steps stay on the home page, so the bot protection on the results page
does not affect this test.
"""
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.e2e
def test_round_trip_and_one_way_form_validation(page):
    home = HomePage(page)

    # Step 1: open the site. The trip type defaults to Round trip.
    home.open()
    if home.is_blocked():
        pytest.xfail("the home page was blocked by the site's bot protection (Access Denied)")
    home.accept_cookies_if_shown()
    expect(page.get_by_text(HomePage.ROUND_TRIP, exact=True)).to_be_visible()

    # Step 2: click the Return field. The calendar opens.
    home.open_date_field(HomePage.RETURN)
    home.expect_calendar_open()
    home.close_popup()

    # Step 3: choose One way. The Return field is not displayed.
    home.select_trip_type(HomePage.ONE_WAY)
    expect(page.get_by_text(HomePage.RETURN, exact=True)).to_be_hidden()

    # Step 4: choose Round trip again. The Return field is back.
    home.select_trip_type(HomePage.ROUND_TRIP)
    expect(page.get_by_text(HomePage.RETURN, exact=True)).to_be_visible()

    # Step 5: click Destination. The airport list opens.
    home.open_airport_field("Destination")
    home.expect_airport_list_open("Destination")

    # Step 6: type Buenos Aires and choose EZE. The field shows the city.
    home.choose_destination("Buenos Aires", "EZE")
    home.expect_airport("Destination", "EZE")

    # Step 7: search without dates. The calendar opens and both date fields
    # show a red "Required" message.
    home.search()
    home.expect_calendar_open()
    expect(page.get_by_text("Required", exact=True)).to_have_count(2)