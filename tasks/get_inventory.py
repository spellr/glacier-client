import logging

from regions import Region
from tasks.base_task import Task
from tasks.wait_for_inventory import WaitForInventoryTask
from task_manager import TaskManager


class GetInventoryTask(Task):
    def __init__(self, region: Region, vault: str):
        super(GetInventoryTask, self).__init__(region)
        self.vault = vault

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to retrieve inventory")
        job = client.initiate_job(vaultName=self.vault, jobParameters={"Type": "inventory-retrieval"})
        logging.info(f"Initiated job to retrieve inventory. Job id = {job['jobId']}")

        TaskManager.add_task(WaitForInventoryTask(self.region, self.vault, job))

    def __repr__(self):
        return f"Getting last inventory from region '{self.region.name}', vault '{self.vault}'"
