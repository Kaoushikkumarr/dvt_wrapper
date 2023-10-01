""" Base config. This should not be used directly.
"""


class Config(object):
    """Base config."""

    LOG_LEVEL = "WARNING"

    # This needs to be unique for each Flask app, and is used to coordinate deployments
    HEALTHCHECK_STATUS_FILE = "/tmp/data_decoupling_automation_down"  # nosec

    SECRET_KEY = "NOT SECRET"  # nosec

    # Below two line are for rowcount
    ROWCOUNT_FIELD_ALIAS = "count"
    ROWCOUNT_TYPE = "count"
    # Below two line are for sum_count
    SUM_COLUMN_FIELD_ALIAS = "my_sum"
    SUM_COLUMN_TYPE = "sum"
