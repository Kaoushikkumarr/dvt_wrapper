"""
This file will be used for formatting the DVT-Payload, required by DVT as a request payloads.
"""
import logging

from data_decoupling_automation.config.own_config_connection import cnf_dict
from data_decoupling_automation.constants import (
    DB_SOURCE_SCHEMA,
    DB_TARGET_SCHEMA,
    ROW_HASH,
    SCHEMA,
    SOURCE_TABLE,
    TARGET_TABLE,
    VALIDATION_TYPE_LIST,
)
from data_decoupling_automation.dvt_wrapper.models.db_model import ConnectionRequest
from data_decoupling_automation.dvt_wrapper.models.request_model import (
    Aggregates,
    DVTRequestPayload,
    SourceTargetPayload,
)
from data_decoupling_automation.exceptions import BadInputException

# # Added logger to the code.
logger = logging.getLogger(__name__)


def dvt_json_request(
    payload: SourceTargetPayload,
    source_table_schema_list: tuple,
    target_table_schema_list: tuple,
    source_column: str,
    target_column: str,
) -> DVTRequestPayload:
    """
    The dvt_json_request function is used to form the DVT Request Payload.
        It will validate the payload and then form the request payload as per DVT System requested.

    :param payload: SourceTargetPayload: Pass the payload to the function
    :param source_table_schema_list: tuple: Get the source table schema
    :param target_table_schema_list: tuple: Get the target table schema list
    :param source_column: str: Pass the column name of source table
    :param target_column: str: Pass the target_column name to the aggregates_model function,
    :param : Validate the payload for source db
    :return: The dvt request payload pydantic model,
    :doc-author: Kaoushik Kumar
    """
    # Below if condition will check the validation_type of the request payload.
    # Based on the validation_type DVT Json Request Payload will be formed, else it will return False.
    if payload.validation_type in VALIDATION_TYPE_LIST:
        # The below ConnectionRequest Pydantic Model will validate the payload for Source DB
        # and then form the request payload for DVT System.
        source_connection = source_connection_model(payload)
        # The below ConnectionRequest Pydantic Model will validate the payload for Target DB
        # and then form the request payload for DVT System.
        target_connection = target_connection_model(payload)
        # The below Aggregates Pydantic Model will validate the payload
        # and then form the request payload for DVT System.
        aggregates = aggregates_model(payload, source_column, target_column)
        # The below DVTRequestPayload Pydantic Model is the main payload,
        # which will validate and restructure all the above Pydantic Model payload,
        # and then form the request payload as per DVT System requested.
        data_dict = dvt_request_payload(
            source_connection,
            target_connection,
            source_table_schema_list,
            target_table_schema_list,
            aggregates,
            payload,
        )
        if not data_dict:
            logger.error(f"{payload.validation_type} is Invalid validation_type")
            raise BadInputException(
                {
                    "message": f"{payload.validation_type} is Invalid validation_type",
                }
            )
        return data_dict
    else:
        logger.error(f"{payload.validation_type} is Invalid validation_type")
        raise BadInputException(
            {
                "message": f"{payload.validation_type} is Invalid validation_type",
            }
        )


def source_connection_model(
    payload: SourceTargetPayload,
) -> ConnectionRequest:
    """
    The source_connection_model function takes a payload object and returns a ConnectionRequest object.
    The source_connection_model function is used to create the connection request for the source database.

    :param payload: SourceTargetPayload: Pass the payload to the function
    :return: A connection request object
    :doc-author: Kaoushik Kumar
    """
    source_connection = ConnectionRequest(
        source_type=payload.source_database.db_type,
        host=payload.source_database.db_host,
        port=int(payload.source_database.db_port),
        user=payload.source_database.db_user,
        password=payload.source_database.db_password,
        database=payload.source_database.db_name,
    )
    return source_connection


def target_connection_model(
    payload: SourceTargetPayload,
) -> ConnectionRequest:
    """
    The target_connection_model function is used to create a ConnectionRequest object for the target database.

    :param payload: SourceTargetPayload: Pass the payload to the function
    :return: The target connection details
    :doc-author: Kaoushik Kumar
    """
    target_connection = ConnectionRequest(
        source_type=payload.target_database.db_type,
        host=payload.target_database.db_host,
        port=int(payload.target_database.db_port),
        user=payload.target_database.db_user,
        password=payload.target_database.db_password,
        database=payload.target_database.db_name,
    )
    return target_connection


def aggregates_model(
    payload: SourceTargetPayload,
    source_column: str,
    target_column: str,
) -> Aggregates:
    """
    The aggregates_model function creates a new Aggregates object from the
        BasePayload | SchemaValidationPayload | RowValidationPayload: Pass the payload to the function
        and returns it.

    :param payload: SourceTargetPayload: Pass the payload to the function
    :param source_column: str: Create the source_column field in the aggregates model
    :param target_column: str: Create a custom string for the target column name
    :return: An aggregates object
    :doc-author: Kaoushik Kumar
    """
    custom_field_alias, custom_string_type = "", ""
    if payload.validation_type in ["rowcount", "sum_column", "Schema"]:
        # The below value will come from a user's payload as a validation_type,
        # which will use name_must_exist_in_field function to create a custom string from the user's request.
        custom_field_alias = name_must_exist_in_field(payload.validation_type)
        # The below value will come from a user's payload as a validation_type,
        # which will use name_must_exist_type function to create a custom string from the user's request.
        custom_string_type = name_must_exist_type(payload.validation_type)
    aggregates = Aggregates(
        source_column=source_column,
        target_column=target_column,
        field_alias=custom_field_alias,
        type=custom_string_type,
    )
    return aggregates


