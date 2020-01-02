import os
from typing import Dict

import yaml

from consts import KEYS_FILE


class Keys(object):
    ACCESS_KEY: str = None
    SECRET_KEY: str = None

    @classmethod
    def to_dict(cls) -> Dict:
        return {
            "access_key": cls.ACCESS_KEY,
            "secret_key": cls.SECRET_KEY
        }

    @classmethod
    def from_dict(cls, d: Dict):
        cls.ACCESS_KEY = d["access_key"]
        cls.SECRET_KEY = d["secret_key"]

    @classmethod
    def dump_to_file(cls):
        data = cls.to_dict()
        yaml.dump(data, open(KEYS_FILE, 'w'))

    @classmethod
    def load_from_file(cls):
        if not os.path.exists(KEYS_FILE):
            return

        data = yaml.safe_load(open(KEYS_FILE, 'r'))
        cls.from_dict(data)


Keys.load_from_file()
