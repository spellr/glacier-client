import os
import appdirs

DEBUG = False

APP_NAME = "glacier_client"

DATA_DIR = appdirs.user_data_dir(APP_NAME)
os.makedirs(DATA_DIR, exist_ok=True)

KEYS_FILE = os.path.join(DATA_DIR, "keys.yaml")

UPLOAD_PART_SIZE = 2**23  # 8MB
