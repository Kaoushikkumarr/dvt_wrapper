# """
# These test use pytest https://pytest.readthedocs.io/en/latest/
#
# Note: client is a pytest fixture that is dependency injected from data_decoupling_automation/tests/conftest.py
#
# """
#
# from flask.testing import FlaskClient
#
# from data_decoupling_automation.constants import (
#     DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE,
# )
#
#
# def test_404(client: FlaskClient) -> None:
#     """
#     Example test shows a non-existent route returns a 404
#     """
#
#     response = client.get("/nonExistentEndpoint")
#
#     assert response.status_code == 404
#
#
# def test_get(client: FlaskClient) -> None:
#     """
#     Example test hitting the index route
#     """
#
#     response = client.get("/")
#     response_data = json.loads(response.data)
#
#     assert response.status_code == 200
#     assert response_data == {"greeting": "Hello data-decoupling-automation!"}
#
#
# def test_example(client: FlaskClient) -> None:
#     """
#     Test example json validation route
#     """
#
#     response = client.post(
#         "/json_example",
#         data=json.dumps({"example_id": 1, "example_message": "testing"}),
#         content_type="application/json",
#     )
#     response_data = json.loads(response.data)
#
#     assert response.status_code == 200
#     assert response_data == {
#         "message": "JSON Validated! (example_id=1 example_message='testing')"
#     }
#
#
# def test_example_fails_with_bad_payload(client: FlaskClient) -> None:
#     """
#     Test example json validation route fails with bad data
#     """
#
#     response = client.post(
#         "/json_example",
#         data=json.dumps({"example_id": "not a number"}),
#         content_type="application/json",
#     )
#
#     assert response.status_code == 400
#
#
# SOME_DELAY = 0.1  # secs
#
#
# def test_expensive_task_reports_delay(mocker, client: FlaskClient) -> None:
#     """
#     Test example json validation route fails with bad data
#     """
#     # replace random.uniform() with a function that always returns a single value
#     mocker.patch("random.uniform", return_value=SOME_DELAY)
#
#     response = client.get("/expensive_task")
#     response_data = json.loads(response.data)
#
#     assert response_data == {"task_duration": SOME_DELAY}
#
#
# def test_feature_toggle_example__hit_endpoint__toggle_on(
#     feature_toggle, mocker, client: FlaskClient
# ) -> None:
#     feature_toggle(enabled=[DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE])
#
#     response = client.get("/feature_toggle_example")
#     response_data = json.loads(response.data)
#
#     assert "on" in response_data["message"]
#
#
# def test_feature_toggle_example__hit_endpoint__toggle_off(
#     feature_toggle, mocker, client: FlaskClient
# ) -> None:
#     feature_toggle(disabled=[DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE])
#
#     response = client.get("/feature_toggle_example")
#     response_data = json.loads(response.data)
#
#     assert "off" in response_data["message"]
