""" Production config. Used when running the application in production datacenters.
"""

from data_decoupling_automation.config.base import Config as BaseConfig


class Config(BaseConfig):
    """Production config."""

    LOG_LEVEL = "INFO"

    # Base URL
    BASE_URL = ""  # This URL will be varied from env to env.
