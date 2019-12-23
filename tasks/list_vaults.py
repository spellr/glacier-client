import boto3

from consts import Region
from tasks.base_task import Task
from keys import PUBLIC_KEY, SECRET_KEY

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import Qt, QModelIndex


class ListVaultsTask(Task):
    def __init__(self, region: Region, view: QTreeView):
        super(ListVaultsTask, self).__init__()
        self.region = region
        self.view = view

    def __repr__(self):
        return f"{self.__class__.__name__}({self.region})"

    def run(self):
        session = boto3.session.Session()
        client = session.client('glacier', region_name=self.region.code,
                                aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
        vaults = []  # client.list_vaults()['VaultList']
        for vault in vaults:
            print(f"{self.region.name}: {vault['VaultName']}")

        root: QModelIndex = self.view.rootIndex()
        child_count = self.view.model().rowCount(root)
        for row in range(child_count):
            region: QModelIndex = root.child(row, 0)
            import rpdb ; rpdb.set_trace()
            print(region)
            asdf = self.view.model().data(region, Qt.DisplayRole)
            print(asdf)
