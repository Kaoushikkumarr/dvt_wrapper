# import logging
# import os
#
# import flask
#
# logger = logging.getLogger(__name__)
#
#
# CONFIG_NAME_ENVIRONMENT_VARIABLE = "DATA_DECOUPLING_AUTOMATION_CONFIG"
# CONFIG_MODULE_IMPORT_PATH_TEMPLATE = "data_decoupling_automation.config.{name}.Config"
#
#
# def _read_config_name_from_environment() -> str:
#     """Read config name environment variable."""
#
#     try:
#         logger.debug(
#             f"Attempting to read config name from environment variable '{CONFIG_NAME_ENVIRONMENT_VARIABLE}'."
#         )
#         config_name = os.environ[CONFIG_NAME_ENVIRONMENT_VARIABLE]
#         logger.debug(f"Successfully read config name '{config_name}'.")
#         return config_name
#     except KeyError:
#         raise KeyError(
#             f"Failed to read config name from environment variable '{CONFIG_NAME_ENVIRONMENT_VARIABLE}'."
#         )
#
#
# def _generate_config_import_path(name: str) -> str:
#     """Generate config import path from config name."""
#
#     return CONFIG_MODULE_IMPORT_PATH_TEMPLATE.format(name=name)
#
#
# def load(app: flask.Flask) -> None:
#
#     logger.debug("Starting to load config.")
#
#     try:
#         config_name = _read_config_name_from_environment()
#         config_import_path = _generate_config_import_path(config_name)
#
#         logger.debug(
#             f"Attempting to load config '{config_name}' from module '{config_import_path}'."
#         )
#         app.config.from_object(config_import_path)
#         logger.info(
#             f"Successfully loaded config '{config_name}' from module '{config_import_path}'."
#         )
#
#     except Exception as e:
#         logger.exception(f"Failed to load config: {e}")
#         raise
