""" Testing config. Used when running the test suite.
"""

from data_decoupling_automation.config.base import Config as BaseConfig


class Config(BaseConfig):
    """Testing config."""

    TESTING = True

    # Base URL
    BASE_URL = ""  # This URL will be varied from env to env.
