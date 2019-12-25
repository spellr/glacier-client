import time
from datetime import timedelta, datetime

from munch import munchify

import consts
from regions import Region
from task_manager import TaskManager
from tasks.base_task import Task
from tasks.download_inventory import DownloadInventoryTask


class WaitForInventoryTask(Task):
    SLEEP_TIME = 15 * 60

    def __init__(self, region: Region, vault: str, job: dict):
        super(WaitForInventoryTask, self).__init__(region)
        self.vault = vault
        self.job = munchify(job)
        self.job_id = self.job.jobId
        self.next_check = None

    def run(self):
        client = self.get_boto_client()

        job_output = client.describe_job(vaultName=self.vault, jobId=self.job_id)
        completed = job_output["Completed"]

        while not completed:
            self.next_check = (datetime.now() + timedelta(seconds=self.SLEEP_TIME)).time()
            self.update_task()

            time.sleep(self.SLEEP_TIME)

            job_output = client.describe_job(vaultName=self.vault, jobId=self.job_id)
            completed = job_output["Completed"]

        TaskManager.add_task(DownloadInventoryTask(self.region, self.vault, self.job))

    def __repr__(self):
        if self.next_check:
            next_check = self.next_check.strftime("%H:%M:%S")
            return f"Waiting for inventory from vault '{self.vault}' in '{self.region.name}'. Next check in {next_check}"
        else:
            return f"Waiting for inventory from vault '{self.vault}' in '{self.region.name}'"
