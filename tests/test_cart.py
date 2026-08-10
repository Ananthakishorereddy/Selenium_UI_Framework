"""
test_cart.py — Shopping cart test scenarios.

Test cases:
  TC_CRT_001 — Cart page accessible from navigation
  TC_CRT_002 — Product can be added to cart
  TC_CRT_003 — Cart displays correct product name
  TC_CRT_004 — Multiple products can be added
  TC_CRT_005 — Product quantity defaults to 1
  TC_CRT_006 — Product can be removed from cart
"""

import pytest

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.logger import get_logger

logger = get_logger(__name__)


def _add_product_and_go_to_cart(driver, index: int = 0):
    """Helper: add a product from the listing page and navigate to cart."""
    home = HomePage(driver)
    products = ProductPage(driver)
    cart = CartPage(driver)

    home.go_to_products()
    products.add_product_to_cart_by_index(index)
    products.go_to_cart_from_modal()
    return cart


class TestCart:

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_page_accessible_from_nav(self, driver):
        """TC_CRT_001 — Cart page opens when clicking the Cart nav link."""
        HomePage(driver).go_to_cart()
        assert CartPage(driver).is_cart_page_displayed(), \
            "URL should contain 'view_cart' when cart nav is clicked"

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart(self, driver):
        """TC_CRT_002 — Adding a product from listing increases cart count to >= 1."""
        cart = _add_product_and_go_to_cart(driver, index=0)
        assert cart.get_cart_item_count() >= 1, \
            "Cart should contain at least one item after adding a product"

    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_shows_correct_product_name(self, driver):
        """TC_CRT_003 — Product name in cart is non-empty."""
        cart = _add_product_and_go_to_cart(driver, index=0)
        names = cart.get_product_names()
        assert len(names) > 0, "Cart should show at least one product name"
        assert all(name.strip() for name in names), \
            "All product names in cart should be non-empty strings"

    @pytest.mark.cart
    @pytest.mark.regression
    def test_add_two_different_products(self, driver):
        """TC_CRT_004 — Two different products can be added to the cart."""
        home = HomePage(driver)
        products = ProductPage(driver)
        cart = CartPage(driver)

        home.go_to_products()
        products.add_product_to_cart_by_index(0)
        products.continue_shopping()
        products.add_product_to_cart_by_index(1)
        products.go_to_cart_from_modal()

        count = cart.get_cart_item_count()
        assert count >= 2, \
            f"Cart should have at least 2 items after adding 2 products, got {count}"

    @pytest.mark.cart
    @pytest.mark.regression
    def test_product_quantity_in_cart(self, driver):
        """TC_CRT_005 — Default product quantity in cart is '1'."""
        cart = _add_product_and_go_to_cart(driver, index=0)
        quantities = cart.get_product_quantities()
        assert quantities, "Cart should show quantity for added product"
        assert quantities[0] == "1", \
            f"Default quantity should be 1, got '{quantities[0]}'"

    @pytest.mark.cart
    @pytest.mark.regression
    def test_remove_product_from_cart(self, driver):
        """TC_CRT_006 — Removing the only product leaves the cart empty."""
        cart = _add_product_and_go_to_cart(driver, index=0)
        initial_count = cart.get_cart_item_count()
        assert initial_count >= 1, "Pre-condition: cart must have an item"

        cart.remove_product_by_index(0)
        # Allow DOM update
        import time; time.sleep(1)

        assert cart.is_cart_empty() or cart.get_cart_item_count() < initial_count, \
            "Cart should be empty or have fewer items after removal"
