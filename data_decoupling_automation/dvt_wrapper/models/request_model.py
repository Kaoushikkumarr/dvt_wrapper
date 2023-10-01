"""
This file contains the main request models, they will be used for validating the request payload from
the DVT system...
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from data_decoupling_automation.dvt_wrapper.models.db_model import (
    ConnectionRequest,
    DataBase,
)


class PrimaryComparisonKeys(BaseModel):
    """
    This PrimaryComparisonKeys field is also a part of DVT Request Payload which need to be in the form of List.
    """

    source_column: Optional[str]
    target_column: Optional[str]
    field_alias: Optional[str]
    cast: Optional[str]


class SourceTargetPayload(BaseModel):
    """
    The SourceTargetPayload Model will be used to accepting the request payload from the End-Users.
    """

    target_database: DataBase
    source_database: DataBase
    project_id: str
    striim_node: str
    tables: str
    validation_type: str
    type: Optional[str]
    columns: Optional[str]
    grouped_columns: Optional[List]
    primary_keys: Optional[List[PrimaryComparisonKeys]]
    comparison_fields: Optional[List[PrimaryComparisonKeys]]
    filter_status: Optional[Literal[None, "fail", "pass", "warn"]]
    pct_threshold: Optional[int] = 0
    labels: Optional[List]
    format: Optional[str]
    request_handler: Optional[str | dict]
    use_random_rows: Optional[bool] = False
    random_row_batch_size: Optional[int] = Field(ge=1, le=100)


class Aggregates(BaseModel):
    """
    This Aggregates field is also a part of DVT Request Payload which need to be in the form of List of aggregates.
    """

    source_column: Optional[str]
    target_column: Optional[str]
    field_alias: Optional[str]
    type: Optional[str]


class DVTRequestPayload(BaseModel):
    """
    This DVTRequestPayload is the main payload, which has consolidated all the above Pydantic Models of DVT System and
    Restructured is as per DVT Request Payload.
    """

    source_conn: ConnectionRequest
    target_conn: ConnectionRequest
    type: Optional[str] = "Column"
    schema_name: str
    table_name: str
    target_schema_name: str
    target_table_name: str
    result_handler: Optional[str | dict] # Available in 3.9 version
    aggregates: List[Aggregates]
    threshold: Optional[int]
