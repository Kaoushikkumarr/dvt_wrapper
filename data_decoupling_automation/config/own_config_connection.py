import os

from data_decoupling_automation.config.own_config import Config

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
config_ini = "/config.ini"  # path of your .ini file
ini_path = APP_ROOT + config_ini
cnf_dict = Config.read_configurations_from_ini(ini_path)
