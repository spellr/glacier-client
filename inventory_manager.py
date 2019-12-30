from typing import Dict, Sequence
from collections import defaultdict

from archive import Archive
from regions import Region


class _Inventories(object):
    def __init__(self):
        self.inventories: Dict[Region, Sequence[Archive]] = defaultdict(lambda x: [])

    def new_inventory(self, region_name: Region, inventory: Sequence[Archive]):
        self.inventories[region_name] = inventory

    def get_inventory(self, region_name: Region):
        return self.inventories[region_name]


Inventories = _Inventories()
