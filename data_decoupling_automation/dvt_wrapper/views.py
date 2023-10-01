"""
This file is for routes, which will have all HTTP methods for the json request.
"""
import logging
import re

import requests
from flask import Blueprint, request
from flask_restful import Api, Resource
from requests import Response

from data_decoupling_automation.constants import (
    AGGREGATION_TYPE,
    DIFFERENCE,
    FORMAT,
    GROUP_BY_COLUMNS,
    LABELS,
    NUM_RANDOM_ROWS,
    PCT_DIFFERENCE,
    PCT_THRESHOLD,
    PRIMARY_KEYS,
    SECOND_ITEM_OF_TABLE_SCHEMA,
    SOURCE_AGG_VALUE,
    SOURCE_TABLE_NAME,
    TARGET_AGG_VALUE,
    TARGET_TABLE_NAME,
    VALIDATION_STATUS,
    VALIDATION_TYPE,
)
from data_decoupling_automation.dvt_wrapper.models.request_model import (
    DVTRequestPayload,
    SourceTargetPayload,
)
from data_decoupling_automation.dvt_wrapper.models.response_model import (
    ResponseData,
    ResponseModel,
)
from data_decoupling_automation.exceptions import BadInputException
from data_decoupling_automation.utils.dvt_utils import dvt_json_request

# Registering the Blueprint for dvt-routes.
dvt_wrapper_bp = Blueprint("routes", __name__, url_prefix="/")
apps = Api(dvt_wrapper_bp)

# Added logger to the code.
logger = logging.getLogger(__name__)


class DVTWrapper(Resource):
    """Class for DVTWrapper API."""

    def post(self):
        """
        The post function will take the request payload and send that to dvt-wrapper.
            ---
            tags:
              - DVT Wrapper API

        :return: The response in json format
        :doc-author: Kaoushik Kumar
        """
        try:
            # The below line will be used to validate Request Payload using Pydantic BaseModel.
            payload = SourceTargetPayload(**request.get_json())
            # The below will take the request payload and send that to dvt-wrapper.
            response = WrapperController().wrapper(payload)
            return response.dict()
        except Exception as e:
            logger.error(str(e))
            # If any exception will be occurred in payload, will be returned through exception.
            return ResponseData(response=False, results=str(e)).dict()


