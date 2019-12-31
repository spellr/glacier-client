from typing import Dict, Sequence
from collections import defaultdict

from archive import Archive
from regions import Region


class _Inventories(object):
    def __init__(self):
        self.inventories: Dict[str, Sequence[Archive]] = defaultdict(lambda: [])

    def new_inventory(self, region: Region, vault: str, inventory: Sequence[Archive]):
        self.inventories[region.code + vault] = inventory

    def get_inventory(self, region: Region, vault: str):
        return self.inventories[region.code + vault]


Inventories = _Inventories()
