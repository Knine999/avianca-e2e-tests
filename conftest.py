"""Shared pytest setup: browser options and the page each test uses."""
import pytest

from utils import config


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # pytest-playwright controls headless mode, so --headed keeps working
    return {**browser_type_launch_args, "slow_mo": config.SLOW_MO_MS}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Desktop size on purpose. On a small screen the search form opens in a
    # different panel and the locators in this project will not match.
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 900},
        "locale": "en-US",
        "timezone_id": "America/Bogota",
    }


@pytest.fixture
def page(context):
    context.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
    context.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT_MS)
    page = context.new_page()
    yield page
    page.close()
