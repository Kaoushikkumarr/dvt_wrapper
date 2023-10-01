""" Local config. Used when running the application on your local machine.
"""

from data_decoupling_automation.config.base import Config as BaseConfig


class Config(BaseConfig):
    """Local config."""

    LOG_LEVEL = "DEBUG"
    DEBUG = True

    # Base URL
    BASE_URL = "www.example.com/"  # This URL will be varied from env to env.
