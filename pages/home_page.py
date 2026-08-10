"""
HomePage — automationexercise.com landing page.
Handles navigation bar actions and subscription widget.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    # ------------------------------------------------------------------ #
    #  Locators
    # ------------------------------------------------------------------ #
    LOGO = (By.CSS_SELECTOR, "img[alt='Website for automation practice']")

    # Nav links — use href-based CSS selectors for reliability across icon/whitespace variations
    NAV_HOME = (By.CSS_SELECTOR, "a[href='/']")
    NAV_SIGNUP_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    NAV_PRODUCTS = (By.CSS_SELECTOR, "a[href='/products']")
    NAV_CART = (By.CSS_SELECTOR, "a[href='/view_cart']")
    NAV_CONTACT_US = (By.CSS_SELECTOR, "a[href='/contact_us']")
    NAV_TEST_CASES = (By.CSS_SELECTOR, "a[href='/test_cases']")
    NAV_LOGGED_USER = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    NAV_LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")
    NAV_DELETE_ACCOUNT = (By.CSS_SELECTOR, "a[href='/delete_account']")

    # Subscription
    SUBSCRIPTION_HEADING = (By.XPATH, "//h2[normalize-space()='Subscription']")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUBSCRIPTION_SUCCESS = (By.XPATH, "//div[contains(@class,'alert-success')]")

    # Slider / homepage content
    SLIDER = (By.ID, "slider")

    # ------------------------------------------------------------------ #
    #  Actions
    # ------------------------------------------------------------------ #

    def _dismiss_ad_overlay(self):
        """
        automationexercise.com renders Google Ad iframes that can sit on top of
        nav links and block standard clicks. This method attempts to remove any
        visible ad iframe from the DOM so subsequent clicks land on the correct
        element. Safe to call even when no ad is present.
        """
        try:
            self.driver.execute_script("""
                var ads = document.querySelectorAll(
                    'iframe, div[id*="google_ads"], div[id*="aswift"], ins.adsbygoogle'
                );
                ads.forEach(function(el) { el.remove(); });
            """)
        except Exception:
            pass

    def is_home_page_visible(self) -> bool:
        return self.is_displayed(self.LOGO)

    def go_to_login_page(self):
        self.logger.info("Nav → Signup / Login")
        self._dismiss_ad_overlay()
        self.js_click(self.NAV_SIGNUP_LOGIN)

    def go_to_products(self):
        self.logger.info("Nav → Products")
        self._dismiss_ad_overlay()
        self.js_click(self.NAV_PRODUCTS)

    def go_to_cart(self):
        self.logger.info("Nav → Cart")
        self._dismiss_ad_overlay()
        self.js_click(self.NAV_CART)

    def go_to_contact_us(self):
        self.logger.info("Nav → Contact Us")
        self._dismiss_ad_overlay()
        self.js_click(self.NAV_CONTACT_US)

    def is_user_logged_in(self) -> bool:
        return self.is_displayed(self.NAV_LOGGED_USER)

    def get_logged_in_username(self) -> str:
        text = self.get_text(self.NAV_LOGGED_USER)
        return text.replace("Logged in as", "").strip()

    def logout(self):
        self.logger.info("Logging out")
        self._dismiss_ad_overlay()
        self.js_click(self.NAV_LOGOUT)

    def delete_account(self):
        self.logger.info("Deleting account via nav")
        self._dismiss_ad_overlay()
        self.js_click(self.NAV_DELETE_ACCOUNT)

    def subscribe_with_email(self, email: str) -> bool:
        """Scroll to subscription section, enter email, submit, and return success flag."""
        self.logger.info(f"Subscribing with: {email}")
        self.scroll_to_element(self.SUBSCRIPTION_EMAIL)
        self.type(self.SUBSCRIPTION_EMAIL, email)
        self.js_click(self.SUBSCRIPTION_BUTTON)
        return self.is_displayed(self.SUBSCRIPTION_SUCCESS)
