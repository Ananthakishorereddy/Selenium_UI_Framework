"""
ConfigReader — loads environment-specific settings from config/config.yaml.
Usage: ConfigReader("qa") or ConfigReader("staging")
"""

import os
import yaml


class ConfigReader:
    def __init__(self, env: str = "qa"):
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "config.yaml"
        )
        with open(config_path, "r") as f:
            full_config = yaml.safe_load(f)

        if env not in full_config:
            raise KeyError(
                f"Environment '{env}' not found in config.yaml. "
                f"Available: {list(full_config.keys())}"
            )

        self._config = full_config[env]

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def get_base_url(self) -> str:
        return self._config.get("base_url", "https://automationexercise.com")

    def get_browser(self) -> str:
        return self._config.get("browser", "chrome")

    def is_headless(self) -> bool:
        return self._config.get("headless", False)

    def get_explicit_wait(self) -> int:
        return self._config.get("explicit_wait", 15)
