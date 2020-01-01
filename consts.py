import os
import appdirs

DEBUG = True

APP_NAME = "glacier_client"

DATA_DIR = appdirs.user_data_dir(APP_NAME)
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
