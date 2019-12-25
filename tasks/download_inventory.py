import logging
from typing import Iterator
from collections import defaultdict

import ijson
from munch import munchify

from archive import Archive
from regions import Region
from tasks.base_task import Task


class DownloadInventoryTask(Task):
    def __init__(self, region: Region, vault: str, job: dict):
        super(DownloadInventoryTask, self).__init__(region)
        self.vault = vault
        self.job = munchify(job)
        self.job_id = self.job.jobId

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to retrieve inventory")
        job = client.output = client.get_job_output(vaultName=self.vault, jobId=self.job_id)
        body_stream = job['body']

        directory_structure = self.create_dir_structure(body_stream)
        print(directory_structure)

    def __repr__(self):
        return f"Downloading inventory from region '{self.region.name}', vault '{self.vault}'"

    def create_dir_structure(self, body_stream) -> dict:
        def nested_dict():
            return defaultdict(nested_dict)

        def default_to_regular(d):
            if isinstance(d, defaultdict):
                d = {k: default_to_regular(v) for k, v in d.items()}
            return d

        dirs = nested_dict()
        for archive in self.get_archives_list(body_stream):
            parts = archive.path.split('/')
            marcher = dirs
            for key in parts[:-1]:
                marcher = marcher[key]
            marcher[parts[-1]] = archive
        return default_to_regular(dirs)

    def get_archives_list(self, body_stream) -> Iterator[Archive]:
        for archive in ijson.items(body_stream, "ArchiveList.item"):
            yield Archive(archive)
