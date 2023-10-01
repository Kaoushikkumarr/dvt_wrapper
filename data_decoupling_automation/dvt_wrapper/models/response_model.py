"""
This file will be used for validating the response payload from the DVT System...
"""
from typing import List, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    The ResponseModel Model will be used to return the response from the DVT-System
    after the validation of below Pydantic Model Fields.
    """

    validation_name: str
    validation_type: str
    aggregation_type: Optional[str]
    source_table_name: str
    source_agg_value: str
    target_table_name: str
    target_agg_value: str
    difference: Optional[float]
    pct_difference: Optional[float]
    pct_threshold: Optional[int]
    validation_status: str
    labels: Optional[List]
    format: Optional[str]
    group_by_columns: Optional[str]
    primary_keys: Optional[str]
    num_random_rows: Optional[str]


class ResponseData(BaseModel):
    response: bool
    results: list | str
