"""
CartPage — covers /view_cart page actions and assertions.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    # ------------------------------------------------------------------ #
    #  Locators
    # ------------------------------------------------------------------ #
    CART_TABLE = (By.ID, "cart_info_table")
    CART_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".cart_description h4 a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".cart_price p")
    PRODUCT_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity button")
    PRODUCT_TOTALS = (By.CSS_SELECTOR, ".cart_total_price")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "a.cart_quantity_delete")
    EMPTY_CART_MESSAGE = (By.ID, "empty_cart")
    PROCEED_TO_CHECKOUT_BTN = (By.CSS_SELECTOR, "a.btn.btn-default.check_out")

    # Checkout modal (when not logged in)
    REGISTER_LOGIN_LINK = (By.XPATH, "//u[normalize-space()='Register / Login']")

    # ------------------------------------------------------------------ #
    #  Actions
    # ------------------------------------------------------------------ #

    def is_cart_page_displayed(self) -> bool:
        return self.wait.wait_for_url_contains("view_cart")

    def get_cart_item_count(self) -> int:
        try:
            rows = self.get_all_elements(self.CART_ROWS)
            return len(rows)
        except Exception:
            return 0

    def get_product_names(self) -> list:
        return self.get_all_texts(self.PRODUCT_NAMES)

    def get_product_prices(self) -> list:
        return self.get_all_texts(self.PRODUCT_PRICES)

    def get_product_quantities(self) -> list:
        return self.get_all_texts(self.PRODUCT_QUANTITIES)

    def get_product_totals(self) -> list:
        return self.get_all_texts(self.PRODUCT_TOTALS)

    def remove_product_by_index(self, index: int = 0):
        """Click the delete (×) button for the product at the given row index."""
        self.logger.info(f"Removing cart item at index {index}")
        delete_buttons = self.get_all_elements(self.DELETE_BUTTONS)
        if index < len(delete_buttons):
            delete_buttons[index].click()
        else:
            raise IndexError(f"No delete button at index {index}")

    def is_cart_empty(self) -> bool:
        return self.is_displayed(self.EMPTY_CART_MESSAGE)

    def proceed_to_checkout(self):
        self.logger.info("Clicking Proceed To Checkout")
        self.click(self.PROCEED_TO_CHECKOUT_BTN)

    def go_to_register_login_from_checkout_modal(self):
        """In the checkout popup for non-logged-in users, click Register/Login."""
        self.click(self.REGISTER_LOGIN_LINK)
