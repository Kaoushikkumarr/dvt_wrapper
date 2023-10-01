"""
This file will be used for testing the Pytest Validation Test Cases for dvt_utils.py file.
"""
import pytest

from data_decoupling_automation.dvt_wrapper.models.db_model import ConnectionRequest
from data_decoupling_automation.utils.dvt_utils import (
    # request_handler_model,
    aggregates_model,
    dvt_request_payload,
    source_connection_model,
    target_connection_model,
)

from data_decoupling_automation.dvt_wrapper.models.request_model import SourceTargetPayload, Aggregates


# from data_decoupling_automation.dvt_wrapper.models.db_model import SourceTargetPayload


# {
#     "db_type": "source_type",
#     "db_host": "host",
#     "db_port": 1234,
#     "db_user": "user",
#     "db_password": "password",
#     "db_name": "database",
# }

# @pytest.fixture
# def valid_requested_source_model(user_payload) -> SourceTargetPayload:
#     return {"source_database": user_payload}


@pytest.fixture
def valid_requested_source_model(user_payload: SourceTargetPayload):
    source_connection = ConnectionRequest(
        source_type=user_payload.source_database.db_type,
        host=user_payload.source_database.db_host,
        port=int(user_payload.source_database.db_port),
        user=user_payload.source_database.db_user,
        password=user_payload.source_database.db_password,
        database=user_payload.source_database.db_name,
    )
    return source_connection


@pytest.fixture
def valid_response_source_model():
    return {
        "source_type": "source_type",
        "host": "host",
        "port": 1234,
        "user": "user",
        "password": "password",
        "database": "database",
    }


def test_valid_source_connection_model(
    valid_requested_source_model, valid_response_source_model: dict
):
    expected_response = valid_response_source_model
    actual_response = source_connection_model(valid_requested_source_model)
    assert actual_response == expected_response


# def test_invalid_value_for_port_payload(valid_requested_source_model: dict):
#     valid_requested_source_model["source_database"]["db_port"] = "hello_world"
#     with pytest.raises(ValueError):
#         source_connection_model(valid_requested_source_model)


def test_invalid_value_for_port_payload(valid_requested_source_model: SourceTargetPayload):
    # valid_requested_source_model["source_database"]["db_port"] = "hello_world"
    valid_requested_source_model.source_database.db_port = "hello_world"
    with pytest.raises(ValueError):
        source_connection_model(valid_requested_source_model)


# def test_cast_port_into_integer(
#     valid_requested_source_model: dict, valid_response_source_model: dict
# ):
#     valid_requested_source_model["source_database"]["db_port"] = "1234"
#     expected_response = valid_response_source_model
#     actual_response = source_connection_model(valid_requested_source_model)
#     assert actual_response == expected_response

def test_cast_port_into_integer(
    valid_requested_source_model: SourceTargetPayload, valid_response_source_model
):
    # valid_requested_source_model["source_database"]["db_port"] = "1234"
    valid_requested_source_model.source_database.db_port = "1234"
    expected_response = valid_response_source_model
    actual_response = source_connection_model(valid_requested_source_model)
    assert actual_response == expected_response


# @pytest.fixture
# def missing_keys_for_source_model_payload():
#     return {
#         "source_type": "source_type",
#         "password": "password",
#         "database": "database",
#     }
@pytest.fixture
def missing_keys_for_source_model_payload(user_payload: SourceTargetPayload):
    # return {
    #     "source_type": "source_type",
    #     "password": "password",
    #     "database": "database",
    # }

    source_connection = ConnectionRequest(
        source_type=user_payload.source_database.db_type,
        host=user_payload.source_database.db_host,
        port=int(user_payload.source_database.db_port)
    )
    return source_connection


def test_missing_keys_for_source_model_payload(
    missing_keys_for_source_model_payload,
):
    with pytest.raises(KeyError):
        source_connection_model(missing_keys_for_source_model_payload)


# @pytest.fixture
# def valid_requested_target_model(user_payload):
#     return {"target_database": user_payload}


@pytest.fixture
def valid_requested_target_model(user_payload: SourceTargetPayload):
    # return {"target_database": user_payload}
    target_connection = ConnectionRequest(
        source_type=user_payload.source_database.db_type,
        host=user_payload.source_database.db_host,
        port=int(user_payload.source_database.db_port),
        user=user_payload.source_database.db_user,
        password=user_payload.source_database.db_password,
        database=user_payload.source_database.db_name,
    )
    return target_connection


@pytest.fixture
def valid_response_target_model():
    return {
        "source_type": "source_type",
        "host": "host",
        "port": 1234,
        "user": "user",
        "password": "password",
        "database": "database",
    }


def test_valid_target_connection_model(
    valid_requested_target_model, valid_response_target_model
):
    expected_response = valid_response_target_model
    actual_response = target_connection_model(valid_requested_target_model)
    assert actual_response == expected_response


