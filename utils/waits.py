"""
WaitUtils — explicit wait wrappers to avoid hardcoded sleeps.
All page objects use this instead of implicit waits or time.sleep().
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

DEFAULT_TIMEOUT = 15


class WaitUtils:
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    def wait_for_element_visible(self, locator: tuple):
        """Wait until element is visible in the DOM and on screen."""
        return self._wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: tuple):
        """Wait until element is visible and enabled (ready to click)."""
        return self._wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_present(self, locator: tuple):
        """Wait until element exists in DOM (may not be visible)."""
        return self._wait.until(EC.presence_of_element_located(locator))

    def wait_for_all_elements_present(self, locator: tuple):
        """Wait for all matching elements to be in the DOM."""
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_element_invisible(self, locator: tuple):
        """Wait until element disappears from screen."""
        return self._wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_url_contains(self, text: str) -> bool:
        """Wait until the current URL contains the given text."""
        return self._wait.until(EC.url_contains(text))

    def wait_for_url_to_be(self, url: str) -> bool:
        """Wait until the current URL is exactly the given URL."""
        return self._wait.until(EC.url_to_be(url))

    def wait_for_text_in_element(self, locator: tuple, text: str) -> bool:
        """Wait until element contains expected text."""
        return self._wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_title_contains(self, text: str) -> bool:
        """Wait until the page title contains the given text."""
        return self._wait.until(EC.title_contains(text))

    def wait_for_alert_present(self):
        """Wait until a JavaScript alert is present."""
        return self._wait.until(EC.alert_is_present())
