import logging
from typing import Iterator, List, BinaryIO

import ijson
from munch import munchify

from widgets import widgets_map
from archive import Archive
from inventory_manager import Inventories
from regions import Region
from tasks.base_task import Task


class DownloadArchiveTask(Task):
    def __init__(self, region: Region, vault: str, job: dict, output_file: str):
        super(DownloadArchiveTask, self).__init__(region)
        self.vault = vault
        self.job = munchify(job)
        self.job_id = self.job.jobId
        self.output_file = output_file

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to retrieve inventory")
        job = client.get_job_output(vaultName=self.vault, jobId=self.job_id)
        body_stream: BinaryIO = job['body']

        with open(self.output_file, 'wb') as output:
            chunk = body_stream.read(4 * 1024 * 1024)
            while chunk:
                output.write(chunk)

    def __repr__(self):
        return f"Downloading archive from region '{self.region.name}', vault '{self.vault}'"
