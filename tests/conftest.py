# import pytest
# from flask import Flask
# from flask.testing import FlaskClient
#
# from data_decoupling_automation.app import create_app
#
# # Enable the pytest plugin for core libraries.
# # See README for each library for details
# pytest_plugins = ["wf_feature_toggle.testing.fixture", "wf_stats.testing"]
#
#
# @pytest.fixture
# def app() -> Flask:
#     """
#     A pytest fixture that returns an app instance
#     """
#     return create_app()
#
#
# @pytest.fixture
# def client(app) -> FlaskClient:
#     """
#     Sets up a flask client fixture.
#
#     :param app: Dependency injected from the app fixture above
#     """
#     return app.test_client()
#
#
# @pytest.fixture(autouse=True)
# def ensure_testing(app):
#     assert app.config["TESTING"]


"""
This file will be used for to contain the fixtures, which will be commonly used in more than one file.
"""
import pytest


@pytest.fixture
def user_payload():
    return {
        "db_type": "source_type",
        "db_host": "host",
        "db_port": 1234,
        "db_user": "user",
        "db_password": "password",
        "db_name": "database",
    }


@pytest.fixture
def dvt_request_payloads(
    sum_count_response_aggregates_model,
    request_handler_models,
    valid_response_source_model,
):
    return {
        "aggregates": [sum_count_response_aggregates_model],
        "result_handler": request_handler_models,
        "schema_name": "dbo",
        "source_conn": valid_response_source_model,
        "table_name": "foo",
        "target_conn": valid_response_source_model,
        "target_schema_name": "public",
        "target_table_name": "foo",
        "type": "Column",
    }


@pytest.fixture
def dvt_striim_node_url():
    return "www.example.com"
