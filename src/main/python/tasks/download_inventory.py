import logging
from typing import Iterator, List

import ijson

from widgets import widgets_map
from archive import Archive
from inventory_manager import Inventories
from regions import Region
from tasks.base_task import Task


class DownloadInventoryTask(Task):
    def __init__(self, region: Region, vault: str, job: dict):
        super(DownloadInventoryTask, self).__init__(region)
        self.vault = vault
        self.job = job
        self.job_id = self.job["jobId"]

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to retrieve inventory")
        job = client.get_job_output(vaultName=self.vault, jobId=self.job_id)
        body_stream = job['body']

        inventory: List[Archive] = list(self.get_archives_list(body_stream))

        Inventories.new_inventory(self.region, self.vault, inventory)
        widgets_map['files_table'].display_inventory(self.region, self.vault, inventory)

    def __repr__(self):
        return f"Downloading inventory from region '{self.region.name}', vault '{self.vault}'"

    def get_archives_list(self, body_stream) -> Iterator[Archive]:
        for archive in ijson.items(body_stream, "ArchiveList.item"):
            yield Archive(archive)
