import logging

from regions import Region
from task_manager import TaskManager
from tasks.base_task import Task
from tasks.list_vaults import ListVaultsTask


class CreateVaultTask(Task):
    def __init__(self, region: Region, vault_name: str):
        super(CreateVaultTask, self).__init__(region)
        self.vault_name = vault_name

    def run(self):
        client = self.get_boto_client()
        logging.info("Initiating job to create vault")
        client.create_vault(vaultName=self.vault_name)

        TaskManager.add_task(ListVaultsTask(self.region))

    def __repr__(self):
        return f"Creating vault '{self.vault_name}' in region '{self.region.name}'"
