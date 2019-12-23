import boto3

from consts import Region
from tasks.base_task import Task
from keys import PUBLIC_KEY, SECRET_KEY

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItem


class ListVaultsTask(Task):
    def __init__(self, region: Region, view: QTreeView):
        super(ListVaultsTask, self).__init__()
        self.region = region
        self.view = view
        self.model = self.view.model()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.region})"

    def run(self):
        session = boto3.session.Session()
        client = session.client('glacier', region_name=self.region.code,
                                aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
        vaults = client.list_vaults()['VaultList']
        for vault in vaults:
            print(f"{self.region.name}: {vault['VaultName']}")

        root: QModelIndex = self.view.rootIndex()
        child_count = self.model.rowCount(root)
        parent = QModelIndex()

        for i in range(child_count):
            row = self.model.index(i, 0, parent)
            cur_region = row.data()
            if self.region.name == cur_region:
                break
        else:
            raise ValueError(f"Failed to find region {self.region}")

        for vault in vaults:
            vault_name = vault['VaultName']
            item = QStandardItem(vault_name)
            self.model.itemFromIndex(row).appendRow(item)

        self.view.expandAll()

        # Refresh model to see new rows
        self.model.rowsInserted.emit(parent, 0, child_count)
