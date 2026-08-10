"""
LoginPage — handles both the Login and the initial Signup (name + email) forms,
which both live on the same /login route on automationexercise.com.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    # ------------------------------------------------------------------ #
    #  Locators — Login section
    # ------------------------------------------------------------------ #
    LOGIN_HEADING = (By.XPATH, "//h2[normalize-space()='Login to your account']")
    LOGIN_EMAIL = (By.XPATH, "//input[@data-qa='login-email']")
    LOGIN_PASSWORD = (By.XPATH, "//input[@data-qa='login-password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@data-qa='login-button']")
    LOGIN_ERROR = (By.XPATH, "//p[contains(text(),'Your email or password is incorrect')]")

    # ------------------------------------------------------------------ #
    #  Locators — Signup initiation section
    # ------------------------------------------------------------------ #
    SIGNUP_HEADING = (By.XPATH, "//h2[normalize-space()='New User Signup!']")
    SIGNUP_NAME = (By.XPATH, "//input[@data-qa='signup-name']")
    SIGNUP_EMAIL = (By.XPATH, "//input[@data-qa='signup-email']")
    SIGNUP_BUTTON = (By.XPATH, "//button[@data-qa='signup-button']")
    SIGNUP_EMAIL_EXISTS_ERROR = (By.XPATH, "//p[contains(text(),'Email Address already exist')]")

    # ------------------------------------------------------------------ #
    #  Login actions
    # ------------------------------------------------------------------ #

    def is_login_page_displayed(self) -> bool:
        return self.is_displayed(self.LOGIN_HEADING)

    def login(self, email: str, password: str):
        self.logger.info(f"Login attempt → {email}")
        self.type(self.LOGIN_EMAIL, email)
        self.type(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_error_displayed(self) -> bool:
        return self.is_displayed(self.LOGIN_ERROR)

    def get_login_error_text(self) -> str:
        return self.get_text(self.LOGIN_ERROR)

    # ------------------------------------------------------------------ #
    #  Signup initiation actions
    # ------------------------------------------------------------------ #

    def is_signup_section_displayed(self) -> bool:
        return self.is_displayed(self.SIGNUP_HEADING)

    def initiate_signup(self, name: str, email: str):
        """Enter name + email in the 'New User Signup' section and submit."""
        self.logger.info(f"Initiating signup → name={name}, email={email}")
        self.type(self.SIGNUP_NAME, name)
        self.type(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)

    def is_email_exists_error_displayed(self) -> bool:
        return self.is_displayed(self.SIGNUP_EMAIL_EXISTS_ERROR)
