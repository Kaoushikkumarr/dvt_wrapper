import logging

_logger = logging.getLogger(__name__)


def log_hello_world():
    """
    Example log command, prints Hello World to stdout
    """
    _logger.info("Hello World called from data-decoupling-automation")
