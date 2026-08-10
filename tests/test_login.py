"""
test_login.py — Login & Logout test scenarios.

Test cases:
  TC_LGN_001 — Login page is displayed
  TC_LGN_002 — Valid login succeeds
  TC_LGN_003 — Invalid credentials show error
  TC_LGN_004 — Parametrized invalid input combinations
  TC_LGN_005 — Logout redirects to login page
"""

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.helpers import load_test_data
from utils.logger import get_logger

logger = get_logger(__name__)
data = load_test_data()


@pytest.fixture(autouse=True)
def navigate_to_login(driver):
    """Navigate to the Login/Signup page before each test in this module."""
    HomePage(driver).go_to_login_page()


class TestLoginPage:

    @pytest.mark.smoke
    def test_login_page_is_displayed(self, driver):
        """TC_LGN_001 — Login page elements render correctly."""
        login = LoginPage(driver)
        assert login.is_login_page_displayed(), \
            "Login heading should be visible on /login"

    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, driver):
        """TC_LGN_002 — User can log in with correct credentials."""
        creds = data["valid_user"]
        LoginPage(driver).login(creds["email"], creds["password"])
        assert HomePage(driver).is_user_logged_in(), \
            "Nav bar should show 'Logged in as <name>' after valid login"

    @pytest.mark.login
    @pytest.mark.regression
    def test_invalid_credentials_show_error(self, driver):
        """TC_LGN_003 — Error message displayed for wrong email/password."""
        LoginPage(driver).login("wrong@example.com", "BadPass999!")
        login = LoginPage(driver)
        assert login.is_login_error_displayed(), \
            "Error message should appear for invalid credentials"

    @pytest.mark.login
    @pytest.mark.regression
    @pytest.mark.parametrize("email,password", [
        ("", "Password123"),           # missing email
        ("valid@test.com", ""),        # missing password
        ("notanemail", "Password123"), # malformed email
        ("a@b.com", "x"),             # too short password
    ])
    def test_login_with_invalid_inputs(self, driver, email, password):
        """TC_LGN_004 — User is NOT logged in after submitting invalid input."""
        LoginPage(driver).login(email, password)
        assert not HomePage(driver).is_user_logged_in(), \
            f"User should NOT be logged in with email='{email}' password='{password}'"

    @pytest.mark.login
    @pytest.mark.regression
    def test_logout_redirects_to_login(self, driver):
        """TC_LGN_005 — Logout sends user back to the login page."""
        creds = data["valid_user"]
        home = HomePage(driver)
        LoginPage(driver).login(creds["email"], creds["password"])
        assert home.is_user_logged_in(), "Pre-condition: user must be logged in"

        home.logout()
        assert LoginPage(driver).is_login_page_displayed(), \
            "User should land on the login page after logout"
