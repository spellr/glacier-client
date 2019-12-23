from typing import cast
from task_manager import TaskManager
from tasks.list_vaults import ListVaultsTask

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMainWindow

from consts import REGIONS


class RegionTree(object):
    def __init__(self, window: QMainWindow):
        self.view: QTreeView = cast(QTreeView, window.findChild(QTreeView, 'treeView'))

        self.model = QStandardItemModel()
        root: QStandardItem = self.model.invisibleRootItem()

        for region in REGIONS:
            item = QStandardItem(region.name)
            root.appendRow(item)
            TaskManager.add_task(ListVaultsTask(region, self.view))

        self.view.setModel(self.model)
