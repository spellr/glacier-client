import logging

from regions import Region
from tasks.base_task import Task


class ListVaultsTask(Task):
    def __init__(self, region: Region, tree_view):
        super(ListVaultsTask, self).__init__(region)
        self.tree_view = tree_view

    def __repr__(self):
        return f"{self.__class__.__name__}({self.region})"

    def run(self):
        client = self.get_boto_client()
        vaults = client.list_vaults()['VaultList']
        for vault in vaults:
            logging.info(f"Found vault - {self.region.name}: {vault['VaultName']}")

        for vault in vaults:
            vault_name = vault['VaultName']
            self.tree_view.add_vault(self.region, vault_name)
