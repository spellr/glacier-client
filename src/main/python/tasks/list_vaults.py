import logging

from tasks.base_task import Task
from widgets import widgets_map


class ListVaultsTask(Task):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.region})"

    def run(self):
        client = self.get_boto_client()
        vaults = client.list_vaults()['VaultList']
        for vault in vaults:
            logging.info(f"Found vault - {self.region.name}: {vault['VaultName']}")

        for vault in vaults:
            vault_name = vault['VaultName']
            widgets_map['region_tree'].add_vault(self.region, vault_name)