def name_must_exist_in_field(validation_type):
    """
    The name_must_exist_in_field function is used to validate the user's input.
        It will check if the value exists in the config object or not.
        If it does, then return that value, else throw ValueError.

    :param validation_type: Get the value from user's payload
    :return: A value, which is the name of a field
    :doc-author: Kaoushik Kumar
    """
    # After adding _field_alias to the value, we need to add upper() function.
    # To access any config variables, variable should have to be in upper case as a key.
    value = f"{validation_type}_field_alias".lower()
    config_val = cnf_dict["aggregates"][value]
    if not config_val:
        raise ValueError("Invalid Validation Type")
    return config_val


def name_must_exist_type(validation_type) -> str:
    """
    The name_must_exist_type function is used to validate the validation_type field in the payload.
        The function will check if the value of validation_type exists in the config object or not.
        If it does, then return that value else throw ValueError.

    :param validation_type: Get the value from user's payload
    :return: A string which is a validation type
    :doc-author: Kaoushik Kumar
    """
    # After adding _type to the value, we need to add upper() function.
    # To access any config variables, variable should have to be in upper case as a key.
    value = f"{validation_type}_type".lower()
    config_val = cnf_dict["aggregates"][value]
    if not config_val:
        raise ValueError("Invalid Validation Type")
    return config_val


def dvt_request_payload(
    source_connection: ConnectionRequest,
    target_connection: ConnectionRequest,
    db_source_table_schema_list: tuple,
    db_target_table_schema_list: tuple,
    aggregates: Aggregates,
    payload: SourceTargetPayload,
) -> DVTRequestPayload:
    """
    The dvt_request_payload function is used to create a DVTRequestPayload object.
    The DVTRequestPayload object is the payload that will be sent to the Data Validation Tool (DVT) API.
    This function takes in several arguments and returns a DVTRequestPayload object with those arguments as attributes.

    :param source_connection: ConnectionRequest: Specify the source connection
    :param target_connection: ConnectionRequest: Connect to the target database
    :param db_source_table_schema_list: tuple: Store the schema and table name of source database
    :param db_target_table_schema_list: tuple: Hold the target schema and table name
    :param aggregates: Aggregates: Hold the aggregates information
    :param payload: SourceTargetPayload: Pass the payload
    :return: A dvt request payload object
    :doc-author: Kaoushik Kumar
    """
    data_dict = DVTRequestPayload(
        source_conn=source_connection,
        target_conn=target_connection,
        # The below db_source_table_schema_list tuple will always be holding two tuples(i.e: ('schema1', 'table1')).
        # And we will be using item of first tuple for schema_name(i.e: schema_name=schema1).
        schema_name=db_source_table_schema_list[
            DB_SOURCE_SCHEMA
        ],  # DB_SOURCE_SCHEMA = 0, access first item.
        # The below db_source_table_schema_list tuple will always be holding two tuples(i.e: ('schema1', 'table1')).
        # And we will be using first for table_name(i.e: table_name=table1).
        table_name=db_source_table_schema_list[
            SOURCE_TABLE
        ],  # SOURCE_TABLE = 1, using the constants to access first item.
        # The below db_target_table_schema_list tuple will always be holding two tuples(i.e: ('schema2', 'table2')).
        # We will be using item of second tuple for target_schema_name(i.e: target_schema_name=schema2).
        target_schema_name=db_target_table_schema_list[
            DB_TARGET_SCHEMA
        ],  # DB_TARGET_SCHEMA = 0, access second item.
        # The below db_target_table_schema_list tuple will always be holding two tuples(i.e: ('schema2', 'table2')).
        # And we will be using second for target_table_name(i.e: target_table_name=table2).
        target_table_name=db_target_table_schema_list[
            TARGET_TABLE
        ],  # TARGET_TABLE = 1, using the constants to access second item.
        result_handler=payload.request_handler,
        aggregates=[aggregates],
        threshold=payload.pct_threshold,
    )
    if payload.validation_type == SCHEMA:
        data_dict.__dict__.update(
            labels=payload.labels, format=payload.format, type=payload.type
        )
    elif payload.validation_type == ROW_HASH:
        del data_dict.aggregates, data_dict.threshold, data_dict.result_handler
        data_dict.__dict__.update(
            filter_status=payload.filter_status,
            primary_keys=payload.primary_keys,
            comparison_fields=payload.comparison_fields,
            type=payload.type,
        )
    return data_dict
