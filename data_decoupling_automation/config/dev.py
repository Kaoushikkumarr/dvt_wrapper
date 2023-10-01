""" Dev config. Used when running the application in development datacenters.
"""

from data_decoupling_automation.config.base import Config as BaseConfig


class Config(BaseConfig):
    """Dev config."""

    LOG_LEVEL = "DEBUG"

    # Base URL
    BASE_URL = "www.example.com/"  # This URL will be varied from env to env.
