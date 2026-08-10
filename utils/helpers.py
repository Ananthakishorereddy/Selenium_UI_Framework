"""
Helpers — reusable utility functions for test data loading, random data generation,
and screenshot capture.
"""

import json
import os
import random
import string
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

_TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "test_data.json")
_SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")


def load_test_data(file_path: str = _TEST_DATA_PATH) -> dict:
    """Load and return the test data JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_random_email(domain: str = "qatest.com") -> str:
    """Generate a unique random email address."""
    prefix = "".join(random.choices(string.ascii_lowercase, k=8))
    ts = datetime.now().strftime("%H%M%S")
    return f"{prefix}{ts}@{domain}"


def generate_random_string(length: int = 8) -> str:
    """Generate a random alphabetic string."""
    return "".join(random.choices(string.ascii_letters, k=length))


def generate_random_phone() -> str:
    """Generate a random 10-digit phone number string."""
    return "".join(random.choices(string.digits, k=10))


def take_screenshot(driver, name: str = "screenshot") -> str:
    """
    Save a screenshot to reports/screenshots/.
    Returns the file path of the saved screenshot.
    """
    os.makedirs(_SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(_SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    logger.info(f"Screenshot saved: {path}")
    return path