# @pytest.fixture
# def request_handler_models():
#     return {"type": "Stackdriver", "project_id": "project_id", "environment": "dev"}
#
#
# def test_request_handler_model(request_handler_models: dict):
#     expected_response = request_handler_models
#     actual_response = request_handler_model(request_handler_models["project_id"])
#     assert actual_response == expected_response


@pytest.fixture
def source_columns():
    return "source_column"


@pytest.fixture
def target_columns():
    return "target_column"


@pytest.fixture
def sum_count_response_aggregates_model():
    return {
        "source_column": "source_column",
        "target_column": "target_column",
        "field_alias": "my_sum",
        "type": "sum",
    }


@pytest.fixture
def rowcount_response_aggregates_model():
    return {
        "source_column": "source_column",
        "target_column": "target_column",
        "field_alias": "count",
        "type": "count",
    }


# def test_positive_sum_column_aggregates_model(
#     source_columns, target_columns, sum_count_response_aggregates_model
# ):
#     valid_sum_column_validation_type = {"validation_type": "sum_column"}
#     expected_response = sum_count_response_aggregates_model
#     actual_response = aggregates_model(
#         valid_sum_column_validation_type, source_columns, target_columns
#     )
#     assert actual_response == expected_response


def test_positive_sum_column_aggregates_model(
    source_columns, target_columns, sum_count_response_aggregates_model, user_payload: SourceTargetPayload
):
    # valid_sum_column_validation_type = {"validation_type": "sum_column"}
    user_payload.validation_type = "sum_column"
    expected_response = sum_count_response_aggregates_model
    actual_response = aggregates_model(
        user_payload, source_columns, target_columns
    )
    assert actual_response == expected_response


# def test_negative_sum_column_aggregates_model(source_columns, target_columns):
#     invalid_sum_column_validation_type = {"validation_type": "sumcolumn"}
#     with pytest.raises(KeyError):
#         aggregates_model(
#             invalid_sum_column_validation_type, source_columns, target_columns
#         )


def test_negative_sum_column_aggregates_model(source_columns, target_columns, user_payload: SourceTargetPayload):
    # invalid_sum_column_validation_type = {"validation_type": "sumcolumn"}
    user_payload.validation_type = "sumcolumn"
    with pytest.raises(KeyError):
        aggregates_model(
            user_payload, source_columns, target_columns
        )


def test_valid_row_column_aggregates_model(
    source_columns, target_columns, rowcount_response_aggregates_model, user_payload: SourceTargetPayload
):
    # valid_rowcount_validation_type = {"validation_type": "rowcount"}
    user_payload.validation_type = "rowcount"
    expected_response = rowcount_response_aggregates_model
    actual_response = aggregates_model(
        user_payload, source_columns, target_columns
    )
    assert actual_response == expected_response


def test_invalid_row_column_aggregates_model(
    source_columns,
    target_columns,
        user_payload: SourceTargetPayload
):
    # invalid_rowcount_validation_type = {"validation_type": "row_count"}
    user_payload.validation_type = "row_count"
    with pytest.raises(KeyError):
        aggregates_model(
            user_payload, source_columns, target_columns
        )


@pytest.fixture
def pct_threshold():
    payload = {"pct_threshold": {"threshold": 0}}
    return payload


# def test_dvt_request_payload(
#     valid_response_source_model: dict,
#     valid_response_target_model: dict,
#     request_handler_models: dict,
#     sum_count_response_aggregates_model: dict,
#     pct_threshold: dict,
#     dvt_request_payloads: dict,
# ):
#     db_source_schema = ["dbo", "foo"]
#     db_target_schema = ["public", "foo"]
#     expected_response = dvt_request_payloads
#
#     actual_response = dvt_request_payload(
#         valid_response_source_model,
#         valid_response_target_model,
#         db_source_schema,
#         db_target_schema,
#         request_handler_models,
#         sum_count_response_aggregates_model,
#         pct_threshold,
#     )
#     assert actual_response == expected_response


def test_dvt_request_payload(
    valid_response_source_model: ConnectionRequest,
    valid_response_target_model: ConnectionRequest,
    # request_handler_models: dict,
    sum_count_response_aggregates_model: Aggregates,
    # pct_threshold: dict,
    dvt_request_payloads: dict,
        user_payload: SourceTargetPayload
):
    db_source_schema = ("dbo", "foo")
    db_target_schema = ("public", "foo")
    expected_response = dvt_request_payloads

    actual_response = dvt_request_payload(
        valid_response_source_model,
        valid_response_target_model,
        db_source_schema,
        db_target_schema,
        # request_handler_models,
        sum_count_response_aggregates_model,
        user_payload,
    )
    assert actual_response == expected_response