class WrapperController:
    def wrapper(
        self,
        payload: SourceTargetPayload,
    ) -> ResponseData:
        """
        The wrapper function is used to validate the request payload and also
            send the API request to DVT-System.

        :param payload: SourceTargetPayload: Get the request payload from user
        :return: The response data object
        :doc-author: Kaoushik Kumar
        """
        results, response_dict, columns, source_column, target_column = (
            [],
            [],
            [],
            "",
            "",
        )
        if payload.use_random_rows and payload.random_row_batch_size is not None:
            if not 1 <= payload.random_row_batch_size <= 100:
                logger.error(
                    "random_row_batch_size key should must present and have to be in the range "
                    "in between 1 to 100, if use_random_rows is set to be true"
                )
                raise BadInputException(
                    {
                        "message": "random_row_batch_size key should must present and have to be in the range "
                        "in between 1 to 100, if use_random_rows is set to be true"
                    }
                )
        if payload.columns:
            columns = payload.columns.replace(" ", "").split(";")
        table_lists = payload.tables.replace(" ", "").split(";")
        for table_list in table_lists:
            # The below line will be used to validate the table_list strings followed by comma(',')
            db_source_schema_name, db_target_schema_name = self._table_list(table_list)
            # The below line will be used to validate the list of columns and return tuple based on the len(columns).
            source_column, target_column = (
                self._columns(columns.pop(0)) if len(columns) > 0 else ("", "")
            )
            # The below dvt_json_request function will be used to restructure the payload as per DVT-System.
            requested_payload = dvt_json_request(
                payload,
                db_source_schema_name,
                db_target_schema_name,
                source_column,
                target_column,
            )
            # The below code will be used to send the API call request to DVT-System, to get the response for request.
            response = self._dvt_post_request(payload, requested_payload)
            response.raise_for_status()
            try:
                # Validating the DVT-Response using Pydantic Model(ResponseModel).
                response_dict = self._dvt_response_payload(
                    table_list, payload, response
                )
                results.extend(response_dict)
            except Exception as e:
                logger.exception(str(e))
                # Below logger will log the same error in a text(readable) format.
                logger.error(response.text)
                return ResponseData(response=False, results=response.text)
        return ResponseData(response=True, results=results)

    def _split_and_validate(self, input_string: str, error_message: str) -> tuple:
        """
        The _split_and_validate function takes in a string and an error message.
        It then checks to see if the input_string contains a comma, and if it does not,
        it logs an error with the given error_message. If there is no comma in the input_string,
        the function raises a BadInputException with that same message. Otherwise, it returns
        a tuple of strings split on commas.

        :param input_string: str: Pass in the input string to be split
        :param error_message: str: Pass in the error message that will be displayed if the input is not valid
        :return: A tuple of strings
        :doc-author: Kaoushik Kumar
        """
        if "," not in input_string:
            logger.error(error_message)
            raise BadInputException({"message": error_message})
        return tuple(re.split(r",", input_string))

    def _table_list(self, table_string: str) -> tuple:
        """
        The _table_list function is used to split the table_list into two lists.
            The first list will be source schema and table name, second list will be target schema and table name.
            After split, if the length of both tuple is not equal to 2, then it raises BadInputException
            with Invalid User's Payload.

        :param table_string: str: Pass the table list from the request body
        :return: A tuple of two lists
        :doc-author: Kaoushik Kumar
        """
        error_message = f"{table_string} Invalid Payload"
        table_list = self._split_and_validate(table_string, error_message)
        # Below regex_patterns will be used to match comma characters and periods in the strings.
        split_table_list = [re.split(r"\.", x) for x in table_list]
        source_schema_table_list, target_schema_table_list = split_table_list
        # There might be chance to get invalid empty_string(" ") as a table name(i.e: ['schema1', '']) or etc...
        # The below list comprehension will be used to remove empty_string using loop.
        list_of_source_schema_table = [
            value for value in source_schema_table_list if value != ""
        ]
        list_of_target_schema_table = [
            value for value in target_schema_table_list if value != ""
        ]
        # The length of both tuple should, have a length of two, else the lists are invalid.
        if not (
            len(list_of_source_schema_table) == 2
            and len(list_of_target_schema_table) == 2
        ):
            logger.error(f"{table_list} Invalid Payload")
            raise BadInputException({"message": f"{table_list} Invalid Payload"})
        return list_of_source_schema_table, list_of_target_schema_table

    def _columns(self, column_string: str) -> tuple:
        """
        The _columns function is a helper function that takes in the column_string, which will be the column_name of
        the tables. The _columns function will always return a tuple of two strings.

        :param self: Represent the instance of the class
        :param column_string: str: Pass in the column_name of the table
        :return: A tuple of two strings
        :doc-author: Kaoushik Kumar
        """
        error_message = f"{column_string} Invalid Payload"
        # column_string will be the column_name of the tables, which will always be returning the tuple of two strings.
        source_column, target_column = self._split_and_validate(
            column_string, error_message
        )
        return source_column, target_column  # ('column_name1', 'column_name2')

    def _dvt_post_request(
        self, payload: SourceTargetPayload, requested_payload: DVTRequestPayload
    ) -> Response:
        """
        The _dvt_post_request function is a helper function that takes in a DVTRequestPayload object and
        returns the response from the DVT API.

        param payload: SourceTargetPayload: Pass in the payload to be sent to dvt
        param requested_payload: DVTRequestPayload: Pass in the payload to be sent to dvt
        :return: A response object
        :doc-author: Kaoushik Kumar
        """
        response = requests.post(
            url=str(payload.striim_node), json=requested_payload.dict()
        )
        return response

    def _dvt_response_payload(
        self,
        table_list: str,
        payload: SourceTargetPayload,
        response_data: Response,
    ) -> list:
        """
        The _dvt_response_payload function takes in a table_list, payload, and response_data.
        It then creates an empty list called result. It then iterates through the dvt_response_list
        and appends each item to the result list as a ResponseModel object with all of its attributes
        set to their corresponding values from the dvt response.

        :param table_list: str: Get the table name from the payload
        :param payload: SourceTargetPayload: Get the source and target details
        :param response_data: Response: Get the response from the post request
        :return: A list of dictionaries
        :doc-author: Kaoushik Kumar
        """
        result = []
        dvt_response_list = response_data.json()
        for dvt_response in dvt_response_list:
            response_dict = ResponseModel(
                validation_name=table_list.split(",")[
                    SECOND_ITEM_OF_TABLE_SCHEMA
                ].split(".")[SECOND_ITEM_OF_TABLE_SCHEMA]
                + "."
                + payload.validation_type,
                validation_type=dvt_response.get(VALIDATION_TYPE),
                aggregation_type=dvt_response.get(AGGREGATION_TYPE),
                source_table_name=dvt_response.get(SOURCE_TABLE_NAME),
                source_agg_value=dvt_response.get(SOURCE_AGG_VALUE),
                target_table_name=dvt_response.get(TARGET_TABLE_NAME),
                target_agg_value=dvt_response.get(TARGET_AGG_VALUE),
                difference=dvt_response.get(DIFFERENCE),
                pct_difference=dvt_response.get(PCT_DIFFERENCE),
                pct_threshold=dvt_response.get(PCT_THRESHOLD),
                validation_status=dvt_response.get(VALIDATION_STATUS),
                labels=dvt_response.get(LABELS),
                format=dvt_response.get(FORMAT),
                group_by_columns=dvt_response.get(GROUP_BY_COLUMNS),
                primary_keys=dvt_response.get(PRIMARY_KEYS),
                num_random_rows=dvt_response.get(NUM_RANDOM_ROWS),
            )
            result.append(response_dict.dict())
        return result


#  Registering End-Points
apps.add_resource(DVTWrapper, "/api/v1/dvt-run-validation")
