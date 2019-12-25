import time
from datetime import timedelta, datetime

from munch import munchify

from regions import Region
from tasks.base_task import Task


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

        completed = False
        while not completed:
            job_output = client.describe_job(vaultName=self.vault, jobId=self.job_id)
            completed = job_output["Completed"]

            self.next_check = (datetime.now() + timedelta(seconds=self.SLEEP_TIME)).time()
            self.update_task()

            time.sleep(self.SLEEP_TIME)

    def __repr__(self):
        if self.next_check:
            next_check = self.next_check.strftime("%H:%M:%S")
            return f"Waiting for inventory from vault '{self.vault}' in '{self.region.name}'. Next check in {next_check}"
        else:
            return f"Waiting for inventory from vault '{self.vault}' in '{self.region.name}'"
