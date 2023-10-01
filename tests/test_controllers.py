# """
# This file will be used for testing the Pytest Validation Test Cases for controllers.py file.
# """
# from unittest.mock import patch
#
# import pytest
#
# # import controllers.controller
# import data_decoupling_automation.dvt_wrapper.views
# from data_decoupling_automation.dvt_wrapper.models.db_model import ConnectionRequest
# from data_decoupling_automation.dvt_wrapper.models.request_model import Aggregates, SourceTargetPayload
#
# # Creating object for WrapperController()
# # controller_obj = controllers.controller.WrapperController()
# controller_obj = data_decoupling_automation.dvt_wrapper.views.WrapperController()
#
#
# @pytest.fixture
# def response_table_names():
#     table_data_one, table_data_two = (
#         ["Sales", "SalesOrderHeader"],
#         ["public", "SalesOrderHeader"],
#     )
#     return table_data_one, table_data_two
#
#
# def test_valid_table_list(response_table_names):
#     valid_request_table_names = "Sales.SalesOrderHeader,public.SalesOrderHeader"
#     expected_response = response_table_names
#
#     actual_response = controller_obj._table_list(valid_request_table_names)
#     assert actual_response == expected_response
#
#
# # def test_invalid_table_list():
# #     invalid_request_table_names = "Sales.SalesOrderHeader,public."
# #     # expected_response = controller_obj._table_list(invalid_request_table_names)
# #     # assert expected_response is False
#
# def test_invalid_table_list():
#     invalid_request_table_names = "Sales.SalesOrderHeader,public."
#     with pytest.raises(ValueError):
#         controller_obj._table_list(invalid_request_table_names)
#
#
# # @pytest.fixture
# # def request_column_names():
# #     return "id,id"
#
#
# @pytest.fixture
# def response_column_names():
#     column_data_one, column_data_two = (
#         "id",
#         "id",
#     )  # ('department_id', 'department_id')
#     return column_data_one, column_data_two
#
#
# # @pytest.fixture
# # def valid_column_request_payload():
# #     # payload = dict()
# #     # payload['columns'] = "id,id"
# #     # return payload
# #     return "id,id"
#
#
# # def test_valid_column_list(
# #         # valid_column_request_payload,
# #         response_column_names,
# #         # request_column_names
# # ):
# #     valid_column_request = "id, id"
# #     expected_response = response_column_names
# #     actual_response = controller_obj._columns(
# #         valid_column_request,
# #         # request_column_names
# #     )
# #     assert actual_response == expected_response
#
#
# def test_valid_column_list(
#         response_column_names,
# ):
#     valid_column_request = "id, id"
#     expected_response = response_column_names
#     actual_response = controller_obj._columns(
#         valid_column_request,
#     )
#     assert actual_response == expected_response
#
#
#
# # @pytest.fixture
# # def invalid_column_request_payload():
# #     # payload = dict()
# #     # payload['columns'] = "id"
# #     return "id"
#
#
# def test_invalid_column_list():
#     invalid_column_request = "id"
#     with pytest.raises(ValueError):
#         controller_obj._columns(invalid_column_request)
#
#
# # @pytest.fixture
# # def sum_count_response_aggregates_model():
# #     return {
# #         "source_column": "source_column",
# #         "target_column": "target_column",
# #         "field_alias": "my_sum",
# #         "type": "sum",
# #     }
#
# @pytest.fixture
# def sum_count_response_aggregates_model():
#     return Aggregates(
#         source_column="source_column",
#         target_column="target_column",
#         field_alias="my_sum",
#         type="sum"
#     )
#
#
# @pytest.fixture
# def request_handler_models():
#     return {"type": "Stackdriver", "project_id": "project_id", "environment": "dev"}
#
#
# # @pytest.fixture
# # def valid_response_source_model():
#     # return {
#     #     "source_type": "source_type",
#     #     "host": "host",
#     #     "port": 1234,
#     #     "user": "user",
#     #     "password": "password",
#     #     "database": "database",
#     # }
#
#
# @pytest.fixture
# def valid_response_source_model():
#     return ConnectionRequest(
#         source_type="source_type",
#         host="host",
#         port=1234,
#         user="user",
#         password="password",
#         database="database"
#     )
#
#
# # @patch("controllers.controller.WrapperController._dvt_post_request")
# @patch(
#     "data_decoupling_automation.dvt_wrapper.views.WrapperController._dvt_post_request"
# )
# def test_valid_dvt_url(mock_post, dvt_striim_node_url, dvt_request_payloads):
#     expected_response = "success"
#     mock_post.return_value = (200, {"status": expected_response})
#     assert (
#             controller_obj._dvt_post_request(dvt_striim_node_url, dvt_request_payloads)
#             == mock_post.return_value
#     )
#
#
# # @patch("controllers.controller.WrapperController._dvt_post_request")
# @patch(
#     "data_decoupling_automation.dvt_wrapper.views.WrapperController._dvt_post_request"
# )
# def test_invalid_dvt_url(mock_post, dvt_striim_node_url, dvt_request_payloads):
#     expected_response = "Not Found"
#     mock_post.return_value = (404, {"status": expected_response})
#     assert (
#             controller_obj._dvt_post_request(dvt_striim_node_url, dvt_request_payloads)
#             == mock_post.return_value
#     )
#
#
# # @patch("controllers.controller.WrapperController._dvt_post_request")
# @patch(
#     "data_decoupling_automation.dvt_wrapper.views.WrapperController._dvt_post_request"
# )
# def test_invalid_method_dvt_url(mock_post, dvt_striim_node_url, dvt_request_payloads):
#     expected_response = "Method Not Allowed"
#     mock_post.return_value = (405, {"status": expected_response})
#     assert (
#             controller_obj._dvt_post_request(dvt_striim_node_url, dvt_request_payloads)
#             == mock_post.return_value
#     )
#
#
# # @pytest.fixture
# # def invalid_wrappers_payload(user_payload):
# #     return {
# #         "source_database": user_payload,
# #         "target_database": user_payload,
# #         "tables": "dbo.foo,public.foo",
# #         "validation_type": "abc",
# #         "pct_threshold": 0,
# #         "columns": "id,id",
# #     }
#
# @pytest.fixture
# def invalid_wrappers_payload(user_payload: SourceTargetPayload):
#     return {
#         "source_database": user_payload.source_database,
#         "target_database": user_payload.target_database,
#         "tables": "dbo.foo,public.foo",
#         "validation_type": "abc",
#         "pct_threshold": 0,
#         "columns": "id,id",
#     }
#
#
# # def test_invalid_wrapper(invalid_wrappers_payload):
# #     # expected_response = controller_obj.wrapper(invalid_wrappers_payload)
# #     # assert expected_response.get('response') is False
#
# def test_invalid_wrapper(invalid_wrappers_payload):
#     with pytest.raises(ValueError):
#         controller_obj.wrapper(invalid_wrappers_payload)
