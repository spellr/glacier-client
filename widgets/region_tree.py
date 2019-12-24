from typing import cast
from task_manager import TaskManager
from tasks.list_vaults import ListVaultsTask

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMainWindow, QAction

from consts import REGIONS


class _RegionTree(object):
    def __init__(self):
        self.view = None
        self.model = None

    def initialize(self, window: QMainWindow):
        self.view: QTreeView = cast(QTreeView, window.findChild(QTreeView, 'treeView'))

        get_inventory_action = QAction("asdf", self.view)
        get_inventory_action.triggered.connect(self.get_inventory_action)
        self.view.addAction(get_inventory_action)

        self.model = QStandardItemModel()
        root: QStandardItem = self.model.invisibleRootItem()
        self.view.setModel(self.model)

        for region in REGIONS:
            item = QStandardItem(region.name)
            root.appendRow(item)
            TaskManager.add_task(ListVaultsTask(region, self.view))

    def get_inventory_action(self):
        print(self.view.selectedIndexes()[0].data())


RegionTree = _RegionTree()
