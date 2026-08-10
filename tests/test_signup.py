"""
test_signup.py — User registration test scenarios.

Test cases:
  TC_SGN_001 — Login/Signup page shows both sections
  TC_SGN_002 — New user can complete full registration
  TC_SGN_003 — Existing email triggers error
  TC_SGN_004 — Registered account can be deleted
"""

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.helpers import load_test_data, generate_random_email
from utils.logger import get_logger

logger = get_logger(__name__)
data = load_test_data()


@pytest.fixture(autouse=True)
def navigate_to_login(driver):
    HomePage(driver).go_to_login_page()


class TestSignup:

    @pytest.mark.smoke
    def test_signup_section_is_visible(self, driver):
        """TC_SGN_001 — The 'New User Signup' section is visible on /login."""
        assert LoginPage(driver).is_signup_section_displayed(), \
            "Signup section heading should be visible"

    @pytest.mark.smoke
    @pytest.mark.signup
    def test_new_user_full_registration(self, driver):
        """TC_SGN_002 — Complete end-to-end user registration flow."""
        user = data["new_user"]
        email = generate_random_email()

        login_page = LoginPage(driver)
        signup_page = SignupPage(driver)
        home = HomePage(driver)

        # Step 1 — name + email on login page
        login_page.initiate_signup(user["name"], email)
        assert signup_page.is_signup_form_displayed(), \
            "Account info form should appear after submitting name + email"

        # Step 2 — account details
        signup_page.fill_account_info(
            password=user["password"],
            day=user["day"],
            month=user["month"],
            year=user["year"],
            subscribe_newsletter=True,
        )

        # Step 3 — address details
        signup_page.fill_address_info(
            first_name=user["first_name"],
            last_name=user["last_name"],
            company=user["company"],
            address1=user["address1"],
            address2=user["address2"],
            country=user["country"],
            state=user["state"],
            city=user["city"],
            zipcode=user["zipcode"],
            mobile=user["mobile"],
        )

        # Step 4 — submit & verify
        signup_page.submit_create_account()
        assert signup_page.is_account_created(), \
            "'Account Created!' confirmation should be displayed"

        # Step 5 — continue and verify auto-login
        signup_page.continue_after_creation()
        # Wait for redirect back to home page, then check logged-in state
        signup_page.wait.wait_for_url_to_be("https://automationexercise.com/")
        assert home.is_user_logged_in(), \
            "User should be automatically logged in after registration"

        # Cleanup — delete the test account
        home.delete_account()
        assert signup_page.is_account_deleted(), \
            "'Account Deleted!' confirmation should appear after deletion"

    @pytest.mark.signup
    @pytest.mark.regression
    def test_signup_with_existing_email_shows_error(self, driver):
        """TC_SGN_003 — Registering with an email that already exists shows an error."""
        existing_email = data["valid_user"]["email"]
        LoginPage(driver).initiate_signup("Existing User", existing_email)
        assert LoginPage(driver).is_email_exists_error_displayed(), \
            "Error message should appear when registering with an existing email"
