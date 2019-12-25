import boto3

from regions import Region
from tasks.base_task import Task
from keys import PUBLIC_KEY, SECRET_KEY


class ListVaultsTask(Task):
    def __init__(self, region: Region, tree_view):
        super(ListVaultsTask, self).__init__()
        self.region = region
        self.tree_view = tree_view

    def __repr__(self):
        return f"{self.__class__.__name__}({self.region})"

    def run(self):
        session = boto3.session.Session()
        client = session.client('glacier', region_name=self.region.code,
                                aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
        vaults = client.list_vaults()['VaultList']
        for vault in vaults:
            print(f"{self.region.name}: {vault['VaultName']}")

        for vault in vaults:
            vault_name = vault['VaultName']
            self.tree_view.add_vault(self.region, vault_name)
