"""
SignupPage — covers the full account registration form on automationexercise.com.
Reached after entering name + email on the LoginPage and clicking Signup.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SignupPage(BasePage):

    # ------------------------------------------------------------------ #
    #  Locators — Account Information
    # ------------------------------------------------------------------ #
    ACCOUNT_INFO_HEADING = (By.XPATH, "//b[normalize-space()='Enter Account Information']")
    GENDER_MR = (By.ID, "id_gender1")
    GENDER_MRS = (By.ID, "id_gender2")
    PASSWORD = (By.ID, "password")
    DAY_DROPDOWN = (By.ID, "days")
    MONTH_DROPDOWN = (By.ID, "months")
    YEAR_DROPDOWN = (By.ID, "years")
    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    OPTIN_CHECKBOX = (By.ID, "optin")

    # ------------------------------------------------------------------ #
    #  Locators — Address Information
    # ------------------------------------------------------------------ #
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    COMPANY = (By.ID, "company")
    ADDRESS1 = (By.ID, "address1")
    ADDRESS2 = (By.ID, "address2")
    COUNTRY_DROPDOWN = (By.ID, "country")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    ZIPCODE = (By.ID, "zipcode")
    MOBILE = (By.ID, "mobile_number")

    # ------------------------------------------------------------------ #
    #  Locators — Result
    # ------------------------------------------------------------------ #
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[@data-qa='create-account']")
    ACCOUNT_CREATED_HEADING = (By.XPATH, "//b[normalize-space()='Account Created!']")
    CONTINUE_BUTTON = (By.XPATH, "//a[@data-qa='continue-button']")
    ACCOUNT_DELETED_HEADING = (By.XPATH, "//b[contains(text(),'Account Deleted')]")

    # ------------------------------------------------------------------ #
    #  Actions
    # ------------------------------------------------------------------ #

    def is_signup_form_displayed(self) -> bool:
        return self.is_displayed(self.ACCOUNT_INFO_HEADING)

    def fill_account_info(
        self,
        password: str,
        day: str,
        month: str,
        year: str,
        subscribe_newsletter: bool = False,
        receive_offers: bool = False,
    ):
        """Fill in the account information section of the registration form."""
        self.logger.info("Filling account information")
        self.click(self.GENDER_MR)
        self.type(self.PASSWORD, password)
        self.select_by_visible_text(self.DAY_DROPDOWN, day)
        self.select_by_visible_text(self.MONTH_DROPDOWN, month)
        self.select_by_visible_text(self.YEAR_DROPDOWN, year)
        if subscribe_newsletter:
            self.click(self.NEWSLETTER_CHECKBOX)
        if receive_offers:
            self.click(self.OPTIN_CHECKBOX)

    def fill_address_info(
        self,
        first_name: str,
        last_name: str,
        company: str,
        address1: str,
        country: str,
        state: str,
        city: str,
        zipcode: str,
        mobile: str,
        address2: str = "",
    ):
        """Fill in the address / personal details section."""
        self.logger.info(f"Filling address info for {first_name} {last_name}")
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.COMPANY, company)
        self.type(self.ADDRESS1, address1)
        if address2:
            self.type(self.ADDRESS2, address2)
        self.select_by_visible_text(self.COUNTRY_DROPDOWN, country)
        self.type(self.STATE, state)
        self.type(self.CITY, city)
        self.type(self.ZIPCODE, zipcode)
        self.type(self.MOBILE, mobile)

    def submit_create_account(self):
        self.logger.info("Submitting Create Account")
        self.scroll_to_element(self.CREATE_ACCOUNT_BUTTON)
        self.click(self.CREATE_ACCOUNT_BUTTON)

    def is_account_created(self) -> bool:
        return self.is_displayed(self.ACCOUNT_CREATED_HEADING)

    def continue_after_creation(self):
        self.click(self.CONTINUE_BUTTON)

    def is_account_deleted(self) -> bool:
        return self.is_displayed(self.ACCOUNT_DELETED_HEADING)
