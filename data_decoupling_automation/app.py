"""
This file initializes the Flask app and boostraps various modules and interfaces.
"""

import logging
import os
from typing import Tuple

# import wf_logging
# import wf_stats
from flask import Blueprint, Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from data_decoupling_automation.constants import (
    DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE,
)
from data_decoupling_automation.dvt_wrapper.views import dvt_wrapper_bp
from data_decoupling_automation.exceptions import BadInputException
from data_decoupling_automation.home.views import home_blueprint

# from wf_feature_toggle import Backend
# from wf_feature_toggle import configure as configure_toggles
# from wf_feature_toggle.testing import configure as configure_local_toggles
# from wf_healthcheck import get_flask_healthcheck_blueprint
# from wf_healthcheck.api import mark_ready

# from data_decoupling_automation.utils.config import load as load_application_config

# feature toggles that will be enabled locally
LOCAL_ENABLED_FEATURE_TOGGLES = [DATA_DECOUPLING_AUTOMATION_EXAMPLE_TOGGLE]

DEFAULT_BLUEPRINTS = (
    # get_flask_healthcheck_blueprint(),
    home_blueprint,
    dvt_wrapper_bp,
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)

    # load application configuration (more info: docs/configuration.md)
    # load_application_config(app)

    # configure_logging(app)
    configure_blueprints(app, DEFAULT_BLUEPRINTS)
    # configure_feature_toggles()
    configure_error_handlers(app)
    configure_debug_toolbar(app)
    # configure_stats()

    logger.warning(f"Flask Worker Started! PID={os.getpid()}.")

    # mark application as ready for kubernetes
    # mark_ready()

    return app


def configure_blueprints(app: Flask, blueprints: Tuple[Blueprint, ...]):
    """
    Registers the Flask blueprints with the flask app
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


# def configure_logging(app: Flask) -> None:
#     """
#     Sets up wf_logging, on the root logger.
#     wf_logging sends GELF logs to kibana for any module under the project root.
#     Also will log to stdout if in debug mode or in testing.
#     """
#
#     # wf_logging.configure sets up the root logger for logging to Kibana
#     wf_logging.configure("data_decoupling_automation", level=app.config["LOG_LEVEL"])


def configure_error_handlers(app):
    """
    Handle uncaught exceptions that happen in the flask views.
    """

    @app.errorhandler(BadInputException)
    def handle_bad_input_exception(e: BadInputException) -> None:
        """
        BadInputException can be raised with a response_dict to send back a 400 to the caller.
        """
        response = jsonify(e.response_dict)
        response.status_code = 400
        return response


def configure_debug_toolbar(app: Flask) -> None:
    """
    Add debug toolbar for UI based apps. Only active in debug mode.
    """
    DebugToolbarExtension(app)


# def configure_feature_toggles() -> None:
#     """
#     Bootstrap wf_feature_toggle lib.
#     Locally, we can define our own toggle specific bahavior.
#     For dev and prod environments, we want to use a specific backend as a source of truth
#     """
#     # locally, we have the ability to set default behavior for our feature toggles.
#     # this allows our local runtime behavior to not depend on the shared dev feature toggle values
#     if os.environ.get("FLASK_DEBUG"):
#         configure_local_toggles(enabled=LOCAL_ENABLED_FEATURE_TOGGLES)
#
#     # in a shared dev or prod environment, we would like to retrieve feature toggle values using the purest backend
#     if not (
#         os.environ.get("FLASK_DEBUG")
#         or os.environ.get("DATA_DECOUPLING_AUTOMATION_CONFIG") == "test"
#     ):
#         configure_toggles(Backend.purest)


# def configure_stats() -> None:
#     wf_stats.configure()


# This is required for flask to bootstrap without gunicorn for development
if os.environ.get("FLASK_DEBUG"):
    app = create_app()
