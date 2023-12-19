import json
import os
import time

from croco_selenium import ChromeDriver
from logs.logger import Logger
from globals import EXTENSIONS_PATH, PROJECT_PATH

logger = Logger("main_py")
metamask_extension_paths = [os.path.join(PROJECT_PATH, 'extensions/metamask.crx')]

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())


def main():
    driver = ChromeDriver(extension_paths=metamask_extension_paths)


    time.sleep(15)



if __name__ == '__main__':
    main()