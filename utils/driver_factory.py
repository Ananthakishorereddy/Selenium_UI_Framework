"""
DriverFactory — centralizes WebDriver initialization for Chrome, Firefox, and Edge.
Uses Selenium 4.x built-in Selenium Manager (no external webdriver-manager needed),
which avoids SSL certificate issues on corporate/proxy networks.
"""

from selenium import webdriver


class DriverFactory:
    @staticmethod
    def get_driver(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
        """
        Return a WebDriver instance for the given browser.
        Selenium Manager (bundled with Selenium 4.x) automatically locates
        or downloads the correct driver binary — no manual setup required.
        """
        browser = browser.lower().strip()

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            return webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Firefox(options=options)

        elif browser == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            return webdriver.Edge(options=options)

        else:
            raise ValueError(
                f"Unsupported browser: '{browser}'. "
                "Supported options: chrome, firefox, edge"
            )
