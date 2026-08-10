"""
ProductPage — covers /products and individual product detail pages.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):

    # ------------------------------------------------------------------ #
    #  Locators — Product listing
    # ------------------------------------------------------------------ #
    ALL_PRODUCTS_HEADING = (By.XPATH, "//h2[normalize-space()='All Products']")
    SEARCHED_PRODUCTS_HEADING = (By.XPATH, "//h2[normalize-space()='Searched Products']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".productinfo h2")
    ADD_TO_CART_OVERLAY_BTNS = (By.CSS_SELECTOR, ".product-overlay .add-to-cart")
    VIEW_PRODUCT_LINKS = (By.XPATH, "//a[contains(text(),'View Product')]")

    # Search
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")

    # Modal after add-to-cart
    MODAL_CONTINUE_BTN = (By.XPATH, "//button[normalize-space()='Continue Shopping']")
    MODAL_VIEW_CART_BTN = (By.XPATH, "//u[normalize-space()='View Cart']")

    # ------------------------------------------------------------------ #
    #  Locators — Product detail
    # ------------------------------------------------------------------ #
    PRODUCT_DETAIL_NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_DETAIL_CATEGORY = (By.XPATH, "//div[@class='product-information']//p[1]")
    PRODUCT_DETAIL_PRICE = (By.CSS_SELECTOR, ".product-information span span")
    PRODUCT_DETAIL_AVAILABILITY = (By.XPATH, "//b[normalize-space()='Availability:']/..")
    ADD_TO_CART_DETAIL_BTN = (By.XPATH, "//button[normalize-space()='Add to cart']")
    QUANTITY_INPUT = (By.ID, "quantity")

    # ------------------------------------------------------------------ #
    #  Actions — listing
    # ------------------------------------------------------------------ #

    def is_products_page_displayed(self) -> bool:
        return self.is_displayed(self.ALL_PRODUCTS_HEADING)

    def get_product_names(self) -> list:
        return self.get_all_texts(self.PRODUCT_NAMES)

    def get_product_count(self) -> int:
        return len(self.get_all_elements(self.PRODUCT_NAMES))

    def search_product(self, keyword: str):
        self.logger.info(f"Searching product: '{keyword}'")
        self.type(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def is_search_results_displayed(self) -> bool:
        return self.is_displayed(self.SEARCHED_PRODUCTS_HEADING)

    def add_product_to_cart_by_index(self, index: int = 0):
        """Hover over a product card and click its 'Add to Cart' overlay button."""
        self.logger.info(f"Adding product at index {index} to cart")
        product_cards = self.get_all_elements((By.CSS_SELECTOR, ".product-image-wrapper"))
        if index >= len(product_cards):
            raise IndexError(f"Product index {index} out of range (total: {len(product_cards)})")
        self.hover((By.CSS_SELECTOR, f".product-image-wrapper:nth-child({index + 1})"))
        btns = self.get_all_elements(self.ADD_TO_CART_OVERLAY_BTNS)
        self.driver.execute_script("arguments[0].click();", btns[index])

    def continue_shopping(self):
        self.click(self.MODAL_CONTINUE_BTN)

    def go_to_cart_from_modal(self):
        self.click(self.MODAL_VIEW_CART_BTN)

    def open_product_detail(self, index: int = 0):
        """Click 'View Product' link for the product at the given index."""
        self.logger.info(f"Opening product detail at index {index}")
        links = self.get_all_elements(self.VIEW_PRODUCT_LINKS)
        links[index].click()

    # ------------------------------------------------------------------ #
    #  Actions — detail page
    # ------------------------------------------------------------------ #

    def get_product_detail_name(self) -> str:
        return self.get_text(self.PRODUCT_DETAIL_NAME)

    def get_product_detail_price(self) -> str:
        return self.get_text(self.PRODUCT_DETAIL_PRICE)

    def set_quantity(self, quantity: int):
        self.type(self.QUANTITY_INPUT, str(quantity))

    def add_to_cart_from_detail(self):
        self.logger.info("Adding product to cart from detail page")
        self.click(self.ADD_TO_CART_DETAIL_BTN)
