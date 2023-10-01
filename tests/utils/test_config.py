# import pytest
#
# from data_decoupling_automation.utils import config
#
# KEY = "PROJECT_CONFIG"
# NAME = "test"
# PATH = "project.config.test.Config"
#
#
# @pytest.fixture()
# def logger(mocker):
#     return mocker.patch("data_decoupling_automation.utils.config.logger")
#
#
# @pytest.fixture()
# def environ(mocker):
#     environ = mocker.patch("data_decoupling_automation.utils.config.os.environ")
#     environ.__getitem__.return_value = NAME
#     return environ
#
#
# def test_read_config_name_from_environment(environ):
#     assert config._read_config_name_from_environment() == NAME
#
#
# def test_read_config_name_from_environment__raises_KeyError(mocker, environ, logger):
#
#     environ.__getitem__.side_effect = KeyError
#
#     with pytest.raises(KeyError):
#         config._read_config_name_from_environment()
#
#
# def test_generate_config_import_path():
#     name = "foo"
#     assert config._generate_config_import_path(
#         name
#     ) == config.CONFIG_MODULE_IMPORT_PATH_TEMPLATE.format(name=name)
#
#
# def test_load(mocker, logger):
#
#     mocker.patch(
#         "data_decoupling_automation.utils.config._generate_config_import_path",
#         return_value=PATH,
#     )
#
#     app = mocker.Mock()
#
#     config.load(app)
#
#     assert logger.debug.called
#     assert logger.debug.call_args_list == [
#         (("Starting to load config.",), {}),
#         (
#             (
#                 f"Attempting to read config name from environment variable '{config.CONFIG_NAME_ENVIRONMENT_VARIABLE}'.",
#             ),
#             {},
#         ),
#         ((f"Successfully read config name '{NAME}'.",), {}),
#         ((f"Attempting to load config '{NAME}' from module '{PATH}'.",), {}),
#     ]
#
#     assert logger.info.called
#     assert logger.info.call_args == (
#         (f"Successfully loaded config '{NAME}' from module '{PATH}'.",),
#         {},
#     )
#
#     assert app.config.from_object.called
#     assert app.config.from_object.call_args == ((PATH,), {})
#
#
# def test_load__raises_Exception(mocker, logger):
#
#     mocker.patch(
#         "data_decoupling_automation.utils.config._generate_config_import_path",
#         return_value=PATH,
#     )
#
#     app = mocker.Mock()
#     exception_message = "exception message"
#     app.config.from_object.side_effect = Exception(exception_message)
#
#     with pytest.raises(Exception) as exception:
#         config.load(app)
#
#     assert str(exception.value) == exception_message
#     assert logger.exception.called
#     assert logger.exception.call_args == (
#         (f"Failed to load config: {exception_message}",),
#         {},
#     )
