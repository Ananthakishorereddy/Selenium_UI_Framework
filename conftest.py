"""
conftest.py — root-level pytest fixtures and hooks.

Key responsibilities:
  - CLI option injection (--browser, --headless, --env)
  - WebDriver lifecycle management per test function
  - Screenshot capture on test failure
  - Shared config/session scope fixtures
"""

import os
import pytest
from datetime import datetime

from utils.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger("conftest")

# ------------------------------------------------------------------ #
#  CLI options
# ------------------------------------------------------------------ #

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser: chrome | firefox | edge (overrides config.yaml)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Target environment: qa | staging | headless_ci"
    )


# ------------------------------------------------------------------ #
#  Session-scoped config (loaded once per run)
# ------------------------------------------------------------------ #

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    logger.info(f"Loading config for environment: '{env}'")
    return ConfigReader(env)


# ------------------------------------------------------------------ #
#  Function-scoped driver (fresh browser per test)
# ------------------------------------------------------------------ #

@pytest.fixture(scope="function")
def driver(request, config):
    # Resolve browser: CLI flag > config.yaml
    browser = request.config.getoption("--browser") or config.get_browser()
    headless = request.config.getoption("--headless") or config.is_headless()

    logger.info(f"Starting {browser} driver | headless={headless}")
    _driver = DriverFactory.get_driver(browser=browser, headless=headless)
    _driver.implicitly_wait(0)          # rely on explicit waits only
    _driver.maximize_window()
    _driver.get(config.get_base_url())
    logger.info(f"Opened URL: {config.get_base_url()}")

    yield _driver

    # ---- teardown ---- #
    _capture_screenshot_on_failure(request, _driver)

    logger.info("Closing driver")
    _driver.quit()


# ------------------------------------------------------------------ #
#  Screenshot on failure
# ------------------------------------------------------------------ #

def _capture_screenshot_on_failure(request, driver):
    """Save screenshot if the test function itself failed."""
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        screenshot_dir = os.path.join("reports", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = request.node.name.replace("[", "_").replace("]", "_")
        path = os.path.join(screenshot_dir, f"FAIL_{safe_name}_{timestamp}.png")
        try:
            driver.save_screenshot(path)
            logger.error(f"Screenshot saved → {path}")
        except Exception as e:
            logger.warning(f"Could not save screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach the test phase result to the item so fixtures can read it."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
