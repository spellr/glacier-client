import time
from enum import Enum
from datetime import timedelta, datetime

from munch import munchify

import consts
from regions import Region
from task_manager import TaskManager
from tasks.base_task import Task
from tasks.download_inventory import DownloadInventoryTask


class JobOutput(Enum):
    INVENTORY = "inventory"
    ARCHIVE = "archive"


class WaitForJobTask(Task):
    SLEEP_TIME = 15 * 60

    def __init__(self, region: Region, vault: str, job: dict, job_output: JobOutput):
        super(WaitForJobTask, self).__init__(region)
        self.vault = vault
        self.job = munchify(job)
        self.job_id = self.job.jobId
        self.next_check = None
        self.job_output = job_output

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

        if self.job_output == JobOutput.INVENTORY:
            TaskManager.add_task(DownloadInventoryTask(self.region, self.vault, self.job))
        else:
            TaskManager.add_task(DownloadArchiveTask(self.region, self.vault, self.job))

    def __repr__(self):
        if self.next_check:
            next_check = self.next_check.strftime("%H:%M:%S")
            return f"Waiting for {self.job_output.value} from vault '{self.vault}' in '{self.region.name}'. Next check in {next_check}"
        else:
            return f"Waiting for {self.job_output.value} from vault '{self.vault}' in '{self.region.name}'"
