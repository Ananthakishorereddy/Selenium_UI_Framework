"""
test_product.py — Product listing, search, and detail page scenarios.

Test cases:
  TC_PRD_001 — All Products page loads
  TC_PRD_002 — Product list is non-empty
  TC_PRD_003 — Search returns results (parametrized)
  TC_PRD_004 — Search results are relevant to keyword
  TC_PRD_005 — Product detail page shows name and price
"""

import pytest

from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.helpers import load_test_data
from utils.logger import get_logger

logger = get_logger(__name__)
data = load_test_data()


@pytest.fixture(autouse=True)
def navigate_to_products(driver):
    HomePage(driver).go_to_products()


class TestProducts:

    @pytest.mark.smoke
    def test_products_page_is_displayed(self, driver):
        """TC_PRD_001 — All Products page heading is visible."""
        assert ProductPage(driver).is_products_page_displayed(), \
            "'All Products' heading should be visible"

    @pytest.mark.smoke
    @pytest.mark.product
    def test_product_list_is_not_empty(self, driver):
        """TC_PRD_002 — At least one product card is rendered."""
        count = ProductPage(driver).get_product_count()
        assert count > 0, "Products page should display at least one product"
        logger.info(f"Found {count} products on the page")

    @pytest.mark.product
    @pytest.mark.regression
    @pytest.mark.parametrize("keyword", ["dress", "top", "shirt"])
    def test_search_returns_results(self, driver, keyword):
        """TC_PRD_003 — Searching a keyword shows the 'Searched Products' section."""
        page = ProductPage(driver)
        page.search_product(keyword)
        assert page.is_search_results_displayed(), \
            f"'Searched Products' heading should appear when searching for '{keyword}'"

    @pytest.mark.product
    @pytest.mark.regression
    def test_search_results_are_relevant(self, driver):
        """TC_PRD_004 — Search results contain at least one item matching the keyword."""
        keyword = "dress"
        page = ProductPage(driver)
        page.search_product(keyword)
        names = page.get_product_names()
        assert len(names) > 0, "Search results list should not be empty"
        matched = [n for n in names if keyword.lower() in n.lower()]
        assert len(matched) > 0, \
            f"At least one result should contain '{keyword}' (found: {names})"

    @pytest.mark.product
    @pytest.mark.regression
    def test_product_detail_page_shows_info(self, driver):
        """TC_PRD_005 — Product detail page shows a non-empty name and price."""
        page = ProductPage(driver)
        page.open_product_detail(index=0)
        name = page.get_product_detail_name()
        price = page.get_product_detail_price()
        assert name, "Product detail page should display a product name"
        assert price, "Product detail page should display a price"
        logger.info(f"Product: '{name}' | Price: '{price}'")
