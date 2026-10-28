"""Test settings. Change values here, not inside the tests."""
import os
from datetime import date, datetime, timedelta, timezone

# We test the English site. Its default origin depends on where the visitor is
# (Miami when testing from the US), so the origin is always set explicitly.
BASE_URL = os.getenv("BASE_URL", "https://www.avianca.com/en")

ORIGIN_CITY = "Miami"
ORIGIN_CODE = "MIA"
DESTINATION_CITY = "San Andres"
DESTINATION_CODE = "ADZ"

# days from today until the flight
DAYS_AHEAD = 14

# pause after each browser action, in milliseconds. 0 means full speed.
SLOW_MO_MS = int(os.getenv("SLOW_MO_MS", "0"))

# the booking engine is slow, so we wait longer than the default
DEFAULT_TIMEOUT_MS = 15_000
NAVIGATION_TIMEOUT_MS = 45_000


def departure_date() -> date:
    """Departure date in Bogota time, so it never falls in the past."""
    bogota = timezone(timedelta(hours=-5))
    return datetime.now(bogota).date() + timedelta(days=DAYS_AHEAD)
