import os
import pickle
from typing import Dict, Sequence
from collections import defaultdict

from consts import DATA_DIR
from archive import Archive
from regions import Region


class _Inventories(object):
    INVENTORY_CACHE_FILE = os.path.join(DATA_DIR, "inventories.pickle")

    def __init__(self):
        self.inventories: Dict[str, Sequence[Archive]]
        if os.path.exists(self.INVENTORY_CACHE_FILE):
            try:
                self.inventories = pickle.load(open(self.INVENTORY_CACHE_FILE, 'rb'))
            except EOFError:
                self.inventories = {}
        else:
            self.inventories = {}

    def _dump_to_cache(self):
        pickle.dump(self.inventories, open(self.INVENTORY_CACHE_FILE, 'wb'))

    def new_inventory(self, region: Region, vault: str, inventory: Sequence[Archive]):
        self.inventories[region.code + vault] = inventory
        self._dump_to_cache()

    def get_inventory(self, region: Region, vault: str):
        key = region.code + vault
        if key in self.inventories:
            return self.inventories[key]
        else:
            return []


Inventories = _Inventories()
