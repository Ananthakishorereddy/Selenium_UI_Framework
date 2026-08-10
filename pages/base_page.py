"""
BasePage — foundation class for all page objects.
Encapsulates common Selenium actions so page objects stay clean and DRY.
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
from utils.waits import WaitUtils
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtils(driver)
        self.logger = get_logger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    #  Core interactions
    # ------------------------------------------------------------------ #

    def click(self, locator: tuple):
        """Wait for element to be clickable, then click it."""
        self.logger.debug(f"Click → {locator}")
        element = self.wait.wait_for_element_clickable(locator)
        element.click()

    def js_click(self, locator: tuple):
        """Click via JavaScript — useful when overlapping elements block normal click."""
        element = self.wait.wait_for_element_present(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator: tuple, text: str):
        """Clear the field and type the given text."""
        self.logger.debug(f"Type '{text}' → {locator}")
        element = self.wait.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        element = self.wait.wait_for_element_visible(locator)
        return element.text.strip()

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Return a specific HTML attribute value from an element."""
        element = self.wait.wait_for_element_present(locator)
        return element.get_attribute(attribute)

    def is_displayed(self, locator: tuple) -> bool:
        """Return True if element is visible, False otherwise (no exception)."""
        try:
            element = self.wait.wait_for_element_visible(locator)
            return element.is_displayed()
        except Exception:
            return False

    def is_present(self, locator: tuple) -> bool:
        """Return True if element exists in DOM (may be hidden)."""
        try:
            self.wait.wait_for_element_present(locator)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Scroll & hover
    # ------------------------------------------------------------------ #

    def scroll_to_element(self, locator: tuple):
        """Scroll the element into the viewport."""
        element = self.wait.wait_for_element_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        return element

    def scroll_to_bottom(self):
        """Scroll to the very bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def hover(self, locator: tuple):
        """Move the mouse to element (triggers hover menus)."""
        element = self.wait.wait_for_element_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    # ------------------------------------------------------------------ #
    #  Dropdowns
    # ------------------------------------------------------------------ #

    def select_by_visible_text(self, locator: tuple, text: str):
        """Select a <select> dropdown option by its visible text."""
        element = self.wait.wait_for_element_visible(locator)
        Select(element).select_by_visible_text(text)

    def select_by_value(self, locator: tuple, value: str):
        """Select a <select> dropdown option by its value attribute."""
        element = self.wait.wait_for_element_visible(locator)
        Select(element).select_by_value(value)

    # ------------------------------------------------------------------ #
    #  Page info
    # ------------------------------------------------------------------ #

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def get_all_elements(self, locator: tuple) -> list:
        """Return a list of all matching WebElements."""
        self.wait.wait_for_element_present(locator)
        return self.driver.find_elements(*locator)

    def get_all_texts(self, locator: tuple) -> list:
        """Return a list of text values from all matching elements."""
        elements = self.get_all_elements(locator)
        return [el.text.strip() for el in elements]
