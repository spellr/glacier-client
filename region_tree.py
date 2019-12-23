import traceback
from typing import cast
from keys import PUBLIC_KEY, SECRET_KEY

import boto3

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMainWindow

from consts import REGIONS


class GetVaultsThread(QThread):
    def __init__(self, *args, **kwargs):
        super(GetVaultsThread, self).__init__(*args, **kwargs)

    def _run(self) -> None:
        for region in REGIONS:
            print(region)

            client = boto3.client('glacier', region_name=region.code,
                                  aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
            vaults = client.list_vaults()['VaultList']
            for vault in vaults:
                print(f"{region.name}: {vault['VaultName']}")

    def run(self) -> None:
        try:
            return self._run()
        except:
            traceback.print_exc()

    def __del__(self):
        self.wait()


class RegionTree(object):
    def __init__(self, window: QMainWindow):
        self.view: QTreeView = cast(QTreeView, window.findChild(QTreeView, 'treeView'))

        self.model = QStandardItemModel()
        root: QStandardItem = self.model.invisibleRootItem()

        for region in REGIONS:
            item = QStandardItem(region.name)
            root.appendRow(item)

        self.view.setModel(self.model)

        GetVaultsThread(self.view).start()
