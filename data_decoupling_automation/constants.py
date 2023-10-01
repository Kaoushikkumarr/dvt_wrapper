"""
This file will be used for adding the constant variables.
"""

DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE = "DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE"

# Mapping Connection Constants
TARGET_TABLE_NAME = "target_table_name"
PCT_THRESHOLD = "pct_threshold"
THRESHOLD = "threshold"


# Mapping DB Constants
SOURCE_DATABASE = "source_database"
TARGET_DATABASE = "target_database"
DB_HOST = "db_host"
DB_USER = "db_user"  # nosec
DB_PASSWORD = "db_password"  # nosec
DB_NAME = "db_name"  # nosec
DB_PORT = "db_port"
DB_TYPE = "db_type"


# DVT Response
VALIDATION_TYPE = "validation_type"
AGGREGATION_TYPE = "aggregation_type"
SOURCE_TABLE_NAME = "source_table_name"
SOURCE_AGG_VALUE = "source_agg_value"
TARGET_AGG_VALUE = "target_agg_value"
DIFFERENCE = "difference"
PCT_DIFFERENCE = "pct_difference"
VALIDATION_STATUS = "validation_status"
LABELS = "labels"
FORMAT = "format"
GROUP_BY_COLUMNS = "group_by_columns"
PRIMARY_KEYS = "primary_keys"
NUM_RANDOM_ROWS = "num_random_rows"
SOURCE_DB_USER_NAME = "SOURCE_DB_USER_NAME"  # nosec
TARGET_DB_DUMMY_PASSWORD = "TARGET_DB_DUMMY_PASSWORD"  # nosec
SCHEMA = "Schema"
ROW_HASH = "row_hash"
USE_RANDOM_ROWS = "use_random_rows"
RANDOM_ROW_BATCH_SIZE = "random_row_batch_size"

FIRST_ITEM_OF_SOURCE_COLUMN_LIST = 0
SECOND_ITEM_OF_TARGET_COLUMN_LIST = 1

SECOND_ITEM_OF_TABLE_SCHEMA = 1

# Below two lines will be used for source and target tables.
SOURCE_TABLE = 1
TARGET_TABLE = 1

# Below two lines will be used for source and target schemas.
DB_SOURCE_SCHEMA = 0
DB_TARGET_SCHEMA = 0

VALIDATION_TYPE_LIST = ["rowcount", "sum_column", "Schema", "row_hash"]
