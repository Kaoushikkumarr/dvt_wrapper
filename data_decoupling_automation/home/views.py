import logging
import random
from time import sleep

# import wf_feature_toggle
# import wf_stats
from flask import Blueprint, jsonify, render_template, request

# from pydantic import ValidationError

# from data_decoupling_automation.constants import (
#     DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE,
# )
# from data_decoupling_automation.exceptions import BadInputException
# from data_decoupling_automation.home.models import ExampleModel

home_blueprint = Blueprint("home", __name__, url_prefix="/")
logger = logging.getLogger(__name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    """
    Send a hello world response to let the user know the service is running
    """
    logger.debug("Received home endpoint request.")
    return jsonify({"greeting": "Hello data-decoupling-automation!"})


@home_blueprint.route("/hello_world", methods=["GET"])
def hello_world():
    """
    Render a hello world template
    """
    return render_template("hello_world.html", request_vars=request.args)


# @home_blueprint.route("json_example", methods=["POST"])
# def json_example():
#     """
#     Demonstrates usage of the Pydantic package, and how it can validate request input using Pydantic Models.
#     Demonstrates usage of the wf_stats package, and how it can publish a metric that counts the occurrences of an event.
#     """
#
#     success = False
#     request_json = request.get_json(force=True)
#
#     try:
#         model = ExampleModel(**request_json)
#         success = True
#     except ValidationError as e:
#         raise BadInputException(e.json())
#     finally:
#         wf_stats.record_increment(
#             "data-decoupling-automation-json_example",
#             tags=[wf_stats.Tag("success", str(success))],
#         )
#
#     return jsonify({"message": f"JSON Validated! ({model})"})


@home_blueprint.route("expensive_task", methods=["GET"])
# @wf_stats.record_execution_time("time_expensive_task")
def expensive_task():
    """
    Execute something that takes time to execute.

    Demonstrates usage of the wf_stats package, and how it can publish the execution time of a function.
    """
    logger.debug("Starting an expensive task.")
    # sleep for a random amount of seconds to simulate an expensive task
    delay = random.uniform(0.25, 1)  # nosec
    sleep(delay)
    logger.debug("Expensive task complete.")
    return jsonify({"task_duration": delay})


# @home_blueprint.route("feature_toggle_example", methods=["GET"])
# def feature_toggle_example():
#     """Demonstrates how to access feature toggle states."""
#     message = (
#         "on"
#         if wf_feature_toggle.is_enabled(DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE)
#         else "off"
#     )
#     return jsonify({"message": f"The toggle is... {message}!"})
