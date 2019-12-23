from typing import cast

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMainWindow

from consts import REGIONS


class RegionTree(object):
    def __init__(self, window: QMainWindow):
        self.view: QTreeView = cast(QTreeView, window.findChild(QTreeView, 'treeView'))

        self.model = QStandardItemModel()
        root: QStandardItem = self.model.invisibleRootItem()

        for region in REGIONS:
            item = QStandardItem(region)
            root.appendRow(item)

        self.view.setModel(self.model)
