import os
import json
from croco_tools import LoggingConfig

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(PROJECT_PATH, 'linea_voyage_0')
TESTS_PATH = os.path.join(PROJECT_PATH, 'tests')
CONFIG_PATH = os.path.join(PROJECT_PATH, 'config.json')

with open(CONFIG_PATH, 'r') as file:
    file = json.load(file)
    logging_config = file['logging']
    logging_config = LoggingConfig(**logging_config)
